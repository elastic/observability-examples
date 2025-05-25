package example;

import io.micrometer.tracing.annotation.NewSpan;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.ai.model.tool.DefaultToolCallingChatOptions;
import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.stereotype.Component;

@Component
class VersionAgent implements CommandLineRunner {

    private final ChatClient chat;
    private final ToolCallbackProvider tools;
    private final ConfigurableApplicationContext context;

    VersionAgent(ChatModel chat, ToolCallbackProvider tools, ConfigurableApplicationContext context) {
        this.chat = ChatClient.builder(chat).build();
        this.tools = tools;
        this.context = context;
    }

    @Override
    // Without a root span, we get multiple traces and can't understand the multiple requests being made.
    // Currently, no automatic root span is created for the CommandLineRunner so we do it ourselves.
    // https://github.com/spring-projects/spring-ai/issues/1440
    @NewSpan("version-agent")
    public void run(String... args) {
        String answer = chat.prompt()
                .user("What is the latest version of Elasticsearch 8?")
                .toolCallbacks(tools)
                .options(DefaultToolCallingChatOptions.builder().temperature(0.0).build())
                .call()
                .content();

        System.out.println(answer);
        context.close(); // See https://github.com/spring-projects/spring-ai/issues/2756
    }
}
