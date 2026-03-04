/**
 * memory-simple 使用示例
 * 展示如何在实际项目中使用记忆系统
 */

const { captureMemories, manualStore } = require('../memory-simple/scripts/capture');
const { searchMemories, getRecentMemories, formatMemoriesForContext } = require('../memory-simple/scripts/recall');

// ============ 示例 1: 自动捕获对话记忆 ============
async function example1_autoCapture() {
  console.log('\n📝 示例 1: 自动捕获对话记忆\n');
  
  const conversation = [
    { role: 'user', content: '你好' },
    { role: 'assistant', content: '你好！有什么可以帮助你的？' },
    { role: 'user', content: '我喜欢喝美式咖啡，不加糖' },
    { role: 'assistant', content: '好的，我记住了你喜欢喝美式咖啡不加糖' },
    { role: 'user', content: '记住我的邮箱是 user@example.com' },
    { role: 'user', content: '我决定选择方案A' }
  ];
  
  const memories = await captureMemories(conversation, 'example-session-1');
  console.log(`✅ 捕获了 ${memories.length} 条记忆`);
  memories.forEach(m => console.log(`  - [${m.type}] ${m.content.substring(0, 50)}...`));
}

// ============ 示例 2: 手动存储记忆 ============
async function example2_manualStore() {
  console.log('\n📝 示例 2: 手动存储记忆\n');
  
  // 存储用户偏好
  await manualStore('用户喜欢蓝色', 'preference', { source: 'manual' });
  console.log('✅ 存储偏好: 用户喜欢蓝色');
  
  // 存储重要决定
  await manualStore('用户决定使用 React 框架', 'decision', { source: 'manual' });
  console.log('✅ 存储决定: 使用 React 框架');
  
  // 存储重要信息
  await manualStore('项目截止时间是 2026-03-15', 'important', { source: 'manual' });
  console.log('✅ 存储重要信息: 项目截止时间');
}

// ============ 示例 3: 检索记忆 ============
async function example3_search() {
  console.log('\n📝 示例 3: 检索记忆\n');
  
  // 基本检索
  console.log('🔍 查询: "用户喜欢什么"');
  const results1 = await searchMemories('用户喜欢什么', { topK: 3 });
  console.log(`找到 ${results1.length} 条结果:`);
  results1.forEach((r, i) => {
    console.log(`  ${i + 1}. [${r.type}] ${r.content.substring(0, 40)}... (相似度: ${r.score.similarity})`);
  });
  
  // 带会话的检索
  console.log('\n🔍 查询: "用户决定" (包含会话记忆)');
  const results2 = await searchMemories('用户决定', {
    topK: 3,
    sessionId: 'example-session-1'
  });
  console.log(`找到 ${results2.length} 条结果`);
}

// ============ 示例 4: 获取最近记忆 ============
async function example4_recent() {
  console.log('\n📝 示例 4: 获取最近记忆\n');
  
  const recent = getRecentMemories(5);
  console.log(`最近 ${recent.length} 条记忆:`);
  recent.forEach((m, i) => {
    console.log(`  ${i + 1}. [${m.type}] ${m.content.substring(0, 40)}...`);
  });
}

// ============ 示例 5: 格式化上下文 ============
async function example5_format() {
  console.log('\n📝 示例 5: 格式化上下文\n');
  
  const memories = await searchMemories('用户偏好', { topK: 3 });
  const context = formatMemoriesForContext(memories);
  
  console.log('格式化后的上下文:');
  console.log(context);
  
  // 实际使用时，将这个 context 加入 LLM 提示词
  console.log('💡 提示: 可以将这个 context 加入 LLM 的系统提示词中');
}

// ============ 示例 6: 完整对话流程 ============
async function example6_fullFlow() {
  console.log('\n📝 示例 6: 完整对话流程\n');
  
  // 模拟对话
  const conversation = [
    { role: 'user', content: '我叫张三' },
    { role: 'user', content: '我喜欢编程，特别是 JavaScript' },
    { role: 'user', content: '我在北京工作' }
  ];
  
  // 1. 对话结束时捕获记忆
  console.log('1️⃣ 捕获对话记忆...');
  await captureMemories(conversation, 'zhangsan-session');
  
  // 2. 用户新提问时检索记忆
  console.log('2️⃣ 用户提问: "我应该学习什么编程语言？"');
  const query = '用户应该学习什么编程语言';
  const memories = await searchMemories(query, { topK: 3 });
  
  // 3. 格式化上下文
  console.log('3️⃣ 检索相关记忆...');
  const context = formatMemoriesForContext(memories);
  console.log(context);
  
  // 4. 构建完整提示词
  console.log('4️⃣ 构建 LLM 提示词:');
  const prompt = `
${context}
用户问题: 我应该学习什么编程语言？

请根据用户的背景和偏好给出建议。
`;
  console.log(prompt);
}

// ============ 运行所有示例 ============
async function runAllExamples() {
  console.log('🚀 memory-simple 使用示例\n');
  console.log('=' .repeat(50));
  
  try {
    await example1_autoCapture();
    await example2_manualStore();
    await example3_search();
    await example4_recent();
    await example5_format();
    await example6_fullFlow();
    
    console.log('\n' + '='.repeat(50));
    console.log('✅ 所有示例运行完成!');
  } catch (error) {
    console.error('❌ 示例运行失败:', error.message);
  }
}

// 如果直接运行此文件
if (require.main === module) {
  runAllExamples();
}

// 导出示例函数
module.exports = {
  example1_autoCapture,
  example2_manualStore,
  example3_search,
  example4_recent,
  example5_format,
  example6_fullFlow,
  runAllExamples
};
