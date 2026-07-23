# Issue 2 - Companies, contacts, deals, and pipeline history

## Goal
Deliver the CRM's core sales workflow: companies, contacts, deals, and auditable stage changes.

## Scope
- Company CRUD with list, get, save, delete
- Contact CRUD linked to a company
- Deal CRUD linked to company and contact
- Pipeline board / grouped deal view
- Stage change action that writes a deal stage history row every time
- Soft delete for records that need audit or relationship integrity

## UI / architecture rules
- Every list page lives in a card container
- Use jQuery DataTables for list screens
- List screen header must show icon + page title on the left and filters + New button on the right
- Row actions must be icon-only buttons with accessible labels

## Acceptance criteria
- A company can be created and linked contacts can be viewed from both directions
- A deal can be created with company, contact, and initial stage
- Moving a deal between stages creates an immutable stage-history record
- The current stage and the full transition history both render correctly

