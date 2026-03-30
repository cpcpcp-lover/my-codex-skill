# Error Recovery

Use this file to keep retry behavior consistent across the full pipeline.

## Retry Policy
- Every required step gets one normal attempt and one repair attempt.
- The repair attempt must change the prompt in response to the previous failure.
- If the repair attempt fails, stop the pipeline and mark `manual_intervention`.

## Repair Mapping

| Error code | Repair instruction |
| --- | --- |
| `INPUT_MISSING` | Re-read the row and confirm whether the task should stay pending or fail fast. |
| `BLUEPRINT_INVALID` | Rebuild Step1 output as strict JSON and ground theme/color/style in the source image. |
| `CUTOUT_SUBJECT_MISSING` | Tell Step2 to preserve the full visible silhouette and all key accessories. |
| `CUTOUT_NOT_TRANSPARENT` | Tell Step2 to enforce pure white staging and remove all white residue before returning success. |
| `FUSION_STYLE_DRIFT` | Tell Step3 to reduce source count, restate the Blueprint, and keep one dominant style direction. |
| `FUSION_RATIO_INVALID` | Tell Step3 to regenerate at the exact target ratio and 4K output size. |
| `ASSET_SET_MISMATCH` | Tell Step4 to choose three distinct objects tied directly to `Blueprint.material_elements`. |
| `ASSET_NOT_TRANSPARENT` | Tell Step4 to isolate each asset on white and remove any halo or fill before success. |
| `TYPOGRAPHY_UNREADABLE` | Tell Step5 to raise text brightness, simplify ornament, and prioritize stroke clarity. |
| `TYPOGRAPHY_NOT_TRANSPARENT` | Tell Step5 to restage on white and clean the alpha before returning success. |
| `WRITEBACK_FAILED` | Retry once, then save locally under `exports/{task_id}/` and mark fallback in the manifest. |
| `PACKAGE_FAILED` | Retry packaging from existing accepted artifacts without regenerating the images. |

## Manual Intervention Rule
Mark `manual_intervention` when:
- a required step fails twice
- artifact storage fails after retry
- write-back and local fallback both fail
- upstream outputs are contradictory or corrupted

When marking `manual_intervention`, write:
- `status=manual_intervention`
- `current_step=<failed step>`
- `error_message=<error code>: <short diagnosis>`

## Idempotency Rule
- Never rerun a step that already produced an accepted artifact unless the repair attempt explicitly replaces that same step.
- Never regenerate upstream artifacts just to repair packaging or write-back.
