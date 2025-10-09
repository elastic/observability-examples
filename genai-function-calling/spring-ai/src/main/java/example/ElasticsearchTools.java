package example;

import jakarta.annotation.Nullable;
import org.springframework.ai.tool.annotation.Tool;
import org.springframework.ai.tool.annotation.ToolParam;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;

import java.util.Comparator;
import java.util.List;


@Component
class ElasticsearchTools {
    record Release(String version, String public_release_date) {
    }

    record ReleasesResponse(List<Release> releases) {
    }

    @Tool(description = "Returns the latest GA version of Elasticsearch in \"X.Y.Z\" format.")
    String getLatestElasticsearchVersion(@ToolParam(description = "Major version to filter by (e.g. 8, 9). Defaults to latest") @Nullable Integer majorVersion) {
        ReleasesResponse response = WebClient.create().get().uri("https://artifacts.elastic.co/releases/stack.json")
                .exchangeToMono(res -> res.mutate()
                        // Fix incorrect content-type from artifacts.elastic.co
                        .headers(hdrs -> hdrs.setContentType(MediaType.APPLICATION_JSON))
                        .build()
                        .bodyToMono(ReleasesResponse.class))
                .block();
        return response.releases().stream()
                // Filter out non-release versions (e.g. -rc1) and remove " GA" suffix
                .map(release -> release.version().replace(" GA", ""))
                .filter(version -> !version.contains("-"))
                .filter(version -> {
                    if (majorVersion == null) {
                        return true;
                    }
                    return version.startsWith(majorVersion + ".");
                })
                // "8.9.1" > "8.10.0", so coerce to an integer: 80901 < 81000
                .max(Comparator.comparingInt(v -> {
                    String[] parts = v.split("\\.");
                    return Integer.parseInt(parts[0]) * 10000 +
                            Integer.parseInt(parts[1]) * 100 +
                            Integer.parseInt(parts[2]);
                }))
                .orElseThrow();
    }
}
