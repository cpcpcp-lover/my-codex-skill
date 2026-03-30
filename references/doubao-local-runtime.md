# Doubao Local Runtime

Use this repository in `local bridge` mode when Feishu OpenClaw cannot call image APIs directly.

## Security Rule

Do not store real API keys in any skill file, markdown file, or repository commit.

Use environment variables instead:

- `DOUBAO_API_KEY`
- `DOUBAO_BASE_URL`
- `DOUBAO_RUNTIME_ENDPOINT` or step-specific `DOUBAO_*_ENDPOINT`
- optional model ids such as `DOUBAO_VISION_MODEL` and `DOUBAO_IMAGE_MODEL`

A starter template is provided in `.env.example`.

## Bridge Script

The local runtime entrypoint is:

```powershell
python scripts/doubao_bridge.py <step> --input-json <input.json> --output-json <result.json>
```

Supported steps:

- `step1` or `analyze`
- `step2` or `cutout`
- `step3` or `fusion`
- `step4` or `assets`
- `step5` or `typography`

## Recommended OpenClaw Pattern

Instead of asking OpenClaw to call the image API directly:

1. OpenClaw prepares a task JSON file.
2. OpenClaw runs the local bridge script.
3. The bridge script reads local environment variables.
4. The bridge script calls your Doubao-compatible runtime endpoint.
5. The bridge script writes a normalized `StepResult` JSON file for the skill to read.

## Example Commands

Step1:

```powershell
python scripts/doubao_bridge.py step1 --input-json tmp\step1-input.json --output-json tmp\step1-result.json
```

Step3:

```powershell
python scripts/doubao_bridge.py step3 --input-json tmp\step3-input.json --output-json tmp\step3-result.json
```

Dry-run payload inspection:

```powershell
python scripts/doubao_bridge.py step3 --input-json tmp\step3-input.json --output-json tmp\step3-result.json --dry-run
```

## Input Contract

The bridge expects one JSON object describing the current task. At minimum include:

```json
{
  "task_id": "TASK-20260330-001",
  "A": "main image url or local path",
  "B": "reference image",
  "C": "material image",
  "D": "material image",
  "E": "material image",
  "F": "material image",
  "G": "typography text",
  "ratio": "16:9",
  "blueprint_json": {}
}
```

## Output Contract

The bridge writes a normalized `StepResult` JSON object:

```json
{
  "success": true,
  "step": "fusion",
  "artifact_urls": ["exports/TASK-20260330-001/fusion_4k.png"],
  "structured_output": {},
  "error_code": "",
  "error_message": ""
}
```

## Runtime Assumption

This bridge assumes you already have a Doubao-compatible HTTP runtime or proxy endpoint that your local machine can call. The repository does not hardcode ByteDance endpoint paths because those vary across environments and gateway setups.
