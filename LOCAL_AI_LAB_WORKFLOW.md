# Local AI Lab — Operating Rules and Startup Guide

**Purpose:** Establish consistent operating procedures for the local AI environment, ChatGPT-assisted development, and locally running AI agents such as Claude Code and Hermes.

**Last verified environment checkpoint:** November 8, 2026.

---

# 1. Project Purpose

Local AI Lab is an independent project.

Its purpose is to build a practical local AI environment using existing computers, local inference engines, coding agents, and open models.

Primary goals:

1. Minimize or eliminate paid API usage.
2. Run useful language models locally.
3. Use Claude Code and other coding agents with locally hosted models.
4. Evaluate models against substantial real-world software projects.
5. Investigate multiple computers working together as inference servers and workstations.
6. Retain useful technical knowledge, configuration history, research, and performance results.

Do not install every interesting AI project simply because it exists.

Prioritize working configurations and measured results over accumulating software.

Machine Builder is an evaluation subject, not part of Local AI Lab's project architecture or governance.

# 2. Project Authority and Evidence

Conversation history is not the permanent project record.

The durable record consists of:

- Local AI Lab repository documentation.
- Actual configuration files.
- Current software versions.
- Experiment results.
- Source repositories and their verified commits.
- Research references and technical documentation.

Use this evidence priority:

1. Actual current system configuration and behavior.
2. Current source code and test results.
3. Verified repository and Git state.
4. Current project documentation.
5. Previous experiment reports.
6. Conversation memory and recollection.

Distinguish four evidence states:

**REPORTED:** Someone stated a result, but it has not been independently inspected.

**LOCALLY INSPECTED:** The relevant configuration, source, or repository state was examined.

**TESTED:** A specific command or test was executed and its outcome recorded.

**PUBLISHED:** A commit or result was verified on the remote repository.

Never promote one evidence state to another without verification.

Distinguish established facts, hypotheses, estimates, recommendations, and unresolved questions.

Do not claim a configuration change, installation, test, or publication succeeded merely because a command was attempted.

# 3. Hardware Environment

## Primary workstation: Skytech RGB 3D

- Operating system: Windows 10.
- Linux environment: Ubuntu 22.04.5 LTS under WSL2.
- WSL username: peter.
- GPU: NVIDIA GeForce RTX 4070 Ti.
- Dedicated GPU memory: 12,282 MiB.
- Physical Windows RAM: approximately 31.8 GB.
- Previously observed WSL memory: 15 GiB.
- Previously observed WSL swap: 4 GiB.
- WSL systemd enabled.
- No custom Windows `.wslconfig` was present at the November 6 inspection.

Keep the Linux development workspace in the Ubuntu filesystem, not OneDrive or a Windows-synchronized folder.

## Secondary home computer

A separate computer may have substantial system RAM and four older NVIDIA Quadro GPUs.

Exact hardware remains unverified.

Do not assume:
- The Quadro cards support modern inference engines.
- Their VRAM can be pooled automatically.
- Four GPUs provide four times the inference performance.
- Old CUDA compatibility guarantees modern AI compatibility.

Investigate its actual hardware before making recommendations.

Do not recommend purchasing GPUs until performance requirements and existing hardware capabilities are understood.

# 4. Local Software Environment

The primary environment is Ubuntu/WSL.

## Ollama

Verified installation:

- Version: 0.33.2.
- Executable: `/usr/local/bin/ollama`.
- Service: `ollama.service`.
- Service command: `/usr/local/bin/ollama serve`.
- API: `http://127.0.0.1:11434`.

The service is enabled under systemd.

Existing service drop-ins:

- `/etc/systemd/system/ollama.service.d/context.conf`
- `/etc/systemd/system/ollama.service.d/keepalive.conf`

Verified settings:

```ini
OLLAMA_CONTEXT_LENGTH=98304
OLLAMA_KEEP_ALIVE=-1
```

Do not modify these without inspecting their current contents and understanding the effects.

`OLLAMA_KEEP_ALIVE=-1` keeps models loaded indefinitely until explicitly unloaded or the service stops.

## Installed Ollama models

Last verified inventory:

