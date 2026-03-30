# Pipeline Schema

This file defines the shared task model, state machine, naming rules, and package manifest used by all six skills.

## TaskRecord

```json
{
  "row_id": "recn123456",
  "task_id": "TASK-20260330-001",
  "status": "pending",
  "current_step": "",
  "retry_count": 0,
  "ratio": "16:9",
  "A": "main image url or attachment",
  "B": "optional reference image",
  "C": "optional material image",
  "D": "optional material image",
  "E": "optional material image",
  "F": "optional material image",
  "G": "art text input",
  "blueprint_json": "",
  "subject_png": "",
  "fusion_4k": "",
  "asset_1": "",
  "asset_2": "",
  "asset_3": "",
  "art_text_png": "",
  "package_path": "",
  "error_message": ""
}
```

## Status Machine
- `pending`: row is ready to be picked up.
- `running`: master has claimed the row and is currently executing one or more steps.
- `partial_failed`: optional intermediate marker if a step fails before retry. The final implementation may keep this transient or skip direct write-back.
- `completed`: all required outputs exist and have been written back.
- `manual_intervention`: at least one required step failed twice or a storage/write-back error prevented completion.

## Step Order
- `step1_step2_parallel`
- `step3`
- `step4`
- `step5`
- `packaging`

## Filename Convention
- `{task_id}/subject_white_bg.png`
- `{task_id}/subject.png`
- `{task_id}/fusion_4k.png`
- `{task_id}/asset_1.png`
- `{task_id}/asset_2.png`
- `{task_id}/asset_3.png`
- `{task_id}/art_text.png`
- `{task_id}/package_manifest.json`
- `{task_id}/bundle.zip`

## Ratio Defaults
- Default ratio: `16:9`
- Supported values reserved for future expansion:
  - `1:1`
  - `3:4`
  - `4:3`
  - `9:16`
  - `16:9`
  - `456mm*156mm`

## PackageManifest

```json
{
  "task_id": "TASK-20260330-001",
  "generated_at": "2026-03-30T12:00:00+08:00",
  "artifacts": [
    {
      "name": "subject_png",
      "path": "{task_id}/subject.png",
      "source_step": "step2"
    },
    {
      "name": "fusion_4k",
      "path": "{task_id}/fusion_4k.png",
      "source_step": "step3"
    },
    {
      "name": "asset_1",
      "path": "{task_id}/asset_1.png",
      "source_step": "step4"
    },
    {
      "name": "asset_2",
      "path": "{task_id}/asset_2.png",
      "source_step": "step4"
    },
    {
      "name": "asset_3",
      "path": "{task_id}/asset_3.png",
      "source_step": "step4"
    },
    {
      "name": "art_text_png",
      "path": "{task_id}/art_text.png",
      "source_step": "step5"
    }
  ],
  "save_target": "feishu_or_local_fallback",
  "package_path": "{task_id}/bundle.zip"
}
```
