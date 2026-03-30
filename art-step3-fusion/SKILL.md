---
name: art-step3-fusion
description: Use when Codex needs to merge the B-F material images, optional reference image, Blueprint, and optional subject cutout into a unified 4K hero artwork for the art pipeline.
---

# Art Step3 Fusion

Create the main 4K composition. This skill is responsible for unified style, spatial structure, layered blending, atmosphere, and the final hero image used by Step4 and Step5.

## Purpose
- Select the best 3-4 supporting materials from `B-F`.
- Respect Step1 `Blueprint` as the primary design brief.
- Use optional reference image and optional subject cutout when present.
- Produce one polished 4K hero artwork in the requested ratio.

## Inputs
- `task_id`
- `Blueprint`
- Optional `subject_png`
- `B-F` source materials and optional reference image
- Ratio field or default `16:9`

## Output Schema
```json
{
  "success": true,
  "step": "step3",
  "artifact_urls": [
    "{task_id}/fusion_4k.png"
  ],
  "structured_output": {
    "ratio": "16:9",
    "selected_materials": ["B", "C", "E"],
    "style_summary": "red-black royal casino fantasy with metallic glow and layered smoke",
    "subject_used": true
  },
  "error_code": "",
  "error_message": ""
}
```

## Prompt Workflow
1. Read the `Blueprint` first and treat it as binding.
2. Score B-F materials for relevance, texture quality, and compatibility with the target style.
3. Pick 3-4 materials maximum to avoid visual clutter.
4. Build the composition with clear foreground, subject or focal plane, midground, and background.
5. Blend with darken, screen, overlay, soft-light, gradient-map, smoke, glow, and texture logic where appropriate.
6. Add controlled liquify-style motion only when it improves flow and tension.
7. Grade the final image so all elements share one lighting and color language.
8. Return StepResult JSON only.

## Retry Rules
- If the style feels inconsistent, retry with fewer materials and stronger `Blueprint` adherence.
- If the subject disappears, retry with explicit focal-priority instructions.
- If the output ratio or resolution is wrong, retry with exact 4K ratio constraints.
- If the scene becomes muddy, retry with stronger depth separation and one dominant light direction.

## Quality Checks
- Final image must have a clear focal hierarchy.
- Chosen materials must feel unified rather than collaged.
- Palette must remain faithful to the `Blueprint`.
- Output must be usable as a style source for Step4 and Step5.

## Handoff To Next Step
- Save the approved hero image as `fusion_4k`.
- Provide `style_summary` so Step4 and Step5 can restate the visual language succinctly.

## Prohibitions
- Do not use more than 4 source materials unless the controller explicitly overrides.
- Do not introduce unrelated motifs absent from the `Blueprint`.
- Do not flatten the image into a texture wall with no space or depth.

## Reference Map
- Shared schema: [`../references/pipeline-schema.md`](../references/pipeline-schema.md)
- Shared contracts: [`../references/prompt-contracts.md`](../references/prompt-contracts.md)
- Step3 prompt example: [`references/step3-prompt-example.md`](references/step3-prompt-example.md)
