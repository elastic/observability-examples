using System.ClientModel; // for ApiKeyCredential
using System.ComponentModel;
using System.Diagnostics;
using System.Diagnostics.CodeAnalysis;
using System.Text.Json;
using System.Text.Json.Serialization;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Agents;
using Microsoft.SemanticKernel.ChatCompletion;
using Microsoft.SemanticKernel.Connectors.OpenAI;
using ModelContextProtocol.Client;
using ModelContextProtocol.Server;
using OpenAI;

sealed class Release
{
    [JsonPropertyName("version")]
    public required string Version { get; set; }
}

sealed class ReleasesResponse
{
    [JsonPropertyName("releases")]
    public required List<Release> Releases { get; set; }
}

[McpServerToolType]
sealed class ElasticsearchPlugin
{
    [KernelFunction("get_latest_elasticsearch_version")]
    [McpServerTool(Name = "get_latest_elasticsearch_version")]
    [Description("Returns the latest GA version of Elasticsearch in \"X.Y.Z\" format.")]
    public string GetLatestVersion(
        [Description("Major version to filter by (e.g. 7, 8). Defaults to latest")] int? majorVersion = null)
    {
        using var httpClient = new HttpClient();
        var response = httpClient.GetAsync("https://artifacts.elastic.co/releases/stack.json").Result;
        var json = response.Content.ReadAsStringAsync().Result;
        var releaseData = JsonSerializer.Deserialize<ReleasesResponse>(json);

        var query = releaseData?.Releases
            // Filter out non-release versions (e.g. -rc1) and remove " GA" suffix
            .Select(r => r.Version.Replace(" GA", ""))
            .Where(v => !string.IsNullOrEmpty(v) && !v.Contains('-') && Version.TryParse(v, out _))
            .Select(v => Version.Parse(v));

        if (majorVersion.HasValue)
        {
            query = query?.Where(v => v.Major == majorVersion.Value) ?? [];
        }

        return query?.Max()?.ToString() ?? throw new Exception("No valid versions found.");
    }
}

class Program
{

    [Experimental("SKEXP0001")]
    static async Task Main()
    {
        var source = new ActivitySource("ElasticsearchVersionAgent");
        if (Environment.GetCommandLineArgs().Contains("--mcp-server"))
        {
            using var activity = source.StartActivity(name: "mcp-server");
            await Mcp.ServerMain<ElasticsearchPlugin>();
        } else if (Environment.GetCommandLineArgs().Any(arg => arg.StartsWith("--mcp")))
        {
            using var activity = source.StartActivity(name: "agent-mcp");
            await Mcp.ClientMain<ElasticsearchPlugin>(RunAgent);
        }
        else
        {
            using var activity = source.StartActivity(name: "agent");
            await RunAgent(KernelPluginFactory.CreateFromType<ElasticsearchPlugin>());
        }
    }

    static async Task RunAgent(KernelPlugin plugin)
    {
        var kernelBuilder = Kernel.CreateBuilder();
        var azureApiKey = Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY");
        if (azureApiKey != null) {
            var endpoint = Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT")!;
            var deployment = Environment.GetEnvironmentVariable("CHAT_MODEL")!;
            kernelBuilder.AddAzureOpenAIChatCompletion(deployment, endpoint, azureApiKey);
        } else {
            var apiKey = Environment.GetEnvironmentVariable("OPENAI_API_KEY") ?? "your-api-key";
            var model = Environment.GetEnvironmentVariable("CHAT_MODEL") ?? "gpt-4o-mini";
            var baseUrl = Environment.GetEnvironmentVariable("OPENAI_BASE_URL");
            OpenAIClientOptions? options = null;
            if (baseUrl != null) {
                options = new OpenAIClientOptions { Endpoint = new Uri(baseUrl) };
            }
            var openAIClient = new OpenAIClient(new ApiKeyCredential(apiKey), options);
            kernelBuilder.AddOpenAIChatCompletion(model, openAIClient);
        }
        var kernel = kernelBuilder.Build();

        kernel.Plugins.Add(plugin);

        ChatCompletionAgent agent = new()
        {
            Name = "version-agent",
            Kernel = kernel,
            Arguments = new KernelArguments(new OpenAIPromptExecutionSettings()
            {
                FunctionChoiceBehavior = FunctionChoiceBehavior.Auto(),
                Temperature = 0
            }),
        };


        var chatHistory = new ChatHistory();
        chatHistory.AddUserMessage("What is the latest version of Elasticsearch 8?");

        AgentThread? thread = null;
        await foreach (ChatMessageContent response in agent.InvokeAsync(chatHistory, thread))
        {
            Console.WriteLine(response.Content);
        }
    }
}

internal static class Mcp
{
    internal static async Task ServerMain<TKPlugin>() where TKPlugin : class, new()
    {
        var builder = Host.CreateApplicationBuilder();
        builder.Services.AddMcpServer()
            .WithStdioServerTransport()
            .WithTools<TKPlugin>();
        await builder.Build().RunAsync();
    }

    [Experimental("SKEXP0001")]
    internal static async Task ClientMain<TKPlugin>(Func<KernelPlugin, Task> pluginCallback) where TKPlugin : class, new()
    {
        var realPlugin = KernelPluginFactory.CreateFromType<TKPlugin>();
        var options = new StdioClientTransportOptions()
        {
            Name = realPlugin.Name,
            Command = Process.GetCurrentProcess().MainModule?.FileName ?? "dotnet",
            WorkingDirectory = Environment.CurrentDirectory,
            Arguments = Environment.GetCommandLineArgs().Concat(["--mcp-server"]).ToArray(),
        };

        await using IMcpClient mcpClient = await McpClientFactory.CreateAsync(new StdioClientTransport(options));
        var tools = await mcpClient.ListToolsAsync();
        var plugin = KernelPluginFactory.CreateFromFunctions(realPlugin.Name, tools.Select(aiFunction => aiFunction.AsKernelFunction()));
        await pluginCallback(plugin);
    }
}
