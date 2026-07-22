# EdgeBoard Milestone 2 — Update Instructions

## Upload

This package replaces Milestone 1.

1. Extract the ZIP.
2. Open the extracted `edgeboard-v3-milestone-2` folder.
3. Copy everything inside it into your local `edgeboard-v3` repository.
4. Choose **replace files** when Windows asks.
5. Commit and push all changes to GitHub.

Do not upload the ZIP itself.

## Render variables

Add these to the `edgeboard-api` service:

```text
ODDS_API_KEY=your-key
NWS_USER_AGENT=EdgeBoard/3.1 (your-email@example.com)
```

Your existing `ADMIN_EMAIL` remains required.

## Verify deployment

- API health: `/health`
- Pipeline status: `/api/v1/system/status`
- Frontend game board: `/games`
- Frontend status: `/live-odds`
- Admin operations: `/admin`

## Generate the first live card

Register or log in with the administrator email, open `/admin`, and click **Full refresh**.

## Data policy

The code stores every fetched line snapshot. Ensure your commercial use complies with the
terms and licensing of every data provider and sportsbook data source.
