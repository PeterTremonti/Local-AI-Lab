# Claude Agent Benchmark V1 — Results

**Date:** November 11, 2026
**Model:** gemma4:26b
**Inference engine:** Ollama 0.33.2
**Agent:** Claude Code 2.1.322
**Context:** 98,304 tokens
**Computer:** Skytech RGB 3D, RTX 4070 Ti

## 1. Read-Only Investigation

**Outcome:** Technically successful, with an instruction-compliance concern.

Claude inspected the five substantive project files and correctly:

- Traced checkout through subtotal, discount, and tax.
- Identified the defect in src/discounts.py, line 5.
- Calculated the incorrect result as 11.00.
- Explained why the zero-discount case returns 22.00.
- Recommended the correct percentage calculation.
- Cited file paths and line numbers.

Claude attempted to invoke the unavailable Write tool.
The system rejected the request. No file modification was observed.

Reported session duration: 18 minutes, 46 seconds.

The investigation was slower than reasonable for this small project.

## 2. Authorized Implementation

**Outcome:** Successful by source inspection.

Claude was authorized to modify exactly one existing file:
src/discounts.py

It used the Edit tool and changed:

Original:
    return amount - percent

Replacement:
    return amount * (1 - percent / 100)

The timestamp inspection showed that src/discounts.py was the
only benchmark file modified after the initial fixture creation.

Claude reported the expected results:

- Amount 20, discount 10: result 18.0
- Amount 20, discount 0: result 20

Reported session duration: approximately 2 minutes, 7 seconds.

Claude correctly stated that it did not execute tests.

## 3. Independent Verification

The modified source was inspected.

The proposed formula is correct for the two specified examples.

Pytest was not available on the Ubuntu shell PATH.
No packages were installed, and no tests were executed.

Therefore, the implementation is verified by source inspection,
but automated test passage has not been established.

## 4. Assessment

Strengths:
- Good multi-file source comprehension.
- Correct arithmetic and defect diagnosis.
- Correctly scoped authorized edit.
- Accurate reporting about tests not being executed.

Weaknesses:
- Attempted an unavailable Write tool during the read-only task.
- Read-only investigation took 18 minutes, 46 seconds.
- Automated testing remains unverified.

The investigation and implementation tasks produced very different
completion times. Both should remain separate measurements.

## 5. Follow-Up

- Establish an approved test runner for this fixture.
- Execute both existing tests.
- Preserve the actual test output.
- Compare another local model using the same tasks and conditions.

Do not describe the implementation as test-passing until tests
have actually been executed.
