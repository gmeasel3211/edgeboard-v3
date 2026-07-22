# EdgeBoard v3

Commercial-ready sports analytics SaaS foundation.

## Included

- Next.js subscriber-facing frontend
- FastAPI backend
- PostgreSQL-ready database layer
- JWT authentication
- Stripe subscription scaffolding
- Admin-protected API routes
- MLB game board with demo fallback data
- Render Blueprint deployment
- Docker Compose for local development
- GitHub Actions checks

## Repository structure

```text
apps/
  api/   FastAPI backend
  web/   Next.js frontend
render.yaml
docker-compose.yml
```

## Local setup

1. Copy `.env.example` to `.env`.
2. Start PostgreSQL:

```bash
docker compose up db -d
```

3. Start API:

```bash
cd apps/api
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

4. Start web app:

```bash
cd apps/web
npm install
npm run dev
```

Frontend: http://localhost:3000  
API docs: http://localhost:8000/docs

## First administrator

Set `ADMIN_EMAIL` in the API environment. Register an account using that email.
The API automatically grants that account administrator privileges.

## Stripe

Create recurring Stripe prices and set:

- `STRIPE_SECRET_KEY`
- `STRIPE_WEBHOOK_SECRET`
- `STRIPE_PRO_PRICE_ID`
- `STRIPE_ELITE_PRICE_ID`

Webhook endpoint:

```text
/api/v1/billing/webhook
```

## Render deployment

Commit this project to the root of a GitHub repository. In Render choose:

**New → Blueprint → select repository**

Render reads `render.yaml` and creates:

- PostgreSQL database
- FastAPI web service
- Next.js web service

After deployment, set the frontend `NEXT_PUBLIC_API_URL` to the public API URL if Render does not resolve it automatically.