| Model | Approximate size |
|---|---:|
| gemma4:26b | 18 GB |
| gemma4:31b | 19 GB |
| gemma4:latest | 9.6 GB |
| gemma:latest | 5.0 GB |
| llama3:8b | 4.7 GB |
| llama3.1:8b | 4.9 GB |

Some tags can refer to identical model digests.

Always check the actual installed inventory before recommending downloads.

## Hermes Agent

Verified installation:

- Version: 0.21.1.
- Installation method: Git.
- Install directory: `/home/peter/.hermes/hermes-agent`.
- Executable: `/home/peter/.local/bin/hermes`.
- Python: 3.11.15.

Verified configuration:

- Model: `gemma4:26b`.
- Provider: `custom`.
- Endpoint: `http://127.0.0.1:11434/v1`.
- Context length: 98,304.

Hermes is configured for the Ubuntu Ollama server.

Do not update Hermes merely because a newer upstream revision is available. Evaluate updates when there is a specific reason.

## Claude Code

Last verified version: 2.1.319.

Installation:

- Native Linux installation.
- Executable: `/home/peter/.local/bin/claude`.
- Native installation directory under `/home/peter/.local/share/claude/versions/`.

Claude Code is launched through the Ollama integration.

The intended model is `gemma4:26b`.

The expected local API endpoint is:

`http://127.0.0.1:11434`

Claude Code's API compatibility layer uses the Anthropic-compatible Ollama endpoint.

Hermes and Claude Code use different API compatibility paths. Do not copy one application's endpoint configuration blindly into the other.

# 5. Windows and Ubuntu Separation

There must be only one Ollama installation for this workstation.

Windows Ollama 0.34.1 was uninstalled.

Its Windows model files were removed.

Ubuntu Ollama 0.33.2 remains the primary installation.

Do not reinstall Windows Ollama.

Do not confuse Windows PowerShell with Ubuntu Bash.

Typical prompts:

```text
PS C:\Users\peter>
```

Windows PowerShell.

```text
peter@SkytechRGB3D:~$
```

Ubuntu Bash.

Commands must be written for the correct shell.

Use WSL for all normal Local AI Lab software management.

# 6. VS Code Workspace Arrangement

VS Code runs in Windows but connects to Ubuntu using Microsoft's Remote - WSL extension.

Primary project:

```text
/home/peter/projects/local-ai-lab
```

Machine Builder evaluation copy:

```text
/home/peter/projects/claude-evaluation/machine-builder-review
```

Open separate VS Code windows for separate workspaces.

To open Local AI Lab:

```bash
cd ~/projects/local-ai-lab
code .
```

To open the Machine Builder evaluation copy:

```bash
cd ~/projects/claude-evaluation/machine-builder-review
code .
```

Confirm the window identifies the correct WSL distribution.

Use the integrated Ubuntu terminal.

Do not accidentally open a Windows PowerShell terminal when Linux commands are expected.

# 7. Standard Workstation Startup Procedure

Use this procedure when starting a new working session.

## Step 1 — Start Ubuntu

Open Ubuntu 22.04 from the Windows Start menu.

Do not start Windows Ollama.

## Step 2 — Verify Ollama

In Ubuntu:

```bash
echo "========== OLLAMA SERVICE =========="
systemctl is-active ollama

echo
echo "========== OLLAMA VERSION =========="
ollama --version

echo
echo "========== OLLAMA API =========="
curl -fsS http://127.0.0.1:11434/api/version

echo
echo
echo "========== INSTALLED MODELS =========="
ollama list
```

Expected service status:

`active`

Expected API version:

`0.33.2`

If the service is inactive, inspect its status and logs before attempting recovery.

Do not restart or modify a working service unnecessarily.

## Step 3 — Open the appropriate VS Code workspace

For Local AI Lab:

```bash
cd ~/projects/local-ai-lab
code .
```

For Machine Builder evaluation:

```bash
cd ~/projects/claude-evaluation/machine-builder-review
code .
```

## Step 4 — Verify the selected model

Check that the intended model exists:

```bash
ollama list
```

For the initial coding-agent evaluation, use:

`gemma4:26b`

Do not select cloud models.

## Step 5 — Start Claude Code

From the directory Claude is supposed to inspect, run:

```bash
ollama launch claude --model gemma4:26b -- --restricted --tools "Read,Glob,Grep" --permission-mode plan
```

