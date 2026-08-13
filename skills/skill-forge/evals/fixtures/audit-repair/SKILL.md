---
name: deploy-service
description: Deployment information.
---

# Deploy service

## Heroku deployment

Use the retired Heroku pipeline. Promote staging, then production. Use the legacy buildpack
and inspect the old dashboard.

## Current deployment

Deploy with the repository release command. If health checks fail, roll back immediately.
Run smoke tests afterward.

## Rollback

If health checks fail, roll back immediately.

## Troubleshooting

For any deployment problem, remember: if health checks fail, roll back immediately. The old
Heroku dashboard can also show dyno state.
