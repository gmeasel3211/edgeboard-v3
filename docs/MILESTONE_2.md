# Milestone 2 architecture

## Refresh sequence

1. MLB schedule and standings
2. Probable-pitcher season statistics
3. FanDuel and DraftKings odds
4. Stadium weather
5. Market-aware card generation

## Model philosophy

The initial model deliberately anchors projections to no-vig market consensus. Team run
differential, starting-pitcher performance, and home field shift that baseline. This reduces
the false precision that would come from treating a small set of public statistics as a mature
predictive system.

## Stored history

`odds_snapshots` stores bookmaker, market, selection, price, line, source update time, and
capture time. This supports future line movement and closing-line value features.

## Next milestone

- Market matching improvements between Odds API and MLB game IDs
- Run-line and total projections
- bullpen usage/fatigue
- offensive rolling windows
- official card lifecycle
- score-based grading
- closing-line capture
- backtesting and calibration
- performance dashboard
