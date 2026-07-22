# EdgeBoard v3 — Milestone 2

Milestone 2 turns the deployable SaaS foundation into a live MLB data platform.

## Added in this milestone

- The Odds API v4 integration
- FanDuel and DraftKings filtering
- Moneyline, spread, and total snapshots
- Persistent historical odds storage
- MLB schedule, standings, probable pitchers, scores, and season pitching statistics
- National Weather Service hourly forecasts for outdoor parks
- MLB stadium coordinates, roof status, and baseline park factors
- Automated refresh pipeline
- APScheduler refresh loop
- Market-aware moneyline projection
- No-vig probability calculation
- Edge, EV, confidence, and fractional Kelly sizing
- Subscriber game board
- Game-detail pages
- Live pipeline status
- Administrator refresh center

## Important limitation

This milestone creates a real data and modeling pipeline, but it is not yet a validated betting model.
Do not market projections as guaranteed or proven. Milestone 3 will add calibration, backtesting,
bet grading, closing-line tracking, expanded markets, and performance analytics.

## Update an existing Milestone 1 repository

Replace the old repository files with the contents of this package, or copy these files over the
existing project and allow matching files to be overwritten. Commit and push to `main`.
Render will redeploy automatically from the updated `render.yaml`.

## Required Render environment variables

- `ADMIN_EMAIL`
- `ODDS_API_KEY`
- `NWS_USER_AGENT` — example: `EdgeBoard/3.1 (you@example.com)`

Stripe variables can remain blank until billing is configured.

## First live refresh

After deployment:

1. Register using `ADMIN_EMAIL`.
2. Visit `/admin`.
3. Click **Full refresh**.
4. Visit `/live-odds` and `/games`.

The scheduled refresh then runs every 10 minutes while the API service is awake.
