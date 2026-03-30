# OpenClaw Local Runtime Setup

Use this guide when Feishu OpenClaw installs the skill from GitHub but cannot call image APIs directly.

## Why This Setup Exists

OpenClaw can install the skill repository from GitHub, but your image generation should run through a local project entrypoint instead of direct model API calls.

This repository provides that local entrypoint at:

```powershell
python scripts/doubao_bridge.py <step> --input-json <input.json> --output-json <result.json>
```

## Required Post-Install Step

After OpenClaw installs or clones this repository onto the machine that will execute the skill, create a local `.env.local` file in the repository root.

Example:

```dotenv
DOUBAO_API_KEY=your-real-key
DOUBAO_BASE_URL=https://your-doubao-compatible-host
DOUBAO_TIMEOUT_SECS=120
DOUBAO_RUNTIME_ENDPOINT=
DOUBAO_ANALYZE_ENDPOINT=
DOUBAO_CUTOUT_ENDPOINT=
DOUBAO_FUSION_ENDPOINT=
DOUBAO_ASSETS_ENDPOINT=
DOUBAO_TYPOGRAPHY_ENDPOINT=
```

`.env.local` is ignored by git and should stay only on the execution machine.

## Recommended OpenClaw Invocation Pattern

1. OpenClaw reads one Feishu row.
2. OpenClaw writes a temporary JSON file for the current step.
3. OpenClaw runs the local bridge script.
4. The bridge reads `.env.local`.
5. The bridge calls your Doubao-compatible runtime.
6. The bridge writes a normalized `StepResult` JSON file.
7. OpenClaw reads that JSON file and updates the Feishu row.

## Example

```powershell
python scripts/doubao_bridge.py step3 --input-json tmp\step3-input.json --output-json tmp\step3-result.json
```

## Security Note

Do not put real secrets into `SKILL.md`, `README.md`, or any tracked GitHub file. The GitHub repository should stay installable, while `.env.local` stays local to the OpenClaw runner machine.