This is the preferred startup for read-only repository investigations.

It:
- Selects the local model explicitly.
- Starts Claude Code in restricted mode.
- Enables only the Read, Glob, and Grep tools.
- Starts in Plan Mode.
- Avoids enabling shell execution or editing tools.

The installed Claude Code and Ollama versions must support the supplied arguments. Check their respective `--help` output after relevant upgrades.

## Step 6 — Verify the Claude session

Inside Claude Code, run:

```text
/status
```

Verify:

- Model: `gemma4:26b`.
- Anthropic base URL: `http://127.0.0.1:11434`.
- Correct working directory.

Then run:

```text
/context
```

Verify that the context window agrees with Ollama's actual allocation.

The expected initial context is 98,304 tokens.

## Step 7 — Check model allocation

Open a second Ubuntu terminal:

```bash
echo "========== LOADED MODELS =========="
ollama ps

echo
echo "========== GPU =========="
nvidia-smi

echo
echo "========== SYSTEM MEMORY =========="
free -h
```

Record GPU/CPU allocation and memory readings when performing meaningful performance experiments.

The model does not need to be fully GPU-resident to work.

Do not interpret Ollama's reported process size as the model's complete memory footprint without corroborating evidence.

## Step 8 — End the session

Inside Claude Code:

```text
/exit
```

Avoid running multiple substantial coding-agent sessions simultaneously by default.

Ollama can serve multiple requests, but concurrent sessions may compete for GPU memory, system memory, and inference throughput.

Prefer one active agent session during controlled performance experiments.

# 8. Local-Only and Cost Restrictions

The default operating requirement is local inference.

Unless explicitly authorized:

- Do not use Anthropic cloud inference.
- Do not use cloud-hosted model tags such as `:cloud`.
- Do not configure OpenAI or other paid model APIs.
- Do not sign into cloud providers simply to make an integration work.
- Do not configure automatic cloud fallbacks.
- Do not use Claude cloud sessions.
- Do not send source code to external services.

Verify local inference using Claude Code `/status` and the actual endpoint.

The text `API Usage Billing` displayed in Claude Code does not establish that paid inference is occurring. The configured endpoint and actual requests determine the inference route.

For Hermes, verify its custom provider and local Ollama endpoint.

Any proposed exception to local-only operation requires explicit user approval.

Local model inference does not automatically make every agent tool local. Browser services, MCP servers, external APIs, plugins, and online research may still communicate with external systems. Treat those capabilities separately.

# 9. Claude Code Operating Rules

Claude Code is an assistant, not an unrestricted repository owner.

## Default operating mode

Use Plan Mode and read-only access for:
- Repository surveys.
- Architecture investigations.
- Code review.
- Research.
- Test coverage analysis.
- Development planning.
- Documentation assessment.

Prefer the restricted tool configuration:

```text
--restricted --tools "Read,Glob,Grep"
```

A prompt saying "do not edit files" is an instruction, not the same thing as technically disabling editing tools.

For important read-only investigations, use actual restricted tool access.

## Permission escalation

Move from read-only operation to implementation only when the user explicitly authorizes the task.

A bounded implementation assignment should specify:

1. Objective.
2. Allowed files or directories.
3. Expected changes.
4. Prohibited changes.
5. Required tests.
6. Acceptance criteria.
7. Git and publication permissions.

Authorization to investigate is not authorization to implement.

Authorization to implement is not automatically authorization to commit or push.

Never use permission-bypass options merely to avoid inconvenient prompts.

## Repository protection

Claude must not:
- Modify unrelated projects.
- Access parent directories unnecessarily.
- Change Git remotes or repository configuration.
- Stage or commit files without explicit authorization.
- Push changes without explicit authorization.
- Delete or overwrite user work.
- Install dependencies without approval.
- Execute unrequested commands.

For a read-only assignment, shell execution, file modification, external access, and Git mutation must remain unavailable.

## Evidence standards

For important findings:
- Identify exact file paths.
- Identify classes, functions, and symbols.
- Provide line references when possible.
- Explain what the evidence proves.
- Clearly identify assumptions and gaps.

Do not invent source files, test results, architectural relationships, or implemented features.

A plausible explanation is not proof.

# 10. ChatGPT Operating Rules

