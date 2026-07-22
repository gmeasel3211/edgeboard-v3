# Render deployment checklist

1. Extract the ZIP.
2. Upload the **contents inside** `edgeboard-v3-foundation` to the root of a new GitHub repository.
3. Verify GitHub displays `render.yaml` at the top level.
4. In Render choose **New → Blueprint**.
5. Select the repository and branch `main`.
6. Leave Blueprint Path blank; Render defaults to `/render.yaml`.
7. Set secret environment variables when prompted.
8. Deploy.
9. Register using the `ADMIN_EMAIL` address.
10. Configure Stripe only after the base app is online.

## Required before public launch

- Replace all generated/default secrets.
- Connect a custom domain.
- Configure transactional email.
- Add Terms, Privacy Policy, and responsible gambling disclosures.
- Confirm sportsbook/data licensing.
- Use paid Render plans for reliable production uptime.
