# Gemma4 26B — Initial Hardware Baseline

**Date:** November 11, 2026
**Computer:** Skytech RGB 3D
**GPU:** NVIDIA RTX 4070 Ti, 12 GB
**Operating environment:** Windows 10 / WSL2 / Ubuntu 22.04.5
**Inference engine:** Ollama 0.33.2
**Model:** gemma4:26b, 25.2B parameters, Q4_K_M
**Model digest:** 08ae7ec1744b
**Allocated context:** 98,304 tokens

## 1. Test Method

Four direct Ollama API requests using the same 143-token coding prompt.

Settings:
- Context: 98,304
- Maximum output: 256 tokens
- Temperature: 0
- Seed: 42
- Thinking: disabled
- Streaming: disabled

The task was to identify and correct a Python function that should
return the second-largest distinct integer in a list.

Test inputs:
- [7, 2, 7, 5] should return 5.
- [4, 4] has no second-largest distinct value.

## 2. Performance Results

| Run | Prompt tokens/sec | Output tokens | Generation tokens/sec | Total seconds |
|---|---:|---:|---:|---:|
| 1 | 5.63 | 160 | 28.83 | 37.23 |
| 2 | 442.45 | 169 | 48.06 | 3.85 |
| 3 | 984.98 | 169 | 44.32 | 3.97 |
| 4 | 404.27 | 169 | 46.94 | 3.97 |

Runs 2–4:
- Average generation speed: 46.44 tokens/sec.
- Median generation speed: 46.94 tokens/sec.
- Average total request time: approximately 3.93 seconds.

Run 1 was substantially slower, particularly during prompt processing.
The reason for this variation is unknown and requires investigation.

## 3. Answer Quality

Run 1 correctly identified the duplicate-value problem but produced
Python code with an indentation error.

Run 4 produced syntactically correct code and the expected results:
- [7, 2, 7, 5] returns 5.
- [4, 4] returns None.

The prompt did not explicitly prescribe what to return when fewer
than two distinct values exist. None was the model's choice.

Runs 2 and 3 have timing records, but their generated answers were
not preserved.

## 4. Resource Observations

Ollama reported:
- CPU allocation: approximately 27%.
- GPU allocation: approximately 73%.
- Process-size column: 1.5 GB. This is not the model's complete
  memory footprint.

GPU memory:
- Approximately 11.3–11.4 GiB occupied out of 12,282 MiB.
- Approximately 600 MiB free after the fourth run.

WSL memory after testing:
- Approximately 8.5 GiB available.
- Approximately 2.3 GiB swap in use.

The model was already loaded before the first request. Run 1 is
therefore not a clean model-load cold-start measurement.

## 5. Initial Assessment

Gemma4 26B successfully completed the direct inference task.

Repeated-request generation speed was approximately 46 tokens/sec.
Answer quality was inconsistent between the first and fourth
preserved responses.

This test did not evaluate Claude Code, agent planning, filesystem
navigation, tool use, repository comprehension, or safe code editing.

Speed and answer quality must be measured separately.

## 6. Follow-up Testing

Future comparisons should:
1. Use identical prompts and settings.
2. Preserve every generated answer.
3. Validate generated code by executing or syntax-checking it.
4. Separate first-request and repeated-request performance.
5. Record GPU and system memory under comparable conditions.
6. Test Claude Code agent behavior separately from direct inference.

This is an initial hardware baseline, not a final model ranking.
