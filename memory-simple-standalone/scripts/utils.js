/**
 * Memory System Utils
 * Core utility functions for the simple memory system
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// Load configuration
function loadConfig() {
  const configPath = path.join(__dirname, '..', 'config.json');
  try {
    const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    return config;
  } catch (error) {
    console.error('Failed to load config:', error.message);
    return null;
  }
}

// Generate UUID
function generateId() {
  return crypto.randomUUID();
}

// Get current timestamp in ISO format
function getTimestamp() {
  return new Date().toISOString();
}

// Calculate cosine similarity between two vectors
function cosineSimilarity(vecA, vecB) {
  if (!vecA || !vecB || vecA.length !== vecB.length) {
    return 0;
  }
  
  let dotProduct = 0;
  let normA = 0;
  let normB = 0;
  
  for (let i = 0; i < vecA.length; i++) {
    dotProduct += vecA[i] * vecB[i];
    normA += vecA[i] * vecA[i];
    normB += vecB[i] * vecB[i];
  }
  
  if (normA === 0 || normB === 0) {
    return 0;
  }
  
  return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
}

// Simple keyword matching for text search
function keywordMatch(text, keywords) {
  if (!text || !keywords || keywords.length === 0) {
    return 0;
  }
  
  const lowerText = text.toLowerCase();
  let matches = 0;
  
  for (const keyword of keywords) {
    if (lowerText.includes(keyword.toLowerCase())) {
      matches++;
    }
  }
  
  return matches / keywords.length;
}

// Check if content should be filtered (noise filter)
function shouldFilter(content, noiseFilter) {
  if (!noiseFilter || !noiseFilter.enabled) {
    return false;
  }
  
  const lowerContent = content.toLowerCase().trim();
  
  // Check greetings
  for (const greeting of noiseFilter.greetings || []) {
    if (lowerContent === greeting.toLowerCase()) {
      return true;
    }
  }
  
  // Check if it's too short
  if (lowerContent.length < 5) {
    return true;
  }
  
  // Check refusal patterns
  for (const pattern of noiseFilter.refusalPatterns || []) {
    if (lowerContent.includes(pattern.toLowerCase())) {
      return true;
    }
  }
  
  return false;
}

// Check if content contains capture keywords
function containsCaptureKeywords(content, keywords) {
  if (!content || !keywords) {
    return false;
  }
  
  const lowerContent = content.toLowerCase();
  
  for (const keyword of keywords) {
    if (lowerContent.includes(keyword.toLowerCase())) {
      return true;
    }
  }
  
  return false;
}

// Read global memories
function readGlobalMemories(storagePath) {
  try {
    if (fs.existsSync(storagePath)) {
      const data = fs.readFileSync(storagePath, 'utf8');
      return JSON.parse(data);
    }
  } catch (error) {
    console.error('Failed to read global memories:', error.message);
  }
  
  return { memories: [], lastUpdated: getTimestamp() };
}

// Write global memories
function writeGlobalMemories(storagePath, data) {
  try {
    const dir = path.dirname(storagePath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    
    data.lastUpdated = getTimestamp();
    fs.writeFileSync(storagePath, JSON.stringify(data, null, 2), 'utf8');
    return true;
  } catch (error) {
    console.error('Failed to write global memories:', error.message);
    return false;
  }
}

// Read session memories
function readSessionMemories(sessionPath) {
  try {
    if (fs.existsSync(sessionPath)) {
      const data = fs.readFileSync(sessionPath, 'utf8');
      return JSON.parse(data);
    }
  } catch (error) {
    console.error('Failed to read session memories:', error.message);
  }
  
  return { memories: [], sessionId: path.basename(sessionPath, '.json'), createdAt: getTimestamp() };
}

// Write session memories
function writeSessionMemories(sessionPath, data) {
  try {
    const dir = path.dirname(sessionPath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    
    data.lastUpdated = getTimestamp();
    fs.writeFileSync(sessionPath, JSON.stringify(data, null, 2), 'utf8');
    return true;
  } catch (error) {
    console.error('Failed to write session memories:', error.message);
    return false;
  }
}

// Calculate recency score (0-1, newer is higher)
function calculateRecencyScore(timestamp, halfLifeDays = 30) {
  const now = new Date();
  const memoryTime = new Date(timestamp);
  const ageMs = now - memoryTime;
  const ageDays = ageMs / (1000 * 60 * 60 * 24);
  
  // Exponential decay
  return Math.exp(-ageDays / halfLifeDays);
}

// Combine similarity and recency scores
function combineScores(similarity, recency, similarityWeight = 0.7, recencyWeight = 0.3) {
  return (similarity * similarityWeight) + (recency * recencyWeight);
}

// Clean old memories if threshold reached
function cleanupOldMemories(data, maxMemories) {
  if (!data.memories || data.memories.length <= maxMemories) {
    return data;
  }
  
  // Sort by timestamp (newest first)
  data.memories.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
  
  // Keep only maxMemories
  data.memories = data.memories.slice(0, maxMemories);
  
  return data;
}

// Export functions
module.exports = {
  loadConfig,
  generateId,
  getTimestamp,
  cosineSimilarity,
  keywordMatch,
  shouldFilter,
  containsCaptureKeywords,
  readGlobalMemories,
  writeGlobalMemories,
  readSessionMemories,
  writeSessionMemories,
  calculateRecencyScore,
  combineScores,
  cleanupOldMemories
};
