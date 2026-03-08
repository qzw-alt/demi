/**
 * Memory Capture Module
 * Automatically captures and stores memories from conversations
 */

const path = require('path');
const {
  loadConfig,
  generateId,
  getTimestamp,
  shouldFilter,
  containsCaptureKeywords,
  readGlobalMemories,
  writeGlobalMemories,
  readSessionMemories,
  writeSessionMemories,
  cleanupOldMemories
} = require('./utils');

const { getEmbedding } = require('./embedder');

// Extract potential memories from conversation
function extractMemories(conversation, config) {
  const memories = [];
  
  if (!conversation || !Array.isArray(conversation)) {
    return memories;
  }
  
  const captureConfig = config.capture;
  const noiseFilter = config.noiseFilter;
  
  for (const message of conversation) {
    if (!message.content || message.role !== 'user') {
      continue;
    }
    
    const content = message.content.trim();
    
    // Check length constraints
    if (content.length < captureConfig.minContentLength ||
        content.length > captureConfig.maxContentLength) {
      continue;
    }
    
    // Apply noise filter
    if (shouldFilter(content, noiseFilter)) {
      continue;
    }
    
    // Check if contains capture keywords
    if (!containsCaptureKeywords(content, captureConfig.keywords)) {
      continue;
    }
    
    // Determine memory type based on content
    let type = 'general';
    if (content.includes('喜欢') || content.includes('love') || content.includes('prefer')) {
      type = 'preference';
    } else if (content.includes('讨厌') || content.includes('hate')) {
      type = 'preference';
    } else if (content.includes('决定') || content.includes('decide') || content.includes('选择')) {
      type = 'decision';
    } else if (content.includes('重要') || content.includes('important')) {
      type = 'important';
    }
    
    memories.push({
      id: generateId(),
      content: content,
      type: type,
      source: 'conversation',
      timestamp: getTimestamp(),
      context: message.context || {}
    });
  }
  
  return memories;
}

// Store a single memory
async function storeMemory(memory, storagePath, isGlobal = true) {
  try {
    // Get embedding
    console.log(`Getting embedding for: ${memory.content.substring(0, 50)}...`);
    const embedding = await getEmbedding(memory.content);
    memory.embedding = embedding;
    
    // Read existing memories
    let data;
    if (isGlobal) {
      data = readGlobalMemories(storagePath);
    } else {
      data = readSessionMemories(storagePath);
    }
    
    // Check for duplicates (simple content similarity)
    const isDuplicate = data.memories.some(m => 
      m.content.toLowerCase() === memory.content.toLowerCase()
    );
    
    if (isDuplicate) {
      console.log('Duplicate memory detected, skipping...');
      return false;
    }
    
    // Add new memory
    data.memories.push(memory);
    
    // Cleanup if needed
    const config = loadConfig();
    if (config.storage.autoCleanup) {
      cleanupOldMemories(data, config.storage.maxMemories);
    }
    
    // Write back
    if (isGlobal) {
      writeGlobalMemories(storagePath, data);
    } else {
      writeSessionMemories(storagePath, data);
    }
    
    console.log(`✅ Memory stored: ${memory.id}`);
    return true;
    
  } catch (error) {
    console.error('Failed to store memory:', error.message);
    return false;
  }
}

// Capture memories from conversation
async function captureMemories(conversation, sessionId = null) {
  const config = loadConfig();
  
  if (!config || !config.capture.enabled) {
    console.log('Memory capture is disabled');
    return [];
  }
  
  console.log('🔍 Extracting memories from conversation...');
  const memories = extractMemories(conversation, config);
  
  if (memories.length === 0) {
    console.log('No memories to capture');
    return [];
  }
  
  console.log(`Found ${memories.length} potential memories`);
  
  const storedMemories = [];
  
  // Store in global memory
  for (const memory of memories) {
    const success = await storeMemory(
      memory,
      path.join(__dirname, '..', config.storage.globalMemoryPath),
      true
    );
    
    if (success) {
      storedMemories.push(memory);
    }
  }
  
  // Store in session memory if sessionId provided
  if (sessionId) {
    for (const memory of memories) {
      await storeMemory(
        memory,
        path.join(__dirname, '..', config.storage.sessionMemoryPath, `${sessionId}.json`),
        false
      );
    }
  }
  
  console.log(`✅ Captured ${storedMemories.length} memories`);
  return storedMemories;
}

// Manual memory store (for tool use)
async function manualStore(content, type = 'general', metadata = {}) {
  const config = loadConfig();
  
  const memory = {
    id: generateId(),
    content: content,
    type: type,
    source: metadata.source || 'manual',
    timestamp: getTimestamp(),
    context: metadata.context || {}
  };
  
  const success = await storeMemory(
    memory,
    path.join(__dirname, '..', config.storage.globalMemoryPath),
    true
  );
  
  return success ? memory : null;
}

// Export functions
module.exports = {
  extractMemories,
  storeMemory,
  captureMemories,
  manualStore
};

// CLI usage
if (require.main === module) {
  // Test capture
  const testConversation = [
    { role: 'user', content: '我喜欢喝咖啡，每天早上都要喝一杯' },
    { role: 'assistant', content: '好的，我记住了你喜欢喝咖啡' },
    { role: 'user', content: '记住我的邮箱是 user@example.com' }
  ];
  
  captureMemories(testConversation, 'test-session')
    .then(memories => {
      console.log('Test complete:', memories.length, 'memories captured');
      process.exit(0);
    })
    .catch(error => {
      console.error('Test failed:', error);
      process.exit(1);
    });
}
