---
name: art-step2-cutout
description: Use when Codex needs to isolate the main subject from the A-column image, stage it on white, and deliver a transparent PNG plus cutout quality status for the art pipeline.
---

# Art Step2 Cutout

Generate a usable subject cutout from the main image. This skill defines the white-background staging rule and the transparent PNG acceptance checks used by the pipeline.

## Purpose
- Extract the main person or hero subject from image `A`.
- Produce a white-background staging render and a transparent PNG.
- Record whether the output is clean enough for Step3 compositing.

## Inputs
- `task_id`
- `A` main image
- Optional subject notes from Step1 if available after parallel completion
- Shared schema in [`../references/prompt-contracts.md`](../references/prompt-contracts.md)

## Output Schema
```json
{
  "success": true,
  "step": "step2",
  "artifact_urls": [
    "{task_id}/subject_white_bg.png",
    "{task_id}/subject.png"
  ],
  "structured_output": {
    "subject_detected": true,
    "transparent_ready": true,
    "subject_notes": "Full upper body preserved, hair edges softened, no background residue."
  },
  "error_code": "",
  "error_message": ""
}
```

## Prompt Workflow
1. Identify the dominant subject in image `A`.
2. Recreate or refine the subject on a pure white background with strong edge separation.
3. Remove the white background to create a transparent PNG.
4. Preserve hair, accessories, semi-transparent fabric, and fingers where possible.
5. Keep body proportions and costume details faithful to the source.
6. Return paths for both the staging image and the transparent output.

## Retry Rules
- If the first output leaves visible background residue, retry with a stronger clean-edge requirement.
- If parts of the subject are missing, retry with explicit instructions to preserve the full visible silhouette.
- If the transparent PNG still contains solid white fill after retry, fail with `CUTOUT_NOT_TRANSPARENT`.

## Quality Checks
- Subject must remain centered and uncropped unless the source itself is cropped.
- Background must be removable to full transparency without gray fringing.
- White staging image must contain only the subject and a pure white background.
- Transparent output must not contain new props, text, or scene elements.

## Handoff To Next Step
- Save the approved transparent PNG as `subject_png`.
- Provide `subject_notes` for Step3 if extraction constraints matter.

## Prohibitions
- Do not stylize the subject into a different outfit or pose.
- Do not keep source background shadows or clutter.
- Do not return a flattened non-transparent subject as success.

## Reference Map
- Shared contracts: [`../references/prompt-contracts.md`](../references/prompt-contracts.md)
- Shared retry rules: [`../references/error-recovery.md`](../references/error-recovery.md)
- Step2 prompt example: [`references/step2-prompt-example.md`](references/step2-prompt-example.md)
