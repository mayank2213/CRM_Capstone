# Issue 1 - Scaffold, schema, and auth foundation

## Goal
Build the Flask foundation for the CRM so every later module sits on the same app structure.

## Scope
- Create the Flask application factory, config, and extension wiring
- Add one blueprint per module: auth, companies, contacts, deals, activities
- Add the shared shell layout with persistent sidebar + header
- Define the core database models and migration setup
- Add login/logout and password hashing support if multi-user auth is enabled
- Add seed data for a working demo environment

## UI / architecture rules
- Keep all pages inside the shared card-based shell
- Use Bootstrap Icons only
- Do not place business logic in templates
- Use one consistent modal pattern for create/edit later in the project

## Acceptance criteria
- App starts cleanly from `run.py`
- Blueprints are registered and routable
- Database extension and migration wiring are in place
- A fresh install can load demo data without manual fixes

