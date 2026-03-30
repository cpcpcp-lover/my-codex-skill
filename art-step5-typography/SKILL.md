---
name: art-step5-typography
description: Use when Codex needs to create transparent artistic typography from the Step3 hero image and the G-column text input for the Feishu OpenClaw art pipeline.
---

# Art Step5 Typography

Generate one transparent artistic text composition that inherits the color, texture, and lighting language of the hero artwork while keeping the input text readable.

## Purpose
- Read `fusion_4k` as the visual style source.
- Read `G` as the exact text content.
- Choose the most suitable typography preset among metallic, gothic, or felt-like treatment.
- Produce one transparent PNG art-text output.

## Inputs
- `task_id`
- `fusion_4k`
- `Blueprint`
- `G` input text

## Output Schema
```json
{
  "success": true,
  "step": "step5",
  "artifact_urls": [
    "{task_id}/art_text.png"
  ],
  "structured_output": {
    "preset": "gothic",
    "brightness_adjusted": true,
    "readability_notes": "Primary strokes lifted above background tone; contrast improved on inner glow."
  },
  "error_code": "",
  "error_message": ""
}
```

## Prompt Workflow
1. Read `fusion_4k` and extract its palette, material feel, and light behavior.
2. Read the exact `G` text and preserve its wording.
3. Choose one preset:
   - metallic
   - gothic
   - felt
4. Build text with depth, weight contrast, breathing room, and controlled mixed layout.
5. Increase text brightness if the hero palette is too dark for readability.
6. Stage on pure white and remove the background to transparent.
7. Return StepResult JSON only.

## Retry Rules
- If readability is poor, retry with stronger contrast and simplified ornament density.
- If the style clashes with the hero artwork, retry with a preset switch and tighter palette extraction.
- If the transparent PNG keeps white residue, retry with stricter clean-background instructions.

## Quality Checks
- Text must stay legible at intended usage size.
- Decorative treatment must support, not obscure, the words.
- Palette should clearly originate from the hero image.
- Final output must be transparent-ready.

## Handoff To Next Step
- Save the accepted output as `art_text_png`.
- Pass only the final artifact path and notes back to the master skill.

## Prohibitions
- Do not paraphrase or translate the input text unless explicitly instructed.
- Do not generate multiple style variants in one run.
- Do not sacrifice legibility for ornament.

## Reference Map
- Shared contracts: [`../references/prompt-contracts.md`](../references/prompt-contracts.md)
- Shared retry rules: [`../references/error-recovery.md`](../references/error-recovery.md)
- Step5 prompt example: [`references/step5-prompt-example.md`](references/step5-prompt-example.md)
