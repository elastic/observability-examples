using System.Diagnostics;
using OpenTelemetry.Resources;
using OpenTelemetry.Trace;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddOpenTelemetry().WithTracing(builder => builder.AddOtlpExporter()
                    .AddSource("helloworld")
                    .AddAspNetCoreInstrumentation()
                    .AddOtlpExporter()  
        .ConfigureResource(resource =>
            resource.AddService(
                serviceName: "helloworld"))
);
builder.Services.AddControllers();
var app = builder.Build();

string output =
"""
<div style="text-align: center;">
<h1 style="color: #005A9E; font-family:'Verdana'">
Hello Elastic Observability - Azure Container Apps - C#
</h1>
<img src="https://elastichelloworld.blob.core.windows.net/elastic-helloworld/elastic-logo.png">
</div>
""";

app.MapGet("/", async context =>
    {   
        using (Activity activity = Telemetry.activitySource.StartActivity("HelloSpan")!)
        {
            Console.Write("hello");
            await context.Response.WriteAsync(output);
        }
    }
);
app.Run();
