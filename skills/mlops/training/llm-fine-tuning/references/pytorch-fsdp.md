# PyTorch FSDP — Distributed Training Reference

> Absorbed from `pytorch-fsdp` skill — use this reference for FSDP distributed training guidance.

## When to Use

- Multi-GPU large model training
- Parameter sharding across GPUs
- CPU offloading for very large models
- Mixed precision training for memory efficiency

## Core FSDP Concepts

### Sharding Strategies

| Strategy | Description |
|-----------|-------------|
| `FULL_SHARD` | Shards parameters, gradients, and optim states across GPUs |
| `SHARD_GRAD_OP` | Shards gradients and optim states, replicates parameters |
| `NO_SHARD` | Replicates all across GPUs (DataParallel behavior) |
| `HYBRID_SHARD` | Shards within a node, replicates across nodes |

### CPU Offloading
```python
from torch.distributed.fsdp import CPUOffload
cpu_offload = CPUOffload(True)  # Offload all params to CPU when not needed
```

### Mixed Precision
```python
from torch.distributed.fsdp import MixedPrecision
mixed_precision = MixedPrecision(
    param_dtype=torch.bfloat16,
    reduce_dtype=torch.float32,
    buffer_dtype=torch.bfloat16,
)
```

## Basic FSDP Setup

```python
from torch.distributed.fsdp import FullyShardedDataParallel as FSDP
from torch.distributed.fsdp import ShardingStrategy

model = FSDP(
    model,
    sharding_strategy=ShardingStrategy.FULL_SHARD,
    cpu_offload=CpuOffload(False),
    mixed_precision=MixedPrecision(...),
    device_id=torch.cuda.current_device(),
)
```

## FSDP2 (Newer API)

FSDP2 is a simplified API available in PyTorch 2.5+ with better performance for transformer models.

## Key Pitfalls

1. **Gradient checkpointing**: Enable with `checkpoint=True` to save memory
2. **Device placement**: Move model to device before wrapping with FSDP
3. **Batch size scaling**: Increase effective batch size with `gradient_accumulation_steps`
4. **Synchronization**: FSDP requires proper distributed setup (`torchrun` or `torch.distributed`)

## Join Context Manager

For uneven inputs across processes:
```python
with torch.distributed.fsdp.FSDPV2.spawn(
    [0, 1, 2, 3],  # GPU IDs
    ...
) as handle:
    ...
```

For full content, use the `pytorch-fsdp` sub-skill directly.
