/**
 * Embedding Module
 * Handles text embedding using Zhipu AI API
 */

const https = require('https');
const { loadConfig } = require('./utils');

// Get embedding for text
async function getEmbedding(text) {
  const config = loadConfig();
  
  if (!config || !config.embedding) {
    throw new Error('Embedding configuration not found');
  }
  
  const { apiKey, model } = config.embedding;
  
  return new Promise((resolve, reject) => {
    const requestData = JSON.stringify({
      model: model,
      input: text
    });
    
    const options = {
      hostname: 'open.bigmodel.cn',
      path: '/api/paas/v4/embeddings',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
        'Content-Length': Buffer.byteLength(requestData)
      },
      timeout: 10000
    };
    
    const req = https.request(options, (res) => {
      let data = '';
      
      res.on('data', (chunk) => {
        data += chunk;
      });
      
      res.on('end', () => {
        try {
          const response = JSON.parse(data);
          
          if (response.data && response.data[0] && response.data[0].embedding) {
            resolve(response.data[0].embedding);
          } else if (response.error) {
            reject(new Error(`API Error: ${response.error.message}`));
          } else {
            reject(new Error('Invalid response format'));
          }
        } catch (error) {
          reject(new Error(`Failed to parse response: ${error.message}`));
        }
      });
    });
    
    req.on('error', (error) => {
      reject(new Error(`Request failed: ${error.message}`));
    });
    
    req.on('timeout', () => {
      req.destroy();
      reject(new Error('Request timeout'));
    });
    
    req.write(requestData);
    req.end();
  });
}

// Get embeddings for multiple texts (batch)
async function getEmbeddingsBatch(texts) {
  const embeddings = [];
  
  for (const text of texts) {
    try {
      const embedding = await getEmbedding(text);
      embeddings.push(embedding);
    } catch (error) {
      console.error(`Failed to get embedding for: ${text.substring(0, 50)}...`, error.message);
      embeddings.push(null);
    }
  }
  
  return embeddings;
}

// Export functions
module.exports = {
  getEmbedding,
  getEmbeddingsBatch
};
