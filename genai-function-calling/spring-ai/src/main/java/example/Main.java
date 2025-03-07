package example;

import io.micrometer.tracing.annotation.NewSpan;
import io.opentelemetry.api.OpenTelemetry;
import io.opentelemetry.api.GlobalOpenTelemetry;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.ai.model.tool.DefaultToolCallingChatOptions;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.stereotype.Component;

@SpringBootApplication
public class Main {

	@Component
    static class VersionAgent implements CommandLineRunner {

		private final ChatClient chat;
		private final ElasticsearchTools tools;

        VersionAgent(ChatModel chat, ElasticsearchTools tools) {
			this.chat = ChatClient.builder(chat).build();
			this.tools = tools;
		}

		@Override
		// Without a root span, we get multiple traces and can't understand the multiple requests being made.
		// Currently, no automatic root span is created for the CommandLineRunner so we do it ourselves.
		// https://github.com/spring-projects/spring-ai/issues/1440
		@NewSpan("version-agent")
		public void run(String... args) {
			String answer = chat.prompt()
					.user("What is the latest version of Elasticsearch 8?")
					.tools(tools)
					.options(DefaultToolCallingChatOptions.builder().temperature(0.0).build())
					.call()
					.content();

			System.out.println(answer);
		}
	}

	// Use javaagent instead of spring for configuring OpenTelemetry
	@Bean
	OpenTelemetry openTelemetry() {
		return GlobalOpenTelemetry.get();
	}

	public static void main(String[] args) {
		SpringApplication.run(Main.class, args);
	}

}
