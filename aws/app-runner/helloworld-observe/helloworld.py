import logging
from flask import Flask

from opentelemetry import trace
tracer = trace.get_tracer("hello-world")

app = Flask(__name__)

@app.route("/")
def helloworld():
    with tracer.start_as_current_span("hi") as span:
        logging.info("hello")
        return '''
        <div style="text-align: center;">
        <h1 style="color: #005A9E; font-family:'Verdana'">
        Hello Elastic Observability - AWS App Runner - Python
        </h1>
        <img src="https://elastic-helloworld.s3.us-east-2.amazonaws.com/elastic-logo.png">
        </div>
        '''

@app.after_request
def after_request(response):
    with tracer.start_as_current_span("bye"):
        logging.info("goodbye")
        return response
