const https = require('https');
const querystring = require('querystring');

// Salesforce Configuration
const SF_CLIENT_ID = process.env.SALESFORCE_CLIENT_ID;
const SF_CLIENT_SECRET = process.env.SALESFORCE_CLIENT_SECRET;
const SF_DOMAIN = process.env.SALESFORCE_DOMAIN;

// Hubspot Configuration
const HUBSPOT_ACCESS_TOKEN = process.env.HUBSPOT_ACCESS_TOKEN;

// Generic HTTPS Request Function
async function request(options, body) {
  return new Promise((resolve, reject) => {
    const req = https.request(options, res => {
      let data = '';
      res.on('data', d => data += d);
      res.on('end', () => {
        try {
          if (res.statusCode >= 400) {
            reject(new Error(`HTTP Error ${res.statusCode}: ${data}`));
          } else {
            resolve({ status: res.statusCode, body: JSON.parse(data) });
          }
        }
        catch(e) { resolve({ status: res.statusCode, body: data }); }
      });
    });
    req.on('error', reject);
    if (body) req.write(body);
    req.end();
  });
}

// Salesforce Functions
async function getSfToken() {
  const body = querystring.stringify({
    grant_type: 'client_credentials',
    client_id: SF_CLIENT_ID,
    client_secret: SF_CLIENT_SECRET
  });
  const res = await request({
    hostname: SF_DOMAIN,
    path: '/services/oauth2/token',
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Content-Length': Buffer.byteLength(body)
    }
  }, body);
  if (!res.body.access_token) throw new Error('Salesforce auth failed: ' + JSON.stringify(res.body));
  return { token: res.body.access_token, instanceUrl: res.body.instance_url };
}

async function sfQuery(instanceUrl, token, query) {
    const url = new URL(instanceUrl);
    const path = `/services/data/v59.0/query/?q=${encodeURIComponent(query)}`;
    const res = await request({
      hostname: url.hostname,
      path: path,
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Accept': 'application/json'
      }
    });
    return res.body;
}

// Hubspot Functions
async function getHubspotAnalytics() {
    const sevenDaysAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);
    const startDate = `${sevenDaysAgo.getFullYear()}${(sevenDaysAgo.getMonth()+1).toString().padStart(2, '0')}${sevenDaysAgo.getDate().toString().padStart(2, '0')}`;
    const endDate = `${new Date().getFullYear()}${(new Date().getMonth()+1).toString().padStart(2, '0')}${new Date().getDate().toString().padStart(2, '0')}`;
    
    return request({
        hostname: 'api.hubapi.com',
        path: `/analytics/v2/reports/sources/total?start=${startDate}&end=${endDate}`,
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${HUBSPOT_ACCESS_TOKEN}`,
            'Accept': 'application/json'
        }
    });
}

async function run() {
    let summary = 'Marketing Dashboard Data Pull Summary:\\n\\n';
    
    summary += '--- Salesforce Data ---\\n';
    try {
        const { token, instanceUrl } = await getSfToken();
        const sevenDaysAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString();

        const leadQuery = `SELECT COUNT() FROM Lead WHERE CreatedDate >= ${sevenDaysAgo}`;
        const opportunityQuery = `SELECT COUNT() FROM Opportunity WHERE CreatedDate >= ${sevenDaysAgo}`;

        const leadResult = await sfQuery(instanceUrl, token, leadQuery);
        const opportunityResult = await sfQuery(instanceUrl, token, opportunityQuery);

        summary += `New Leads (last 7 days): ${leadResult.totalSize}\\n`;
        summary += `New Opportunities (last 7 days): ${opportunityResult.totalSize}\\n`;
    } catch (e) {
        summary += `Error fetching Salesforce data: ${e.message}\\n`;
    }

    summary += '\\n--- Hubspot Data ---\\n';
    try {
        const hubspotResult = await getHubspotAnalytics();
        const analytics = hubspotResult.body.totals;
        summary += `Website Visits (last 7 days): ${analytics.visits}\\n`;
        summary += `New Contacts (last 7 days): ${analytics.contacts}\\n`;
        summary += `New Leads (last 7 days): ${analytics.leads}\\n`;
    } catch (e) {
        summary += `Error fetching Hubspot data: ${e.message}\\n`;
    }
    
    console.log(summary);
}

run();