ChatGPT acts as technical adviser, investigator, documentation reviewer, and project coordinator.

It should:

1. Follow this document and the user's explicit instructions.
2. Use actual system output and supplied files as evidence.
3. Avoid unnecessary installations or complicated workflows.
4. Explain technical decisions and likely downstream problems.
5. Provide practical, copy-ready terminal commands when needed.
6. Keep commands bounded and independently verifiable.
7. Avoid claiming local execution or file modification without evidence.
8. Maintain separation between Local AI Lab and Machine Builder.
9. Research current versions and compatibility when those details matter.
10. Distinguish official documentation, developer claims, and independent benchmarks.

Do not ask the user to repeat known configuration information.

Do not make the user perform unnecessary diagnostic work.

When something is already working, preserve it unless there is a demonstrated reason to change it.

The user prefers:
- Exact commands.
- Clear sequential steps.
- Exact paths.
- Full-file replacements where appropriate.
- Plain-language technical explanations.
- Minimal Git complexity.
- Concise but complete reporting.
- A clear next action or an explicit statement that no user action is needed.

# 11. Tool Restrictions

For Local AI Lab repository inspection, source review, architecture work, testing, and documentation:

Do not use:
- Python.
- Jupyter.
- pandas.
- Notebooks.
- Data-analysis workflows.
- Temporary generated analysis scripts or artifacts.

Use:
- Ubuntu Bash.
- PowerShell where Windows operations are required.
- Git.
- Direct file inspection.
- Existing project tools.
- Existing test frameworks.

Do not create downloadable repository replacements or generated files as a substitute for understandable, direct repository operations.

For written documentation requested by the user, provide complete Markdown text and exact placement instructions.

# 12. Git and Repository Practices

Local AI Lab has its own independent repository:

```text
/home/peter/projects/local-ai-lab
```

GitHub:

`https://github.com/PeterTremonti/Local-AI-Lab`

The initial published commit is:

`b6e5f2b`

Branch:

`main`

Remote:

`origin`

Machine Builder has a separate evaluation snapshot:

```text
/home/peter/projects/claude-evaluation/machine-builder-review
```

Initial snapshot commit:

`810e29f302d81fc5a7a4ef1102e0f415eb0cd10a`

That checkout was cloned shallowly and its Git remote and upstream were removed.

Its intended role is isolated source review.

Do not reconnect it to the authoritative Machine Builder repository or publish changes from it.

## Git safety

Before meaningful Git operations, inspect:

- Repository root.
- Branch.
- HEAD.
- Remote configuration.
- Upstream.
- Working-tree status.
- Index status.
- Relevant diffs.

Stage only exact paths.

Never routinely use:
- `git add -A`.
- Broad resets.
- Blind discards.
- Forced pushes.
- Unverified amendments.
- Commands that might overwrite concurrent work.

Separate editing, validation, staging, committing, and pushing.

After committing, inspect the commit and exact changed paths.

After pushing, verify the remote branch.

Keep Local AI Lab documentation changes separate from Machine Builder source changes.

Never put passwords, tokens, private keys, model files, or personal credentials into Git.

# 13. Machine Builder Evaluation Rules

Machine Builder is used to assess the capabilities of local models and coding agents.

It is not part of Local AI Lab's own software architecture.

The first evaluation uses a published snapshot, not the user's authoritative working checkout.

Snapshot baseline:

`810e29f302d81fc5a7a4ef1102e0f415eb0cd10a`

Important limitation:

A published snapshot does not necessarily include uncommitted changes or later work on the user's laptop.

Do not claim it represents the complete current local project unless that has been verified.

## Evaluation phases

**Phase A — Repository comprehension**

Read the workflow documentation and understand the project.

**Phase B — Architecture**

Identify actual implementation layers, domain models, interfaces, data flow, persistence, and major subsystems.

**Phase C — Implementation classification**

Distinguish implemented, partially implemented, incomplete, proposed, and unknown functionality.

**Phase D — Testing assessment**

Examine test organization and coverage without claiming tests were executed.

**Phase E — Architectural assessment**

Identify strengths, weaknesses, coupling, dependencies, inconsistencies, and risks.

**Phase F — Development roadmap**

Propose staged work with reasons, dependencies, and acceptance criteria.

The first assignment is read-only.

