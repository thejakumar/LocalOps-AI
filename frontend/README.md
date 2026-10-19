# LocalOps AI frontend

React + TypeScript + Vite dashboard for the LocalOps incident investigator. The UI follows the backend contract documented by the project: `POST /api/incidents` (multipart `log` and `source`), `POST /api/incidents/:id/investigate`, and `GET /api/incidents/:id/report`.

## Run locally

```bash
npm ci
npm run dev
```

Vite proxies `/api` and `/health` to `http://localhost:8000`. Set `VITE_API_URL` when the API is hosted elsewhere.

## Check and build

```bash
npm test
npm run build
```

The **Try sample incident** action provides a reviewable UI demonstration without pretending that a backend run occurred. The upload flow reports API failures directly and never fabricates a report.

## Docker

```bash
docker run --rm -p 8080:80 localops-ai-frontend
```
