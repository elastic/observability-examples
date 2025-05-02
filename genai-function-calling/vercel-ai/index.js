const {createAzure} = require('@ai-sdk/azure');
const {createOpenAI} = require('@ai-sdk/openai');
const {extractReasoningMiddleware, generateText, tool, wrapLanguageModel} = require('ai');
const {z} = require('zod');
const {mcpClientMain} = require('./mcp');

const openai = process.env.AZURE_OPENAI_API_KEY
    ? createAzure({ // coerce to standard OpenAI SDK ENV variables
        apiKey: process.env.AZURE_OPENAI_API_KEY,
        baseURL: new URL('openai/deployments/', process.env.AZURE_OPENAI_ENDPOINT).href,
        apiVersion: process.env.OPENAI_API_VERSION || '2024-10-01-preview'
    })
    : createOpenAI({
        baseURL: process.env.OPENAI_BASE_URL || 'https://api.openai.com/v1'
    });
const model = process.env.CHAT_MODEL || 'gpt-4o-mini';

const getLatestElasticsearchVersion = tool({
    description: 'Get the latest version of Elasticsearch',
    parameters: z.object({
        majorVersion: z.number().optional().describe('Major version to filter by (e.g. 7, 8). Defaults to latest'),
    }),
    execute: async ({majorVersion}) => {
        const response = await fetch('https://artifacts.elastic.co/releases/stack.json');
        const data = await response.json();
        const latest = data.releases
            // Filter out non-release versions (e.g. -rc1) and remove " GA" suffix
            .filter(release => !release.version.includes('-'))
            .filter(release => {
                if (!majorVersion) {
                    return true;
                }
                return release.version.startsWith(majorVersion + '.');
            })
            .map(release => release.version.replace(' GA', ''))
            // "8.9.1" > "8.10.0", unless configured to handle *numeric* segments
            .sort((a, b) => a.localeCompare(b, undefined, {numeric: true}))
            .pop();
        if (!latest) {
            throw new Error('No stable versions found');
        }
        return latest;
    },
});

const tools = {get_latest_elasticsearch_version: getLatestElasticsearchVersion};

/**
 * Runs the agent with the given tools.
 *
 * @param {import('ai').ToolSet} tools - The tools the LLM can use to answer the question.
 */
async function runAgent(tools) {
    const {text} = await generateText({
        // If using qwen3, remove the reasoning tags from output. GPT models will not have
        // such tags making it effectively a no-op.
        model: wrapLanguageModel({
            model: openai(model),
            middleware: [extractReasoningMiddleware({ tagName: 'think' })],
        }),
        messages: [{role: 'user', content: "What is the latest version of Elasticsearch 8?"}],
        temperature: 0,
        tools,
        tool_choice: 'auto',
        maxSteps: 10,
        experimental_telemetry: {isEnabled: true},
    });

    console.log(text);
}

async function main() {
    if (process.argv.some(arg => arg.startsWith("--mcp"))) {
        return await mcpClientMain(runAgent, tools);
    }
    await runAgent(tools);
}

main().catch(error => {
    console.error('Error:', error);
    process.exit(1);
});
