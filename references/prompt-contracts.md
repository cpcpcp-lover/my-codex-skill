# Prompt Contracts

Use these JSON interfaces exactly. All skills should return `StepResult`, and Step1 should embed a `Blueprint` in `structured_output`.

## Blueprint

```json
{
  "theme": "string",
  "palette": ["string"],
  "style": "string",
  "material_elements": ["string"],
  "composition": "string",
  "lighting": "string",
  "negative_constraints": ["string"]
}
```

Field rules:
- `theme`: one concrete theme phrase.
- `palette`: 2-5 concise color descriptors.
- `style`: one unified art-direction phrase.
- `material_elements`: 3-6 objects or motifs that can appear as background or accessory assets.
- `composition`: one sentence describing focal hierarchy and layout.
- `lighting`: one sentence describing dominant lighting behavior.
- `negative_constraints`: 3-5 guardrails that block common failure modes.

## StepResult

```json
{
  "success": true,
  "step": "step-name",
  "artifact_urls": ["path-or-url"],
  "structured_output": {},
  "error_code": "",
  "error_message": ""
}
```

Field rules:
- `success`: boolean only.
- `step`: one of `master`, `step1`, `step2`, `step3`, `step4`, `step5`.
- `artifact_urls`: stable output paths in task-local namespace.
- `structured_output`: step-specific JSON payload.
- `error_code`: machine-friendly short code, empty on success.
- `error_message`: concise diagnosis, empty on success.

## Recommended Error Codes
- `INPUT_MISSING`
- `BLUEPRINT_INVALID`
- `CUTOUT_SUBJECT_MISSING`
- `CUTOUT_NOT_TRANSPARENT`
- `FUSION_STYLE_DRIFT`
- `FUSION_RATIO_INVALID`
- `ASSET_SET_MISMATCH`
- `ASSET_NOT_TRANSPARENT`
- `TYPOGRAPHY_UNREADABLE`
- `TYPOGRAPHY_NOT_TRANSPARENT`
- `WRITEBACK_FAILED`
- `PACKAGE_FAILED`

## Prompt Framing Rules
- Bind the skill to one `task_id`.
- Restate only the inputs that matter to the current step.
- Ask for JSON only.
- Explicitly mention the expected artifact filenames.
- If retrying, mention the previous `error_code` and one targeted repair instruction.
