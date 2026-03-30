---
name: art-pipeline-master
description: Use when Codex needs to orchestrate the full Feishu OpenClaw art pipeline: detect new sheet tasks, validate A-G inputs, run Step1-Step5 in order, manage retries, write back status, and package final outputs.
---

# Art Pipeline Master

Coordinate the end-to-end OpenClaw art workflow for one Feishu table row at a time. Treat this skill as the only controller allowed to change task status, trigger downstream skills, and decide whether to retry or mark `manual_intervention`.

## Purpose
- Watch for rows whose `status` is `pending` and that contain at least one usable source input in `A` or `B-F`, plus optional text in `G`.
- Normalize the row into the shared `TaskRecord` contract in [`../references/pipeline-schema.md`](../references/pipeline-schema.md).
- Start Step1 and Step2 in parallel, then gate Step3, Step4, and Step5 on their required upstream outputs.
- Retry any failed step once using the repair rules in [`../references/error-recovery.md`](../references/error-recovery.md).
- Write all outputs, final status, and package location back to Feishu or the local fallback path.

## Inputs
- One Feishu table row mapped to the `TaskRecord` schema.
- Shared contracts from [`../references/prompt-contracts.md`](../references/prompt-contracts.md).
- Shared retry and escalation rules from [`../references/error-recovery.md`](../references/error-recovery.md).
- Optional ratio field. If absent, default to `16:9`.

## Output Schema
Return a `StepResult` JSON object for the master orchestration step:

```json
{
  "success": true,
  "step": "master",
  "artifact_urls": [
    "{task_id}/subject.png",
    "{task_id}/fusion_4k.png",
    "{task_id}/asset_1.png",
    "{task_id}/asset_2.png",
    "{task_id}/asset_3.png",
    "{task_id}/art_text.png"
  ],
  "structured_output": {
    "task_id": "TASK-20260330-001",
    "final_status": "completed",
    "package_manifest_path": "{task_id}/package_manifest.json",
    "package_path": "{task_id}/bundle.zip"
  },
  "error_code": "",
  "error_message": ""
}
```

## Workflow
1. Validate the row. Refuse to start if all of `A`, `B`, `C`, `D`, `E`, and `F` are empty.
2. Set `status=running`, `current_step=step1_step2_parallel`, `retry_count=0`.
3. Trigger `$art-step1-analyst` and `$art-step2-cutout` in parallel against the same `task_id`.
4. Wait for Step1. Step3 must not start without a valid `Blueprint` JSON.
5. Wait for Step2 only when `A` exists. If `A` is empty, Step3 may continue without a subject cutout.
6. Trigger `$art-step3-fusion` with the approved `Blueprint`, optional subject PNG, and B-F materials.
7. Trigger `$art-step4-assets` with the Step3 hero image plus `Blueprint.material_elements`.
8. Trigger `$art-step5-typography` with the Step3 hero image plus `G` text input.
9. Package all successful outputs into `{task_id}/bundle.zip` and generate `package_manifest.json`.
10. Write result paths, status, and errors back to Feishu. If Feishu write-back fails, store the package under `exports/{task_id}/` and record that fallback in `package_path`.

## Retry Rules
- Allow exactly one automatic retry per failed step.
- The retry must add a targeted repair constraint instead of repeating the same prompt unchanged.
- If the second attempt fails, set:
  - `status=manual_intervention`
  - `current_step=<failed step>`
  - `error_message=<concise diagnosis + last error code>`
- Never rerun a step that already produced an accepted artifact.

## Quality Checks
- Confirm that each downstream step reads the latest approved upstream outputs only.
- Confirm all expected filenames follow the naming convention in [`../references/pipeline-schema.md`](../references/pipeline-schema.md).
- Confirm `artifact_urls` and write-back fields are populated only after the artifact exists.
- Confirm `completed` is used only when all required deliverables exist.

## Handoff To Next Step
- Step1 receives `task_id` and image `A`.
- Step2 receives `task_id` and image `A`.
- Step3 receives `task_id`, `Blueprint`, optional `subject_png`, and materials `B-F`.
- Step4 receives `task_id`, `Blueprint.material_elements`, and `fusion_4k`.
- Step5 receives `task_id`, `fusion_4k`, `Blueprint`, and `G`.

## Prohibitions
- Do not skip failed-step reporting.
- Do not overwrite successful outputs from earlier accepted runs.
- Do not mark `completed` when any required artifact is missing.
- Do not swallow errors from Feishu, storage, or downstream skills.

## Reference Map
- Shared schema: [`../references/pipeline-schema.md`](../references/pipeline-schema.md)
- Shared JSON contracts: [`../references/prompt-contracts.md`](../references/prompt-contracts.md)
- Shared retry policy: [`../references/error-recovery.md`](../references/error-recovery.md)
- Feishu table template: [`../assets/feishu-table-template.md`](../assets/feishu-table-template.md)
- Master prompt example: [`references/master-prompt-example.md`](references/master-prompt-example.md)
