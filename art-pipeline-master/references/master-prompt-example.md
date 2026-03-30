# Master Prompt Example

Use this prompt shape when the controller needs to run one Feishu row through the full workflow.

```text
Use $art-pipeline-master.

Task source:
- row_id: recn123456
- task_id: TASK-20260330-001
- status: pending
- ratio: 16:9
- A: https://example.com/main.png
- B: https://example.com/ref.png
- C: https://example.com/material-1.png
- D: https://example.com/material-2.png
- E:
- F:
- G: 巅峰对决

Execution requirements:
1. Normalize the row into the shared TaskRecord schema.
2. Trigger Step1 and Step2 in parallel.
3. Wait for required dependencies before Step3-Step5.
4. Retry any failing step once using the shared repair rules.
5. Write back all status changes and artifact paths.
6. If Feishu write-back fails, package to exports/{task_id}/ and record the fallback path.
7. Return the final StepResult JSON only.
```
