var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

string output =
"""
<h1>Hello World!</h1>
""";

app.MapGet("/", async context =>
    { await context.Response.WriteAsync(output); }
);
app.Run();
