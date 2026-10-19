# LocalOps AI

LocalOps AI is an offline-first, read-only incident investigation dashboard for developers. Upload a synthetic application log and a source ZIP; it parses the exception, runs bounded source tools, verifies real file/line evidence, and returns a developer-reviewed hypothesis with a traceable remediation checklist.

## What is implemented

- FastAPI API with typed report contracts and health check.
- Safe `.log`/`.txt` and ZIP uploads with size, count, traversal, symlink, and extension checks.
- Deterministic .NET exception/stack-frame parsing.
- Bounded read-only source search and line reader; uploaded code is never executed.
- Offline investigator with a strict tool budget, grounded citations, uncertainty language, and an auditable tool trace.
- React/Vite dashboard with sample incident mode, progress state, evidence cards, trace, and JSON/Markdown export.
- Synthetic ASP.NET-style fixture and pytest/Vitest coverage.

## Quick start

Prerequisites: Python 3.12, Node.js 22.19+, and npm. Copy `.env.example` to `.env` only if you want to configure a future live model endpoint; offline mode needs no key or network.

```bash
python -m venv .venv
. .venv/bin/activate                 # Windows: .venv\\Scripts\\activate
pip install -r backend/requirements.txt
cd frontend && npm ci && cd ..
make test
```

Run the API and frontend in two terminals:

```bash
uvicorn backend.app.main:app --reload --port 8000
cd frontend && npm run dev
```

Open http://localhost:5173 and choose **Try sample incident**, or upload a `.log` plus `.zip` source fixture. The API is http://localhost:8000/docs.

## Docker

Build and run the API image:

```bash
docker build -t localops-ai-api .
docker run --rm --network none -p 8000:8000 localops-ai-api
```

Run the two-service development stack:

```bash
docker compose up --build
```

The backend image contains all backend tests and dependencies. To run the reproducible backend suite in the built image without runtime network access:

```bash
docker run --rm --network none localops-ai-api python -m pytest -q
```

The frontend lockfile is committed; run `npm ci` once during image/dependency setup, then tests do not contact a model or external API.

## Offline semantics and safety

Offline mode is the default and is the acceptance-test path. It uses the real parser, source tools, investigator state transitions, evidence checks, and report builder; only model choice is deterministic. A future live OpenAI-compatible adapter can be configured without changing the report contract. No uploaded code, scripts, shell commands, or generated patches are executed. Suggested fixes always require developer review.

When no matching source is found, the report is `inconclusive` and does not invent file names or line numbers. The supported status means the hypothesis is grounded in returned source evidence, not that production root cause is confirmed.

## Architecture

`Browser → FastAPI upload/storage → parser → bounded investigator → search/read tools → evidence/report → dashboard`. Temporary incident workspaces are isolated from the repository and are read-only to investigation tools.

## Demo walkthrough

1. Start API and frontend.
2. Click **Try sample incident** to show a grounded `System.NullReferenceException` report.
3. Upload `tests/fixtures/incident.log` and a ZIP containing the files in `tests/fixtures/`.
4. Expand **Tool trace** to show parser/search/read chronology.
5. Export JSON or Markdown and show the proposed fix is advisory only.
6. Repeat with a ZIP containing an unrelated source file to demonstrate the `inconclusive` failure-safe path.

## Project checks

`make test` runs `python -m pytest -q` and `cd frontend && npm test -- --run`. Run `npm run build` in `frontend/` for the production bundle. All required tests are deterministic and do not download model weights or call external services.

## Limitations

The MVP uses in-memory incident storage, has no authentication, and the live model adapter is intentionally not enabled. It is designed for synthetic/local evidence, not production incident ingestion. A public GitHub repository, demo recording, and OmniRush session references must be added by the entrant before submission.
