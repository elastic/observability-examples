package example;

import io.opentelemetry.api.GlobalOpenTelemetry;
import io.opentelemetry.api.OpenTelemetry;
import org.springframework.ai.model.SpringAIModelProperties;
import org.springframework.ai.model.SpringAIModels;
import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.ai.tool.method.MethodToolCallbackProvider;
import org.springframework.boot.SpringBootConfiguration;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Import;

import java.util.Arrays;

/**
 * Runs {@linkplain VersionAgent} with {@linkplain ElasticsearchTools}.
 */
@SpringBootConfiguration
@EnableAutoConfiguration
@Import({VersionAgent.class, ElasticsearchTools.class})
class Main {
    // Use javaagent instead of spring for configuring OpenTelemetry
    @Bean
    OpenTelemetry openTelemetry() {
        return GlobalOpenTelemetry.get();
    }

    @Bean
    public ToolCallbackProvider elasticsearchToolCallbackProvider(ElasticsearchTools elasticsearchTools) {
        return MethodToolCallbackProvider.builder().toolObjects(elasticsearchTools).build();
    }


    public static void main(String[] args) {
        // We use a common entrypoint so that we can launch with the same args
        // regardless of if this is a client or server. If we didn't, we would
        // need to search through the args and replace McpClientAgent with
        // McpServer.
        if (Arrays.asList(args).contains("--mcp-server")) {
            McpServer.main(args);
        } else if (Arrays.asList(args).contains("--mcp")) {
            McpClientAgent.main(args);
        } else {
            run(Main.class, args,
                    "spring.ai.mcp.client.enabled=false",
                    "spring.ai.mcp.server.enabled=false"
            );
        }
    }

    static void run(Class<?> source, String[] args, String... defaultProperties) {
        // Choose between Azure OpenAI and OpenAI based on the presence of the official SDK
        // environment variable AZURE_OPENAI_API_KEY. Otherwise, we'd create two beans.
        String azureApiKey = System.getenv("AZURE_OPENAI_API_KEY");
        String chatModel = azureApiKey != null && !azureApiKey.trim().isEmpty()
                ? SpringAIModels.AZURE_OPENAI
                : SpringAIModels.OPENAI;

        String[] properties = Arrays.copyOf(defaultProperties, defaultProperties.length + 1);
        properties[defaultProperties.length] = SpringAIModelProperties.CHAT_MODEL + "=" + chatModel;

        new SpringApplicationBuilder(source)
                .properties(properties)
                .run(args).close();
    }
}
