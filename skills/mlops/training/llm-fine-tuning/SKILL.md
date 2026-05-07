---
name: llm-fine-tuning
description: Unified skill for LLM fine-tuning — covers SFT, GRPO, DPO, PPO, and distributed training (FSDP, LoRA/QLoRA, PEFT). Browse subsections below or use sub-skills directly for targeted workflows.
version: 1.0.0
category: mlops/training
metadata:
  hermes:
    tags: [fine-tuning, LoRA, QLoRA, GRPO, DPO, PPO, TRL, FSDP, PEFT, distributed-training, RLHF]
---

# LLM Fine-Tuning

> **Umbrella skill** — covers all LLM fine-tuning approaches. Sub-skills are still usable directly for targeted workflows.

## Skill Overview

| Sub-Skill | Focus | Use When |
|-----------|-------|----------|
| `grpo-rl-training` | GRPO/RL fine-tuning with TRL | Enforcing output format, reasoning tasks, reward-based training |
| `pytorch-fsdp` | FSDP distributed training | Multi-GPU large model training, parameter sharding |
| `peft-fine-tuning` | LoRA/QLoRA PEFT methods | Memory-efficient fine-tuning on consumer GPUs |
| `unsloth` | Fast LoRA/QLoRA (2-5× faster) | Rapid prototyping, limited VRAM |
| `axolotl` | YAML-based multi-method training | Structured config-driven training pipelines |
| `trl-fine-tuning` | SFT + DPO + PPO with TRL | Standard supervised fine-tuning and preference learning |

## Quick Decision Guide

**What training method should I use?**

```
Is your model already instruction-tuned and you need to:
  → GRPO (grpo-rl-training): Enforce format, improve reasoning, verifiable tasks
  → DPO (trl-fine-tuning): Align to human preferences, no reward model needed

Do you have limited GPU memory (< 24GB)?
  → PEFT/LoRA (peft-fine-tuning or unsloth)

Do you need multi-GPU for a large model?
  → FSDP (pytorch-fsdp)

Is your task simple supervised fine-tuning?
  → SFT (trl-fine-tuning)
```

## Subsections

### [GRPO/RL Training](./grpo-rl-training/)
*Expert guidance for Group Relative Policy Optimization with TRL*

Covers: reward function design, GRPOConfig, multi-reward composition, training insights (loss increases — this is normal), debugging, deployment.

### [PyTorch FSDP](./pytorch-fsdp/)
*Distributed training with Fully Sharded Data Parallel*

Covers: parameter sharding, mixed precision, CPU offloading, FSDP2, Join context manager.

### [PEFT Fine-Tuning](./peft/)
*LoRA/QLoRA parameter-efficient fine-tuning*

Covers: LoRA rank selection, target modules, QLoRA quantization, memory calculations.

### [Unsloth](./unsloth/)
*2-5× faster LoRA/QLoRA training with less VRAM*

Covers: FastLanguageModel, gradient checkpointing, batch size optimization.

### [Axolotl](./axolotl/)
*YAML-driven multi-method training (SFT, DPO, GRPO, etc.)*

Covers: YAML configs, dataset formatting, multi-GPU configs,常见 pitfalls.

### [TRL Fine-Tuning](./trl-fine-tuning/)
*Supervised Fine-Tuning and DPO with Transformer Reinforcement Learning library*

Covers: SFTTrainer, DPOTrainer, PPOTrainer, dataset preparation, training loops.

---

## Common Workflow: GRPO Training

See `grpo-rl-training` sub-skill for the full guide. Quick summary:

1. **Dataset**: prompts as `List[Dict]` with role/content, include ground truth
2. **Reward functions**: compose 3-5 (format + correctness + style)
3. **Config**: `num_generations=8`, `bf16=True`, `optim="adamw_8bit"`
4. **Monitor**: reward metrics, NOT loss (loss INCREASES during training — this is correct)
5. **Save**: `trainer.save_model()` then merge LoRA if using PEFT

### Basic GRPO Template

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
    logging_steps=1,
    save_steps=100,
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

### Key GRPO Insights

- **Loss starts near 0 and INCREASES** — this is correct behavior
- Monitor `reward` (should rise) and `reward_std` (should stay > 0.1)
- If `reward_std → 0`: mode collapse — increase `num_generations`
- If KL > 0.5: diverging too fast — reduce learning rate
- Combine 3-5 reward functions; each handles one aspect

---

## Common Workflow: PEFT/LoRA

See `peft-fine-tuning` sub-skill for the full guide.

```python
from peft import LoraConfig

peft_config = LoraConfig(
    r=16,                          # Rank: higher = more capacity
    lora_alpha=32,                 # Typically 2× r
    target_modules=[
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj"
    ],
    task_type="CAUSAL_LM",
    lora_dropout=0.05,
)
```

---

## Common Workflow: FSDP Multi-GPU

See `pytorch-fsdp` sub-skill for the full guide.

```python
from torch.distributed.fsdp import FullyShardedDataParallel as FSDP

model = FSDP(
    model,
    sharding_strategy=ShardingStrategy.FULL_SHARD,
    cpu_offload=CpuOffload(False),
    mixed_precision=MixedPrecision(
        param_dtype=torch.bfloat16,
        reduce_dtype=torch.float32,
        buffer_dtype=torch.bfloat16,
    ),
)
```

---

## Resources

- TRL: https://huggingface.co/docs/trl
- Unsloth: https://docs.unsloth.ai/
- Axolotl: https://github.com/axolotl-ai/axolotl
- DeepSeek R1 GRPO Paper: https://arxiv.org/abs/2501.12948
