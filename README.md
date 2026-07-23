# CRM Capstone

Python/Flask CRM capstone scaffold for RPATech.

## Structure

- `app/` application package
- `app/blueprints/` module blueprints for auth, companies, contacts, deals, and activities
- `app/templates/` shared shell and module pages
- `app/static/` shared CSS and JavaScript
- `tests/` smoke and regression tests

## UI rules

- Shared header + collapsible sidebar shell
- Module content rendered inside a card container
- Bootstrap Icons only
- jQuery DataTables for list views
- One modal for create/edit per object
- Soft delete and audit logging for important records

## Run

1. Create a virtual environment.
2. Install dependencies from `requirements.txt`.
3. Run `python run.py`.

