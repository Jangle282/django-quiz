---
name: implement-plan-phase
description: 'Implement one phase from agents/implementation_plan.md in this Django quiz repo. Use when the user names a phase or phase subsection and wants an agent that has already read agents/AGENTS.md, agents/user_journeys.md, agents/implementation_plan.md, and api-contract.yaml, then is ready to build that slice with tests, contract alignment, and focused validation.'
argument-hint: 'Phase or subsection to implement, for example: Phase 3.1 health endpoint, Phase 2 models, or Phase 7 start game endpoint'
user-invocable: true
---

# Implement Plan Phase

## What This Skill Does

This skill prepares the agent to implement one named phase or subsection from `agents/implementation_plan.md` for this repository.

It assumes the agent will first ground itself in the local project constraints:

- `agents/AGENTS.md` for architecture and testing standards
- `agents/user_journeys.md` for user-facing behavior and error cases
- `agents/implementation_plan.md` for the requested phase scope
- `api-contract.yaml` for API shape and contract checks
- `frontend/src/api/` and the affected frontend pages/components when backend behavior must match existing client expectations

Use this skill when the user wants implementation work, not just planning.

This repository is a learning and portfolio project rather than a production system. Prefer choices that make the Django implementation clear, idiomatic, and easy to learn while still honoring the contract and existing frontend integration points.

The agent should still call out production-oriented complexity when it is relevant, but should treat it as context, tradeoff analysis, or optional follow-up unless the current phase explicitly requires implementing it.

## When To Use

Use this skill when the request includes any of these intents or trigger phrases:

- implement phase
- build phase
- start Phase 1, 2, 3, 5, 6, or 7
- implement subsection such as `3.1` or `6.2`
- create backend slice from the plan
- pick up next phase from `agents/implementation_plan.md`
- add the Django code, tests, and contract alignment for a named phase

Do not use this skill for broad architecture brainstorming, frontend-only work unrelated to the phase plan, or generic code review.

## Required Inputs

The user must specify which phase or subsection to implement.

Examples:

- `Phase 1.1`
- `Phase 3.1 health endpoint`
- `Phase 3.3 register and login endpoints`
- `Phase 7 start new game endpoint`

If the user names a broad phase with multiple large subsections, narrow it to the smallest independently testable slice before editing.

## Procedure

1. Read the controlling requirements.
   - Read the relevant section in `agents/implementation_plan.md`.
   - Read the adjacent standards in `agents/AGENTS.md`.
   - Read the matching user journeys in `agents/user_journeys.md`.
   - Read `api-contract.yaml` for the endpoints, schemas, status codes, and field names touched by the phase.

2. Define the exact implementation slice.
   - Restate the named phase as concrete deliverables: models, endpoints, services, tests, docs, infrastructure, or frontend compatibility work.
   - Separate mandatory items from optional follow-up.
   - Choose one smallest valuable slice if the phase is too large for a single pass.

3. Find the local ownership points before editing.
   - Identify the nearest code that directly controls the requested behavior.
   - Prefer the owning model, service, repository, serializer, view, route, migration, or test module over broad exploration.
   - If the backend does not exist yet, start by creating the minimal project structure needed for the requested slice.

4. Check for contract and standards conflicts.
   - If `implementation_plan.md`, `AGENTS.md`, `user_journeys.md`, and `api-contract.yaml` disagree, treat the conflict as blocking.
   - Surface the mismatch clearly and ask the user which source should win before implementing ambiguous behavior.
   - If the conflict is only naming or placement and the intended behavior is still clear, choose the smallest standards-compliant solution and note it.

5. Identify production-oriented concerns without defaulting to implementation.
   - Note relevant production concerns such as token rotation strategy, secret handling, observability, retry behavior, background work, caching, migrations at scale, API hardening, or deployment implications when they materially affect the design.
   - Keep these concerns concise and separate from the core learning implementation.
   - Only implement them when the phase requires them or the user explicitly asks for the production-grade version.

6. Implement from the root cause.
   - Keep controllers or views slim.
   - Put business logic in service classes.
   - Use repository classes for database interactions.
   - Keep throttling centralized rather than duplicated per endpoint.
   - Reuse validation rules for username and password instead of duplicating them.
   - Keep changes minimal and consistent with the existing codebase.

7. Add or update tests immediately around the edited slice.
   - Feature tests cover authentication, authorization, validation, throttling behavior, and response shape.
   - Unit tests cover service logic and persistence behavior.
   - Prefer real database-backed tests with transactions, matching the repo standards.
   - If the slice is infrastructure-only, add the narrowest executable validation available.

8. Validate right after the first substantive edit.
   - Run the narrowest relevant test or check first.
   - Then run any needed focused lint, typecheck, migration check, or contract-related validation for the touched slice.
   - If Swagger or OpenAPI generation is part of the phase, verify the generated result still conforms to `api-contract.yaml`.

9. Finish only when the slice is implementation-ready.
   - Code compiles or runs in the touched area.
   - Tests for the changed behavior pass, or any blocker is explicitly identified.
   - API responses match the contract.
   - The implementation follows the Django architecture and testing standards in `agents/AGENTS.md`.

## Decision Rules

### If the user names a phase without a subsection

- Always stop and ask which subsection to implement before editing.
- Do not choose a subsection automatically, even if one seems like the obvious starting point.

### If the backend skeleton does not exist yet

- Build only the minimum structure needed to support the requested phase.
- Do not scaffold unrelated app domains just because later phases mention them.

### If the frontend already depends on an endpoint shape

- Compare the plan and contract against `frontend/src/api/` and the consuming pages.
- Keep the implementation backend-first.
- Treat the frontend as a fixed integration target used to verify that the Django backend can plug into the existing SPA.
- Only change frontend code when it is necessary to maintain compatibility, repair drift, or support an intentional contract-aligned adjustment.
- Preserve the contract-facing behavior unless the user explicitly wants a coordinated contract change.

### If production-grade concerns are relevant but not required

- Mention them explicitly so the user learns what would matter in a real deployment.
- Keep them out of the implementation unless the named phase requires them or the user asks for them.
- When useful, separate the answer into `implement now` and `production follow-up` so the learning path stays clear.

### If a phase is too large for one safe implementation pass

- Split it into the smallest vertical slice that includes code, tests, and validation.
- State what remains out of scope for the next pass.

### If validation fails

- Repair the same slice first.
- Re-run the same focused validation before widening scope.

## Quality Bar

A phase implementation is not complete unless these are true:

- Behavior matches the named phase and the relevant user journey.
- Responses, request fields, and status codes match `api-contract.yaml`.
- Architecture follows the repo standards: slim controllers, services for logic, repositories for persistence.
- Authentication, authorization, and throttling rules are enforced where required.
- Tests exist for the changed behavior.
- Validation has been run on the touched slice.
- Relevant production-oriented concerns were noted when they materially affect the design, even if they were not implemented.

## Completion Checklist

- Requested phase or subsection is clearly identified.
- Relevant plan, journey, standards, and contract files were read.
- Smallest testable implementation slice was chosen.
- Code was added or updated in the owning layer.
- Tests were added or updated.
- Focused validation was executed.
- Any remaining ambiguity, follow-up work, or blockers were called out explicitly.

## Example Prompts

- `/implement-plan-phase Phase 1.1`
- `/implement-plan-phase Phase 3.1 health endpoint`
- `/implement-plan-phase Implement Phase 3.3 registration endpoint only`
- `/implement-plan-phase Start Phase 7 with POST /api/games`