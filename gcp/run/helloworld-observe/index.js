const otel = require('@opentelemetry/api');
const tracer = otel.trace.getTracer('hello-world');

const express = require('express');
const app = express();

app.get('/', (req, res) => {
    tracer.startActiveSpan('hi', (span) => {
        console.log('hello');
        span.end();
      });
      res.send(
        `<div style="text-align: center;">
        <h1 style="color: #005A9E; font-family:'Verdana'">
        Hello Elastic Observability - Google Cloud Run - Node.js
        </h1>
        <img src="https://storage.googleapis.com/elastic-helloworld/elastic-logo.png">
        </div>`
        );
      tracer.startActiveSpan('bye', (span) => {
        console.log('goodbye');
        span.end();
      });
});

const port = parseInt(process.env.PORT) || 8080;
app.listen(port, () => {
  console.log(`helloworld: listening on port ${port}`);
});
