---
name: art-step4-assets
description: Use when Codex needs to generate three transparent supporting assets that match the Step3 hero style and the Blueprint material elements for the art pipeline.
---

# Art Step4 Assets

Generate three matching transparent accessory assets after the hero artwork is approved. This skill must keep Step3 style continuity while using Step1 material cues as the subject matter source.

## Purpose
- Reverse-engineer style, palette, and lighting from `fusion_4k`.
- Combine that style with `Blueprint.material_elements`.
- Produce exactly three isolated transparent assets for downstream packaging.

## Inputs
- `task_id`
- `fusion_4k`
- `Blueprint.material_elements`
- Optional `style_summary` from Step3

## Output Schema
```json
{
  "success": true,
  "step": "step4",
  "artifact_urls": [
    "{task_id}/asset_1.png",
    "{task_id}/asset_2.png",
    "{task_id}/asset_3.png"
  ],
  "structured_output": {
    "asset_subjects": ["tarot card", "crescent sigil", "crystal charm"],
    "transparent_ready": true
  },
  "error_code": "",
  "error_message": ""
}
```

## Prompt Workflow
1. Read `fusion_4k` and summarize its palette, render style, materials, and lighting.
2. Choose three distinct objects from `Blueprint.material_elements`.
3. Render each object as a modern polished asset, defaulting to a premium 3D look unless the hero style strongly suggests another medium.
4. Stage each object on pure white, then remove the background to transparent.
5. Keep each asset visually readable at small scale.
6. Return one `StepResult` with three artifact paths.

## Retry Rules
- If assets do not match the hero image style, retry with a tighter style summary derived from `fusion_4k`.
- If the assets are not transparent-ready, retry with stronger white-background isolation instructions.
- If two assets are too similar, retry by forcing distinct silhouettes and functions.

## Quality Checks
- Exactly three assets must be returned.
- Each asset must be isolated and readable.
- Assets must feel like a set, not three unrelated objects.
- Transparency must be clean enough for compositing.

## Handoff To Next Step
- Package `asset_1.png`, `asset_2.png`, and `asset_3.png` for the final bundle.
- No further downstream dependency beyond packaging.

## Prohibitions
- Do not create scene fragments instead of single objects.
- Do not ignore the `Blueprint.material_elements`.
- Do not keep white halos in the transparent PNGs.

## Reference Map
- Shared contracts: [`../references/prompt-contracts.md`](../references/prompt-contracts.md)
- Shared retry rules: [`../references/error-recovery.md`](../references/error-recovery.md)
- Step4 prompt example: [`references/step4-prompt-example.md`](references/step4-prompt-example.md)
