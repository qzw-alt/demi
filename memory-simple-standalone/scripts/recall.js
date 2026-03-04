/**
 * Memory Recall Module
 * Retrieves relevant memories based on query
 */

const path = require('path');
const {
  loadConfig,
  cosineSimilarity,
  keywordMatch,
  readGlobalMemories,
  readSessionMemories,
  calculateRecencyScore,
  combineScores
} = require('./utils');

const { getEmbedding } = require('./embedder');

// Search memories using vector similarity + keyword matching
async function searchMemories(query, options = {}) {
  const config = loadConfig();
  
  if (!config || !config.recall.enabled) {
    console.log('Memory recall is disabled');
    return [];
  }
  
  const {
    topK = config.recall.topK,
    minSimilarity = config.recall.minSimilarity,
    sessionId = null,
    includeGlobal = true
  } = options;
  
  console.log(`🔍 Searching memories for: "${query.substring(0, 50)}..."`);
  
  try {
    // Get query embedding
    const queryEmbedding = await getEmbedding(query);
    
    // Collect all memories
    let allMemories = [];
    
    // Add global memories
    if (includeGlobal) {
      const globalData = readGlobalMemories(
        path.join(__dirname, '..', config.storage.globalMemoryPath)
      );
      allMemories = allMemories.concat(globalData.memories.map(m => ({
        ...m,
        scope: 'global'
      })));
    }
    
    // Add session memories
    if (sessionId) {
      const sessionData = readSessionMemories(
        path.join(__dirname, '..', config.storage.sessionMemoryPath, `${sessionId}.json`)
      );
      allMemories = allMemories.concat(sessionData.memories.map(m => ({
        ...m,
        scope: 'session'
      })));
    }
    
    if (allMemories.length === 0) {
      console.log('No memories found');
      return [];
    }
    
    console.log(`Searching through ${allMemories.length} memories...`);
    
    // Score each memory
    const scoredMemories = allMemories.map(memory => {
      // Vector similarity
      let vectorScore = 0;
      if (memory.embedding && queryEmbedding) {
        vectorScore = cosineSimilarity(memory.embedding, queryEmbedding);
      }
      
      // Keyword match score
      const keywordScore = keywordMatch(memory.content, query.split(' '));
      
      // Combined similarity (70% vector, 30% keyword)
      const similarityScore = (vectorScore * 0.7) + (keywordScore * 0.3);
      
      // Recency score
      const recencyScore = calculateRecencyScore(memory.timestamp, 30);
      
      // Final combined score
      const finalScore = combineScores(
        similarityScore,
        recencyScore,
        config.recall.similarityWeight,
        config.recall.recencyWeight
      );
      
      return {
        ...memory,
        similarityScore,
        recencyScore,
        finalScore
      };
    });
    
    // Filter by minimum similarity
    const filteredMemories = scoredMemories.filter(m => m.similarityScore >= minSimilarity);
    
    // Sort by final score (descending)
    filteredMemories.sort((a, b) => b.finalScore - a.finalScore);
    
    // Return top K
    const results = filteredMemories.slice(0, topK);
    
    console.log(`✅ Found ${results.length} relevant memories`);
    
    // Clean up results (remove embedding to reduce size)
    return results.map(m => ({
      id: m.id,
      content: m.content,
      type: m.type,
      source: m.source,
      timestamp: m.timestamp,
      scope: m.scope,
      score: {
        similarity: Math.round(m.similarityScore * 100) / 100,
        recency: Math.round(m.recencyScore * 100) / 100,
        final: Math.round(m.finalScore * 100) / 100
      }
    }));
    
  } catch (error) {
    console.error('Failed to search memories:', error.message);
    return [];
  }
}

// Get recent memories (for session context)
function getRecentMemories(limit = 5, sessionId = null) {
  const config = loadConfig();
  
  let allMemories = [];
  
  // Add global memories
  const globalData = readGlobalMemories(
    path.join(__dirname, '..', config.storage.globalMemoryPath)
  );
  allMemories = allMemories.concat(globalData.memories);
  
  // Add session memories
  if (sessionId) {
    const sessionData = readSessionMemories(
      path.join(__dirname, '..', config.storage.sessionMemoryPath, `${sessionId}.json`)
    );
    allMemories = allMemories.concat(sessionData.memories);
  }
  
  // Sort by timestamp (newest first)
  allMemories.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
  
  // Return most recent
  return allMemories.slice(0, limit).map(m => ({
    id: m.id,
    content: m.content,
    type: m.type,
    timestamp: m.timestamp
  }));
}

// Format memories for injection into context
function formatMemoriesForContext(memories) {
  if (!memories || memories.length === 0) {
    return '';
  }
  
  let formatted = '\n\n[Relevant Memories]\n';
  formatted += 'The following information may be relevant to the conversation:\n\n';
  
  for (let i = 0; i < memories.length; i++) {
    const m = memories[i];
    formatted += `${i + 1}. [${m.type}] ${m.content}\n`;
  }
  
  formatted += '\n';
  return formatted;
}

// Export functions
module.exports = {
  searchMemories,
  getRecentMemories,
  formatMemoriesForContext
};

// CLI usage
if (require.main === module) {
  const query = process.argv[2] || '用户喜欢什么';
  
  searchMemories(query, { topK: 5 })
    .then(results => {
      console.log('\nSearch Results:');
      console.log(JSON.stringify(results, null, 2));
      process.exit(0);
    })
    .catch(error => {
      console.error('Search failed:', error);
      process.exit(1);
    });
}