No modifications, installations, commits, pushes, or unapproved test execution.

Compare model conclusions against actual source evidence and known project architecture.

Measure the quality of reasoning, not merely the length or confidence of the report.

# 14. Model and Inference Experiments

Performance experiments must be reproducible.

Record:

- Computer and hardware.
- Operating system.
- Inference engine and version.
- Model and exact quantization.
- Context size.
- GPU offload.
- System RAM usage.
- GPU memory usage.
- Swap usage.
- Prompt size.
- Generated output size.
- Time to first token.
- Prompt prefill performance when available.
- Decode tokens per second.
- Total elapsed time.
- Tool-calling accuracy.
- Observed failures and limitations.

Always distinguish prompt prefill from decode speed.

A headline tokens-per-second result is meaningless unless its measurement type is known.

Use identical prompts and conditions when comparing models.

Do not draw firm conclusions from a single run.

# 15. Alternative Inference Engines and Research

Research interests include:

- llama.cpp.
- Strata.
- DeepSeek Coder.
- Qwen coding models.
- Other local inference engines.
- CPU/RAM/SSD offloading.
- Multi-computer inference servers.

Strata research:

`https://github.com/mach10x/strata`

Strata is not currently installed.

Do not install it or modify the working Ollama setup merely to investigate it.

DeepSeek Coder 33B, DeepSeek Coder 6.7B, and Qwen 3.5 were previously installed in Windows Ollama, but those models were removed during the Windows Ollama uninstall.

They remain candidates for future Ubuntu downloads.

Do not download large models until the existing models have been evaluated.

Do not assume older Quadro cards will work with modern inference engines.

Verify current official documentation and compatibility before making deployment decisions.

Distinguish developer benchmarks from independent measurements.

# 16. Documentation and Continuity

Maintain useful project records in Local AI Lab.

Recommended documentation organization:

```text
Local-AI-Lab/
    README.md
    LOCAL_AI_LAB_WORKFLOW.md
    hardware/
    software/
    configuration/
    experiments/
    research/
    handoffs/
```

Use README for project orientation.

Use the workflow document for operating rules.

Use configuration documents for actual system settings.

Use experiment reports for model and hardware measurements.

Use research notes for external technical investigations.

Use handoffs when a substantial task or conversation is being continued elsewhere.

Update documentation at meaningful checkpoints, not after every minor command.

Preserve historical results rather than silently replacing them with newer measurements.

A handoff should identify:

- Current objective.
- Verified configuration.
- Repository and commit state.
- Work completed.
- Test results.
- Outstanding questions.
- Known limitations.
- Exact next action.

Keep one clear current-state reference rather than creating competing instructions.

# 17. Change Management

Before making a significant system change:

1. Inspect the existing configuration.
2. Identify what the change is intended to accomplish.
3. Identify dependencies and possible side effects.
4. Preserve the existing working configuration.
5. Make the smallest reasonable change.
6. Verify the result.
7. Record the actual outcome.

Prefer reversible changes.

Do not change multiple independent variables during one experiment.

Avoid optimizing performance before establishing a repeatable baseline.

Never change WSL memory ceilings, Ollama context settings, GPU configuration, or service configuration without evidence that the change is necessary.

# 18. Current Project Priorities

Maintain this order unless the user changes it.

1. Finish verifying local Claude Code operation using Gemma4 26B.
2. Evaluate Claude Code's ability to understand Machine Builder.
3. Record inference performance and tool-calling reliability.
4. Compare other coding models, including DeepSeek Coder and Qwen.
5. Evaluate the home computer's actual hardware.
6. Investigate a two-computer inference arrangement.
7. Revisit Strata and alternative inference engines.

Interesting discoveries may be recorded in the research list without interrupting the active priority.

# 19. General Operating Principle

The purpose of Local AI Lab is to build a useful working environment, not an unnecessarily complicated one.

Preserve working configurations.

Prefer measurable results over assumptions.

Keep the distinction between local and cloud inference explicit.

Keep source repositories protected.

Do not confuse an agent that can generate plausible answers with one that can reliably understand and work with real software.

Every meaningful experiment should improve our understanding of what the available hardware and software can actually accomplish.

**A successful installation is only the beginning. A reliable, reproducible, useful local AI environment is the objective.**