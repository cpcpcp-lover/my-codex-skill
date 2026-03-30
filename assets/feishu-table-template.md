# Feishu Table Template

Create one table for task intake and result write-back with these recommended fields.

| Column | Field name | Type | Required | Notes |
| --- | --- | --- | --- | --- |
| A | 主图 | attachment | No | Main subject image for Step1 and Step2. |
| B | 溶图参考图 | attachment | No | Optional style reference. |
| C | 素材1 | attachment | No | Fusion material input. |
| D | 素材2 | attachment | No | Fusion material input. |
| E | 素材3 | attachment | No | Fusion material input. |
| F | 素材4 | attachment | No | Fusion material input. |
| G | 艺术字文案 | single line text | No | Exact text for Step5. |
| H | task_id | single line text | Yes | Unique task identifier. |
| I | status | single select | Yes | `pending`, `running`, `partial_failed`, `completed`, `manual_intervention`. |
| J | current_step | single line text | No | Current pipeline step. |
| K | retry_count | number | No | Current retry count for the active step. |
| L | ratio | single select | No | Default `16:9`; future-ready. |
| M | blueprint_json | long text | No | Raw Step1 Blueprint JSON. |
| N | subject_png | attachment or URL | No | Approved transparent subject output. |
| O | fusion_4k | attachment or URL | No | Approved Step3 hero image. |
| P | asset_1 | attachment or URL | No | Approved Step4 asset. |
| Q | asset_2 | attachment or URL | No | Approved Step4 asset. |
| R | asset_3 | attachment or URL | No | Approved Step4 asset. |
| S | art_text_png | attachment or URL | No | Approved Step5 typography output. |
| T | package_path | single line text | No | Bundle location in Feishu or local fallback. |
| U | error_message | long text | No | Final failure summary when manual intervention is required. |

## Row Ready Rule
A row is considered ready when:
- `status=pending`
- at least one of `A-F` contains an attachment
- `task_id` is present

## Suggested Views
- `待处理`: filter `status = pending`
- `运行中`: filter `status = running`
- `需人工干预`: filter `status = manual_intervention`
- `已完成`: filter `status = completed`
