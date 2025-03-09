using System;
using System.ClientModel; // for ApiKeyCredential
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Net.Http;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Threading.Tasks;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Agents;
using Microsoft.SemanticKernel.ChatCompletion;
using Microsoft.SemanticKernel.Connectors.OpenAI;
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

sealed class ElasticsearchPlugin
{
    [KernelFunction("get_latest_version")]
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
            ?.Select(r => r.Version?.Replace(" GA", ""))
            .Where(v => v != null && !v.Contains('-') && Version.TryParse(v, out var _));

        if (majorVersion.HasValue)
        {
            query = query.Where(v => Version.Parse(v).Major == majorVersion.Value);
        }

        return query
            // "8.9.1" > "8.10.0", so coerce to System.Version for proper comparison
            .Select(v => Version.Parse(v))
            .Max()
            ?.ToString() ?? throw new Exception("No valid versions found.");
    }
}

class Program
{
    static async Task Main()
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

        kernel.Plugins.AddFromType<ElasticsearchPlugin>("Elasticsearch");

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

        await foreach (ChatMessageContent response in agent.InvokeAsync(chatHistory))
        {
            Console.WriteLine(response.Content);
        }
    }
}
