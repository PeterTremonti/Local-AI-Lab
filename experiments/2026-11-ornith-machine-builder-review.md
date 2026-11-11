# Ornith-1.5 Machine Builder Architecture Review

**Evaluation date:** November 11, 2026
**Agent:** Claude Code with local Ollama model `ornith-1.5:9b`
**Review mode:** Read-only (`Read`, `Glob`, `Grep`), Plan Mode
**Context ceiling:** 98,304 tokens
**Evaluated snapshot:** `810e29f302d81fc5a7a4ef1102e0f415eb0cd10a` (`Current wiring issues`)
**Snapshot state:** Clean `main` checkout with no configured remotes

## 1. Purpose and scope

This was an isolated architectural evaluation of Ornith-1.5 as a coding and repository-investigation agent. The Machine Builder checkout was a separate review snapshot, not the authoritative working repository.

The investigation covered six areas:

1. Canonical semantic model and presentation model boundaries.
2. Mutation atomicity and store transaction behavior.
3. Provenance and semantic data coverage.
4. Relationship removal and model consistency.
5. Persistence and serialization.
6. UI synchronization, notifications, and documentation status.

Follow-up investigations examined transaction rollback, relationship removal, UI references after synchronization, and listener exception behavior.

**Safety and test boundaries:** The session was restricted to read-only tools and Plan Mode. No source files were intentionally changed, no implementation was attempted, and no test suite was run. Findings below are the agent's source inspection and follow-up analysis, not independently reproduced test results.

## 2. Executive assessment

Ornith-1.5 produced a useful architectural review and followed the observed read-only tool boundary during this evaluation. It traced several relevant code paths across the semantic model, store, canvas, and persistence layers.

The strongest confirmed result is that `store.commit()` protects the mutation application phase with a snapshot-and-restore mechanism. The review also clarified that semantic relationships are independently stored objects; the earlier concern about orphaned inverse relationship references was withdrawn after inspection.

The most actionable remaining observation is a possible error-reporting ambiguity in post-commit notification: a listener exception can escape to the caller even though the mutation and undo bookkeeping have already succeeded. This is a latent design weakness, not a demonstrated data-corruption bug. No actual listener exception was reproduced.

Overall, the review is promising evidence of useful repository-level reasoning, but it should not be treated as a substitute for tests or source-owner review. Follow-up questioning materially improved the accuracy of the initial findings.

## 3. Architecture: canonical model and presentation model

The agent identified the canonical semantic model as the authoritative representation of machine meaning, with the visual model acting as a presentation-oriented projection.

This is an important boundary:

- Semantic entities and relationships represent the machine's meaning.
- Visual objects represent how that information is presented and manipulated in the editor.
- Canvas synchronization should update the presentation from model state rather than turn visual objects into a competing semantic authority.

The inspection traced the canvas store subscription through `canvas.py` and into scene synchronization. The scene code uses identifiers to reconcile visual items with current model data. The inspected node graphics item retains an ID and node type rather than serving as a long-lived reference to a canonical model object.

Relevant source locations reported by the agent:

- `canvas.py:79` — store listener registration.
- `canvas.py:163-165` — model-change handling and scene synchronization.
- `canvas_scene.py:504-544` — scene synchronization.
- `graphics/node.py:66-67` — retained node identity/type.

This supports the architectural direction in which the semantic model remains authoritative and the canvas is synchronized from it.

## 4. Mutation atomicity and transaction behavior

The follow-up inspection traced `store.commit()` in `store.py:119-136`.

The reported execution sequence is:

1. Deep-copy the current editor state as a rollback snapshot.
2. Apply the mutation to the current state.
3. If mutation application raises an exception, restore the snapshot and re-raise.
4. After successful application, perform undo bookkeeping and update modified state.
5. Notify listeners.

The exception handler protects the mutation application phase. The follow-up also found only one production `.apply()` invocation in this commit path.

**Conclusion:** The inspected in-memory mutation boundary is atomic with respect to exceptions raised during `mutation.apply()`. Semantic and visual changes performed together inside that mutation are restored together when application fails.

This corrects any interpretation that the store lacks mutation rollback. It does not mean every later operation in `commit()` is part of the same rollback-protected region. Listener notification occurs after the mutation and undo bookkeeping.

Relevant source location: `store.py:119-136`.

## 5. Provenance and semantic data coverage

The agent found explicit provenance support across a number of canonical data types. The types identified in the review included:

- `HardwareDefinition`
- `SemanticPort`
- `Function`
- `MachineComponent`
- `Machine`
- `Controller`
- `ControllerResource`
- `ControllerResourceAssignment`
- `SemanticConnection`
- `Harness`
- `SemanticRelationship`
- `SemanticValue`
- `SemanticValueStatus`

The review also examined validation around controller-resource assignments and harness data, including cleanup behavior.

The architectural significance is that provenance is represented as model data for important semantic entities rather than being solely an informal UI annotation.

This inventory should be treated as the agent's inspected coverage list, not proof that every provenance path is complete or that all model types have identical provenance guarantees. No exhaustive automated coverage check was run.

