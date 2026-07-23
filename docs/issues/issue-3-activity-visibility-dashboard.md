# Issue 3 - Activity log, visibility rules, and dashboard summary

## Goal
Add the deal/contact activity layer plus the role-based visibility and dashboard behavior that make the CRM useful in daily use.

## Scope
- Activity log entries on deal and contact records
- Deal detail timeline that merges activities and stage history in chronological order
- Server-side permission checks for view/create/edit/delete
- UI hiding for actions the current role cannot use
- Dashboard summary widgets for counts and pipeline value
- Activity logging for role changes, status changes, deletes/restores, and ownership changes

## UI / architecture rules
- Keep permissions enforced in routes, not just templates
- Use the same shell and card layout as every other module
- Make audit/history views readable and chronological

## Acceptance criteria
- Activities persist and render in reverse-chronological order where appropriate
- Direct navigation obeys role visibility rules
- Audit log entries capture entity type, entity id, action, old/new value, user, and timestamp

