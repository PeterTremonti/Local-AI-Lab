# Local AI Lab

A practical local AI environment using existing computers,
local inference engines, coding agents, and open models.

The primary objective is to minimize paid API usage and
develop a useful local AI development environment.

## Current Priorities

1. Establish reliable local Ollama inference.
2. Use Claude Code with locally hosted models.
3. Evaluate local models against substantial coding tasks.
4. Investigate the high-RAM home computer as a possible
   secondary inference server.
5. Evaluate alternative inference engines and model-loading
   approaches when justified by testing.

## Workstation: Skytech RGB 3D

- Operating system: Windows 10 with WSL2
- Linux: Ubuntu 22.04.5 LTS
- WSL username: peter
- GPU: NVIDIA GeForce RTX 4070 Ti
- Dedicated GPU memory: approximately 12 GB
- Windows physical RAM: approximately 31.8 GB
- WSL memory: approximately 15 GiB
- WSL swap: 4 GiB
- No custom .wslconfig currently present

## Development Environment

- VS Code connected through Remote - WSL
- Workspace: /home/peter/projects/local-ai-lab
- Python: 3.11.15 (Hermes environment)
- Git repository initialized locally on branch main

## Ollama

- Installation: Ubuntu/WSL
- Executable: /usr/local/bin/ollama
- Version: 0.33.2
- Service: ollama.service
- API: http://127.0.0.1:11434

Systemd drop-ins:

- context.conf: OLLAMA_CONTEXT_LENGTH=98304
- keepalive.conf: OLLAMA_KEEP_ALIVE=-1

### Installed Models

| Model | Approximate disk size |
|---|---:|
| gemma4:26b | 18 GB |
| gemma4:31b | 19 GB |
| gemma4:latest | 9.6 GB |
| gemma:latest | 5.0 GB |
| llama3:8b | 4.7 GB |
| llama3.1:8b | 4.9 GB |

Additional aliases may refer to identical model digests.

## Hermes Agent

- Version: 0.21.1
- Installation: Git
- Location: /home/peter/.hermes/hermes-agent
- Executable: /home/peter/.local/bin/hermes
- Python: 3.11.15

Current model configuration:

- Model: gemma4:26b
- Provider: custom
- Endpoint: http://127.0.0.1:11434/v1
- Context length: 98304

## Claude Code

- Version observed: 2.1.319
- Installation: Native Linux
- Executable: /home/peter/.local/bin/claude
- Inference integration: Ollama
- Selected model: gemma4:26b
- Endpoint reported by /status: http://127.0.0.1:11434

Initial tests:

- Claude Code launched successfully through Ollama.
- A simple text-generation test succeeded.
- A read-only workspace inspection succeeded.
- Plan Mode was activated using Shift+Tab.
- Context window reported approximately 98.3k tokens.

Initial repository-inspection test took approximately 3 minutes.
Performance requires further testing.

## GPU and Memory Observations

During the initial Gemma4 26B session:

- Ollama reported 27% CPU / 73% GPU.
- Ollama reported a 98,304-token context.
- NVIDIA reported approximately 11.1 GiB GPU memory occupied.
- WSL reported approximately 12 GiB available memory.
- Approximately 596 MiB swap was in use.

The Ollama process-size report requires further verification.
Do not assume its reported 1.5 GB represents total model memory.

## Windows Ollama

The separate Windows Ollama installation was uninstalled.

Its downloaded model files were also removed.

DeepSeek Coder 33B, DeepSeek Coder 6.7B, and Qwen 3.5
are candidates for future Ubuntu downloads and testing.

Ubuntu Ollama and its models were unaffected.

## Separate Home Computer

A second computer may provide substantial system RAM
and four older NVIDIA Quadro GPUs.

Exact hardware specifications remain unverified.

Do not assume the Quadro GPUs support modern inference
software or that their VRAM can be pooled automatically.

## Research List

- llama.cpp
- Strata (https://github.com/mach10x/strata)
- DeepSeek Coder
- Qwen coding models
- Multi-computer local inference
- CPU/RAM/SSD model offloading

These are research topics, not immediate installation tasks.

## Immediate Next Steps

1. Complete initial repository documentation.
2. Create a private GitHub repository.
3. Verify model loading and inference performance.
4. Complete a controlled Claude Code test.
5. Prepare a protected Machine Builder source copy.
6. Evaluate architectural analysis quality.
7. Investigate the home computer.

## Security

Never commit:

- API keys or passwords.
- Authentication tokens.
- SSH private keys.
- Personal credentials.
- Model weights.
- Private configuration files containing secrets.

## Operating Guide

See [LOCAL_AI_LAB_WORKFLOW.md](LOCAL_AI_LAB_WORKFLOW.md) for the
project's operating rules, workstation startup instructions,
Claude Code restrictions, Git practices, and experiment procedures.
