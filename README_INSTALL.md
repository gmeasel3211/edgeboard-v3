# EdgeBoard Pick Reasoning Hotfix

Adds:

- One best-price recommendation instead of duplicate sportsbook cards
- A visible Why this bet section
- Break-even probability and best-line value
- Team record and run-differential reasoning
- Probable-pitcher comparison when available
- Data-quality warnings
- Primary risks
- No market-only picks when team data is missing
- Lower confidence and stake when pitcher information is incomplete

## Install

1. Extract this ZIP.
2. Copy `install_hotfix.py` into the root of your `edgeboard-v3` folder.
3. Open PowerShell or Command Prompt in that folder.
4. Run `python install_hotfix.py`.
5. Commit and push the changed files.
6. Wait for both Render services to redeploy.
7. Open `/admin`.
8. Click **Rebuild card**.

Existing cards keep their old generic text until the card is rebuilt.

This update only explains data the current model actually has. It does not pretend bullpen, lineup, injury, Statcast, or pitch-mix analysis exists before Milestone 4.
