# EdgeBoard Hotfix 2.1

This fixes three launch blockers:

1. Free alpha accounts were incorrectly blocked from `/games` and `/dashboard`.
2. Existing accounts did not become administrators after `ADMIN_EMAIL` was added later.
3. The data refresh waited for the first interval instead of running when the API started.
4. The navigation did not show an Admin link.

## Install

1. Extract this ZIP.
2. Copy the `apps` folder into the root of your existing `edgeboard-v3` repository.
3. Choose **Replace files** for all four matching files.
4. Commit and push to GitHub.
5. Wait for both Render services to redeploy.
6. Log out and log back in.

## Render checks

On `edgeboard-api`, confirm:

- `ADMIN_EMAIL` exactly matches your registered email, with no spaces.
- `ODDS_API_KEY` contains a valid The Odds API key.
- `AUTO_REFRESH_ENABLED` is `true`.
- `NWS_USER_AGENT` contains a real contact email.

After redeployment, open `/live-odds`. The recent pipeline runs will show whether MLB, odds, or weather failed.

The Games page can populate from MLB schedule data even if the odds key is missing. Picks require valid odds data.
