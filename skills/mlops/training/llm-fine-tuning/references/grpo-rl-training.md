# GRPO/RL Training with TRL

> Absorbed from `grpo-rl-training` skill — use this reference for detailed GRPO/RL fine-tuning guidance.

## When to Use

- Enforcing specific output formats (XML tags, JSON, structured reasoning)
- Verifiable tasks with objective correctness metrics (math, coding, fact-checking)
- Improving reasoning capabilities by rewarding chain-of-thought patterns
- **Do NOT use**: simple SFT, tasks without clear reward signals, when you have high-quality preference pairs (use DPO instead)

## Core Concepts

**Key Mechanism:**
- Generates multiple completions per prompt (group size: 4-16)
- Compares completions within each group using reward functions
- Updates policy to favor higher-rewarded responses relative to the group

**Critical Difference from PPO:**
- No separate reward model needed
- More sample-efficient (within-group comparisons)
- Simpler to implement and debug

## Reward Function Design

**Golden Rules:**
1. Compose multiple reward functions — each handles one aspect (format, correctness, style)
2. Scale rewards appropriately — higher weight = stronger signal
3. Use incremental rewards — partial credit for partial compliance
4. Test rewards independently — debug each function in isolation

| Type | Use Case | Weight |
|------|----------|--------|
| Correctness | Verifiable tasks (math, code) | 2.0 |
| Format | Strict structure enforcement | 0.5-1.0 |
| Length | Verbosity/conciseness | 0.1-0.5 |
| Style | Penalize unwanted patterns | -0.5 to 0.5 |

## Training Insights

### Loss Behavior (EXPECTED PATTERN)
- **Loss starts near 0 and INCREASES during training** — this is CORRECT
- Loss measures KL divergence from initial policy
- Model is learning (diverging from original to optimize rewards)
- Monitor reward metrics instead of loss for progress

### Key Metrics
- `reward`: Average across all completions (should increase)
- `reward_std`: Diversity within groups (should remain > 0.1)
- `kl`: KL divergence from reference (should grow moderately, < 0.5)

### Warning Signs
| Symptom | Problem | Solution |
|---------|---------|----------|
| reward_std → 0 | Mode collapse | Increase `num_generations` |
| KL > 0.5 | Diverging too fast | Reduce learning rate |
| Flat rewards | Reward functions too harsh | Check logic, increase LR |
| OOM | GPU memory exceeded | Reduce batch size, enable gradient checkpointing |

## Quick Template

See `templates/basic_grpo_training.py` for a complete production-ready template.

```python
from trl import GRPOTrainer, GRPOConfig

training_args = GRPOConfig(
    output_dir="outputs/grpo-model",
    learning_rate=5e-6,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    num_generations=8,
    max_prompt_length=256,
    max_completion_length=512,
    bf16=True,
    optim="adamw_8bit",
)
trainer = GRPOTrainer(
    model=model,
    processing_class=tokenizer,
    reward_funcs=[incremental_format_reward, format_reward, correctness_reward],
    args=training_args,
    train_dataset=dataset,
    peft_config=peft_config,
)
trainer.train()
```

## Advanced Patterns

### Multi-Stage Training
```python
# Stage 1: Format compliance
trainer_stage1 = GRPOTrainer(
    model=model, reward_funcs=[incremental_format_reward, format_reward], ...
)
trainer_stage1.train()

# Stage 2: Correctness
trainer_stage2 = GRPOTrainer(
    model=model, reward_funcs=[format_reward, correctness_reward], ...
)
trainer_stage2.train()
```

### Unsloth Integration (2-3× faster)
```python
from unsloth import FastLanguageModel
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="google/gemma-3-1b-it",
    max_seq_length=1024, load_in_4bit=True, fast_inference=True, max_lora_rank=32,
)
model = FastLanguageModel.get_peft_model(model, r=32, ...)
# Rest is identical to standard setup
```