## 6. Relationship removal: earlier concern retracted

The initial review raised a concern that removing a relationship might leave orphaned inverse references.

The follow-up inspected `semantic_model.py:998-1016` and found that `remove_relationship` removes the relationship from its independent relationship collection. The inspection did not find other model objects retaining inverse relationship IDs that would need cleanup.

**Conclusion:** The orphaned-inverse-reference concern was not supported by the inspected data model and was explicitly withdrawn. It should not be recorded as a confirmed defect.

## 7. Persistence and serialization

The review identified a manually maintained type registry in `persistence.py`, around lines 64-91. The serialization path uses explicit encode/decode handling and a format-version field. The inspected save path also uses a temporary file followed by `os.replace`, which is intended to avoid leaving a partially written destination during replacement.

Two observations were left unresolved:

- The manual type registry means new persisted types need the appropriate registration and serialization handling. This is a maintenance requirement, not by itself a defect.
- The agent noticed a possible integer-key serialization issue in connection with board fixtures. It was not reproduced or established as a production persistence failure.

The integer-key observation should remain a verification item, not a confirmed bug.

## 8. UI synchronization and listener exceptions

The follow-up examined whether failed mutations could leave the canvas holding stale references.

The agent reported that:

- The store listener is `canvas._model_changed` (`canvas.py:79`).
- The canvas synchronizes the scene from the current visual model.
- Scene synchronization reconciles by identifiers and re-reads model state.
- The inspected graphics node retains identity fields rather than a direct canonical object reference.
- The semantic layer is accessed from the store when needed.
- A failed mutation restores the previous state and does not notify listeners.

The review found 19 `store.commit()` call sites and reported no exception handling around those calls. It also distinguished the document-controller listener in `app.py:290` from the store listener; they are separate notification paths.

### Remaining observation: notification exceptions happen after commit

`store.py:295-298` contains `_notify()`, which invokes listeners in a bare loop without catching listener exceptions.

In `store.commit()`, notification occurs after mutation application and undo bookkeeping, outside the mutation rollback handler.

Consequently, if a listener raises:

- The mutation may already be successfully applied.
- The undo record may already be stored.
- The exception can still propagate to the caller.
- The caller may interpret the operation as failed even though the state change succeeded.

This is a **post-commit error-reporting ambiguity**, not evidence that the mutation itself was partially applied or corrupted.

No listener exception was actually triggered during the review. The current store listener was identified as the canvas model-change handler, but its failure behavior was not experimentally tested.

A focused test and an explicit policy for listener failures would be reasonable future work. Possible policies include isolating listener exceptions and reporting them separately, or otherwise making the post-commit nature of the failure clear. Any change should preserve the distinction between a failed mutation and a notification failure after a successful mutation.

## 9. Additional unverified observation

The agent identified a possible `KeyError` path in `assignments_from_source` / `assignments_for_source` in `controller_resource_assignment_queries.py:119-134` when an unknown source is supplied.

This was not tested. It remains a small verification candidate rather than a confirmed defect.

## 10. Documentation and roadmap observations

The review inspected roadmap and documentation status and noted that documented completion claims and test counts may be historical rather than evidence of the current checkout's test state.

The agent distinguished documented milestone status from GUI acceptance items that remained open.

Because the evaluation used an isolated snapshot and did not run tests, it does not establish the current live repository's test count, acceptance status, or implementation state.

## 11. Accuracy and limitations of the evaluation

The follow-up questions were valuable. In particular:

- Store rollback behavior was traced to the actual commit implementation.
- The orphaned inverse-reference concern was withdrawn after examining the relationship representation.
- The UI stale-reference concern was checked against the actual synchronization path.
- The remaining listener concern was narrowed to exceptions after a successful mutation, with no claim that an exception had been reproduced.

This is a useful example of why agent-generated architectural findings should be challenged with targeted source tracing. The initial observation, its evidence, and the follow-up correction should remain distinguishable.

Limitations:

- No automated tests were run.
- No listener exception was simulated.
- The possible integer-key persistence issue was not reproduced.
- The possible unknown-source `KeyError` was not tested.
- The review was against the identified isolated snapshot, not a fresh checkout of the live Machine Builder repository.
- Source line references describe that snapshot and may move as the code changes.

## 12. Recommended disposition

**No immediate Machine Builder code change is justified by this review alone.**

The useful follow-up candidates, in priority order, are:

1. Add a focused test for a store listener that raises after a successful commit, and decide how the application should report that post-commit failure.
2. Verify the suspected integer-key persistence edge case against a minimal real serialization example.
3. Verify behavior when assignment query helpers receive an unknown source.
4. Continue using source-backed, read-only agent reviews before authorizing implementation work.

The evaluation supports keeping Ornith-1.5 as a promising local coding-agent candidate. It does not yet establish reliability for unrestricted or substantial engineering work. Continue to require narrow task scopes, explicit tool permissions, independent test execution, and review of the actual diff.
