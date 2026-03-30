---
name: art-step1-analyst
description: Use when Codex needs to analyze the A-column image, infer character traits and visual cues, and output a normalized Blueprint JSON for the Feishu OpenClaw art pipeline.
---

# Art Step1 Analyst

Analyze the main uploaded image and convert it into a stable `Blueprint` contract for downstream generation. This skill is the single source of truth for theme, palette, style, composition intent, and material elements.

## Purpose
- Read image `A`.
- Infer persona, clothing cues, mood, color dominance, and usable symbolic elements.
- Convert those observations into a structured design blueprint that Step3-Step5 can consume without reinterpretation.

## Inputs
- `task_id`
- `A` main image URL or attachment
- Optional ratio preference from the table
- Shared schema rules in [`../references/prompt-contracts.md`](../references/prompt-contracts.md)

## Output Schema
Return a `StepResult` JSON object whose `structured_output` is a valid `Blueprint`:

```json
{
  "success": true,
  "step": "step1",
  "artifact_urls": [],
  "structured_output": {
    "theme": "神秘冷酷的占卜师",
    "palette": ["blue-black", "silver", "violet-accent"],
    "style": "dreamlike occult fantasy",
    "material_elements": ["tarot cards", "moon sigils", "glowing smoke"],
    "composition": "hero-centered portrait with layered foreground symbols",
    "lighting": "cold rim light with deep shadow contrast",
    "negative_constraints": ["avoid cartoon anatomy", "avoid muddy background", "avoid text in main artwork"]
  },
  "error_code": "",
  "error_message": ""
}
```

## Prompt Workflow
1. Describe the visible subject factually: clothing, posture, expression, age presentation, props, and standout patterns.
2. Identify the dominant and secondary colors actually supported by the image.
3. Infer a single leading theme phrase that can anchor Step3-Step5.
4. Choose one coherent style phrase, not a list of unrelated aesthetics.
5. Propose 3-6 `material_elements` that are visually producible as background motifs or transparent accessory assets.
6. Add `composition` and `lighting` directions that improve layout consistency.
7. Add 3-5 `negative_constraints` that prevent common drift.
8. Return JSON only.

## Retry Rules
- If the first result is too generic, retry with stronger grounding in visible wardrobe details and color evidence.
- If the theme conflicts with the image, retry using the subject's actual clothing and emotional cues as the anchor.
- If the output is not valid JSON, repair formatting immediately.

## Quality Checks
- `theme` must be singular and specific.
- `palette` must reflect the image instead of random trend colors.
- `material_elements` must be drawable and relevant to the theme.
- `negative_constraints` must block likely failures without banning the whole style.

## Handoff To Next Step
- Write the accepted `Blueprint` JSON into `blueprint_json`.
- Pass the same `Blueprint` unchanged to Step3, Step4, and Step5.

## Prohibitions
- Do not invent a theme unrelated to the image.
- Do not output prose outside the JSON envelope.
- Do not include impossible asset requests such as full scenes in `material_elements`.

## Reference Map
- Shared contracts: [`../references/prompt-contracts.md`](../references/prompt-contracts.md)
- Step1 prompt example: [`references/step1-prompt-example.md`](references/step1-prompt-example.md)
