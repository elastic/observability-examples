package example;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import io.opentelemetry.api.GlobalOpenTelemetry;
import io.opentelemetry.api.OpenTelemetry;
import org.springframework.ai.mcp.client.autoconfigure.properties.McpStdioClientProperties;
import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.ai.tool.method.MethodToolCallbackProvider;
import org.springframework.boot.SpringBootConfiguration;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Import;
import org.springframework.context.annotation.Primary;
import org.springframework.core.io.ByteArrayResource;

import java.nio.charset.StandardCharsets;

/**
 * Launches {@linkplain McpServer} in a subprocess and runs
 * {@linkplain VersionAgent} with its tools via MCP stdio client.
 */
@SpringBootConfiguration
@EnableAutoConfiguration
@Import(VersionAgent.class)
class McpClientAgent {
    // Use javaagent instead of spring for configuring OpenTelemetry
    @Bean
    OpenTelemetry openTelemetry() {
        return GlobalOpenTelemetry.get();
    }

    /**
     * Generates MCP server configuration in <a href="https://modelcontextprotocol.io/quickstart/user">Claude Desktop Format</a>.
     * <p/>
     * Notably, this takes the existing process command, args, and env, and
     * appends "--mcp-server" to the args. Since this process was launched via
     * {@linkplain Main#main(String[])}, the additional arg will route the MCP
     * server subprocess correctly to {@linkplain McpServer}.
     */
    String mcpServersConfiguration() throws Exception {
        ObjectMapper mapper = new ObjectMapper();
        ObjectNode root = mapper.createObjectNode();
        ObjectNode serverConfig = mapper.createObjectNode();

        // Set up the configuration structure
        root.set("mcpServers", mapper.createObjectNode().set("elasticsearch-versions", serverConfig));

        // Get process information
        ProcessHandle.Info info = ProcessHandle.current().info();

        // Add command
        serverConfig.put("command",
                info.command().orElseThrow(() -> new IllegalStateException("Cannot get command of current process")));

        // Add arguments with "--mcp-server" appended
        ArrayNode argsNode = mapper.createArrayNode();
        String[] args = info.arguments().orElseThrow(() -> new IllegalStateException("Cannot get arguments of current process"));
        for (String arg : args) {
            argsNode.add(arg);
        }
        argsNode.add("--mcp-server");
        serverConfig.set("args", argsNode);

        // Add environment variables
        serverConfig.set("env", mapper.valueToTree(System.getenv()));

        // Serialize to pretty-printed JSON
        return mapper.writerWithDefaultPrettyPrinter().writeValueAsString(root);
    }

    /**
     * Overrides {@link McpStdioClientProperties} defined by properties with
     * dynamic values, notably that derive MCP server launch configuration from
     * the current process.
     */
    @Bean
    @Primary
    McpStdioClientProperties stdioClientProperties() throws Exception {
        String mcpServersConfiguration = mcpServersConfiguration();

        McpStdioClientProperties properties = new McpStdioClientProperties();
        properties.setServersConfiguration(new ByteArrayResource(mcpServersConfiguration.getBytes(StandardCharsets.UTF_8)));
        return properties;
    }


    static void main(String[] args) {
        Main.run(McpClientAgent.class, args,
                "spring.ai.mcp.client.enabled=true",
                "spring.ai.mcp.client.toolcallback.enabled=true",
                "spring.ai.mcp.server.enabled=false"
        );
    }
}

/**
 * Starts an MCP server and registers {@linkplain ElasticsearchTools},
 * listening on stdin/stdout.
 */
@SpringBootConfiguration
@EnableAutoConfiguration
@Import(ElasticsearchTools.class)
class McpServer {
    // Use javaagent instead of spring for configuring OpenTelemetry
    @Bean
    OpenTelemetry openTelemetry() {
        return GlobalOpenTelemetry.get();
    }

    @Bean
    public ToolCallbackProvider elasticsearchToolCallbackProvider(ElasticsearchTools elasticsearchTools) {
        return MethodToolCallbackProvider.builder().toolObjects(elasticsearchTools).build();
    }

    static void main(String[] args) {
        Main.run(McpServer.class, args,
                "spring.ai.mcp.client.enabled=false",
                "spring.ai.mcp.server.stdio=true"
        );
    }
}
