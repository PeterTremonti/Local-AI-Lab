# Ornith-1.5 9B — Claude Code Agent Benchmark

**Date:** November 11, 2026
**Model:** ornith-1.5:9b
**Agent:** Claude Code 2.1.322
**Inference engine:** Ollama 0.33.2
**Computer:** Skytech RGB 3D
**GPU:** NVIDIA RTX 4070 Ti
**Context:** 98,304 tokens

## 1. Read-Only Investigation

**Result: Successful.**

Claude inspected the benchmark files and produced a technically correct
diagnosis.

It:
- Traced checkout through subtotal, discount, and tax.
- Located the defect in src/discounts.py, line 5.
- Calculated the incorrect result as 11.00.
- Explained why the zero-discount test returns 22.00.
- Proposed an appropriate percentage-discount correction.
- Cited exact file paths and line numbers.
- Did not claim to have executed tests.

No unavailable Write-tool attempt was observed.

Reported session duration: approximately 1 minute, 4 seconds.

The model demonstrated good source navigation, arithmetic reasoning,
evidence use, and instruction compliance.

## 2. Authorized Implementation

**Result: Successful.**

Claude was authorized to modify exactly one existing file:
src/discounts.py.

It used the Edit tool and replaced:

    return amount - percent

with:

    return amount - amount * (percent / 100)

The timestamp inspection showed that src/discounts.py was the only
benchmark file modified after fixture creation.

Expected results:
- Amount 20, discount 10: 18.
- Amount 20, discount 0: 20.

Claude correctly stated that it had not executed tests.

Reported session duration: approximately 21 seconds.

## 3. Independent Test Verification

Pytest was installed in a dedicated virtual environment outside
the repository.

- Python: 3.10.12
- Pytest: 9.2.0
- Environment: ~/.venvs/local-ai-lab-pytest

Both existing tests were executed independently of Claude Code.

**Result: 2 passed in 0.01 seconds.**

The tests verified:
- Ten-percent discount followed by ten-percent tax: 19.80.
- Zero discount followed by ten-percent tax: 22.00.

The corrected implementation passed both tests.

This establishes correctness for the supplied cases, not every
possible discount input.

## 4. Comparison With Gemma4 26B

| Measurement | Gemma4 26B | Ornith 9B |
|---|---:|---:|
| Read-only investigation | 18m 46s | 1m 4s |
| Authorized implementation | 2m 7s | 21s |
| Correct diagnosis | Yes | Yes |
| Correct implementation | Yes | Yes |
| One-file edit scope | Respected | Respected |
| Independent tests | 2 passed | 2 passed |
| Unavailable Write attempt during read-only investigation | Yes, blocked | None observed |

Ornith completed the investigation approximately 17.6 times faster
and the implementation approximately 6 times faster.

The original Gemma4 read-only investigation attempted to invoke an
unavailable Write tool. Claude Code rejected the request.

No corresponding forbidden-tool attempt was observed during Ornith's
read-only investigation.

These timings are individual observed sessions, not statistically
controlled averages.

## 5. Assessment

Ornith demonstrated:
- Strong multi-file source comprehension.
- Accurate calculation and defect identification.
- Good source references and explanations.
- Better observed instruction compliance.
- Correct authorized implementation.
- Successful independent tests.
- Much shorter observed completion times.

**Preliminary conclusion:** Ornith-1.5 9B is the stronger coding-agent
candidate in this evaluation.

Further testing on a substantially larger real-world repository
is required before treating it as the definitive primary model.
