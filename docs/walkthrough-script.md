# LocalOps AI walkthrough

Target length: 2 minutes 30 seconds. Record the browser at 1080p with the API and frontend already running (or use the deployed Render URL). Keep the narration conversational and show the UI, not private account details.

## Before recording

1. Open the LocalOps AI dashboard.
2. Confirm the API indicator is connected.
3. Have `tests/fixtures/incident.log` and a ZIP containing `OrderService.cs` and `OrdersController.cs` ready.
4. Keep a second ZIP containing only an unrelated source file ready for the failure-safe example.
5. Do not show API keys, personal tokens, browser profile data, or private repositories.

## Shot list and narration

### 0:00–0:20 — The problem

“When an incident arrives, a stack trace tells us where the failure surfaced, but not whether the source evidence supports a cause. LocalOps AI gives developers a bounded, read-only investigation with citations instead of an overconfident answer.”

Show the dashboard headline and the **Read-only by design** message.

### 0:20–0:40 — Provide evidence

“I’ll upload one synthetic .NET application log and the matching source fixture. Uploaded code is never executed.”

Upload the log and source ZIP. Briefly show both files in the input panel, then click **Start investigation**.

### 0:40–1:10 — Follow the bounded run

“The investigator parses the exception, searches for the stack-frame symbol, reads only bounded source lines, and preserves every tool call in the trace.”

Show the progress panel, then expand **Tool trace**. Pause briefly over the parser/search/read rows.

### 1:10–1:40 — Review grounded evidence

“The result is a supported hypothesis because the cited file and line range came from the uploaded source. Supported does not mean production root cause confirmed.”

Show `System.NullReferenceException`, the probable cause, and the `OrderService.cs` citation. Scroll through the excerpt and rationale.

### 1:40–2:00 — Remediation stays developer-controlled

“LocalOps suggests a narrow guard and a validation checklist, but it never applies a patch or writes to the repository.”

Show **Proposed fix** and **Validation steps**. Click JSON export, then Markdown export if desired.

### 2:00–2:20 — Failure-safe behavior

“Now I’ll use an unrelated source archive. With no matching evidence, the system says it is inconclusive and does not invent a filename or line number.”

Run the unrelated ZIP case and show the inconclusive state and warning.

### 2:20–2:30 — Reproducibility takeaway

“The workflow is offline-first and reproducible: the parser, real source tools, bounded investigator, evidence checks, and tests run without a model download or external API.”

End on the report or README’s Docker/test commands.

## Suggested title and description

**Title:** LocalOps AI — Evidence-backed incident investigation, offline-first

**Description:** LocalOps AI analyzes synthetic application logs and source fixtures with bounded, read-only tools. It returns grounded file/line evidence, uncertainty-aware hypotheses, remediation suggestions, validation steps, and an auditable tool trace. No uploaded code is executed and no patches are applied automatically.

## Submission checklist

- [ ] Video is 2–3 minutes and accessible by an unlisted/public link.
- [ ] The deployed URL or local URL is visible and works in a private browser window.
- [ ] Known incident and inconclusive incident are both shown.
- [ ] No secrets, personal data, or private repository contents appear.
- [ ] Narration states that output is developer-reviewed and not confirmed production root cause.
