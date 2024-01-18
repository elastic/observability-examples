const serviceName = process.env.SERVICE_NAME || "node-server-elastic-manual";
const secretToken = process.env.ELASTIC_APM_SECRET_TOKEN;
// error if secret token is not set
if (!secretToken) {
  throw new Error("ELASTIC_APM_SECRET_TOKEN environment variable is not set");
}
const serverUrl = process.env.ELASTIC_APM_SERVER_URL;
// error if server url is not set
if (!serverUrl) {
  throw new Error("ELASTIC_APM_SERVER_URL environment variable is not set");
}
const environment = process.env.ELASTIC_APM_ENVIRONMENT || "dev";


const apm = require('elastic-apm-node').start({
  serviceName: serviceName,
  secretToken: secretToken,
  serverUrl: serverUrl,
  environment: environment,
});
