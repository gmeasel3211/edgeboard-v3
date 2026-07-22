# START HERE

This package is the first complete deployable milestone of EdgeBoard v3.

## Important

Upload the files **inside this folder** to your GitHub repository root.

GitHub must show this at its top level:

```text
.github/
apps/
docs/
.env.example
.gitignore
docker-compose.yml
README.md
render.yaml
START_HERE.md
```

Do not upload the outer folder as an extra nested directory.

## Render

On the Blueprint screen:

- Branch: `main`
- Blueprint Path: leave blank

Render will locate `render.yaml` automatically.

## What is working now

- Public landing and pricing pages
- Registration and login
- JWT-secured subscriber dashboard
- Free/pro/elite subscription data model
- Stripe checkout and webhook routes
- Admin-only board refresh endpoint
- PostgreSQL persistence
- MLB demo model board
- Render Blueprint

## What comes next

Milestone 2 replaces demo MLB data with live odds ingestion, MLB Stats API integration,
scheduled model runs, market history, grading, and a full administrator interface.
