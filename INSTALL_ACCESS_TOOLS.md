# EdgeBoard Admin Views + Friend Invites

## What this adds

### Admin plan preview
The administrator can switch between:

- Actual Admin
- Free
- Pro
- Elite

The selected preview is stored only in the admin's browser. It does not change the real subscription attached to the account. API calls include an `X-EdgeBoard-View-As` header so protected features can behave like the selected plan.

### Downsized friend invite codes
The Admin page can generate a signed Pro or Elite code valid for 7, 30, 60, or 90 days.

A friend:

1. Opens `/register`
2. Creates an account
3. Pastes the code
4. Receives the selected plan

The code is signed using the existing `SECRET_KEY`, so nobody can edit the plan or expiration without invalidating it.

## Installation

1. Extract this ZIP.
2. Copy the included `apps` folder into the root of the existing `edgeboard-v3` repository.
3. Replace matching files.
4. Add the new files.
5. Commit and push to GitHub.
6. Wait for both Render services to redeploy.
7. Log out, then log back in.
8. Open `/admin`.

## Important limitation

This deliberately small beta-code system does not track usage counts or individual redemptions yet. A valid code can be reused until it expires. Only send codes to people you trust. Usage limits, revocation, redemption history, and email delivery belong in the full Milestone 5/7 invite center.

## Layout note

To show the yellow preview banner on every page, import and render `PlanViewBanner` in the site's root layout. The core preview controls and API header work without it, but the banner makes it obvious when preview mode is active.
