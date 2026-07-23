# Issue 4 - Polish, accessibility, validation, and seed-data completion

## Goal
Finish the CRM with the polish and guardrails needed for a capstone-quality review.

## Scope
- Final seed dataset spanning each stage and key entity relationships
- Search and filter improvements for list pages
- Form validation and empty states
- Accessibility basics: aria-labels, focus states, modal titles, Escape to close
- Confirm-before-delete behavior everywhere
- Test coverage for the core workflows
- Production sanity checks such as no debug mode and no hardcoded secrets

## UI / architecture rules
- Keep all screens on the same palette and shell
- Preserve the single create/edit modal pattern
- Ensure list pages remain DataTable-based and responsive

## Acceptance criteria
- A fresh install has enough demo data to show every stage and object type
- List screens support filtering without leaving the page
- Delete actions always require confirmation
- Basic accessibility requirements are visible and usable

