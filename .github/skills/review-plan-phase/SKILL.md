---
name: review-plan-phase
description: 'Review one implemented phase or subsection from agents/implementation_plan.md in this Django quiz repo. Use when the user wants a code review that checks plan coverage, api-contract alignment, tests, repo standards, production follow-up notes, common Django gotchas for the topic, and similarities or differences versus PHP Laravel approaches.'
argument-hint: 'Phase or subsection to review, for example: Phase 3.1 health endpoint, Phase 3.3 auth endpoints, or Phase 2 models'
user-invocable: true
---

# Review Plan Phase

## What This Skill Does

This skill reviews one implemented phase or subsection from `agents/implementation_plan.md` for this repository.

It is designed for a learning-oriented Django backend project where the user also wants to understand:

- whether the code matches the implementation plan
- whether it conforms to `api-contract.yaml`
- whether tests and validation are adequate
- what production-oriented concerns matter later
- what common Django gotchas apply to the current topic
- how the current Django approach is similar to or different from a PHP Laravel implementation

Use this skill for review and learning synthesis, not for doing the implementation itself.

## When To Use

Use this skill when the request includes intents or trigger phrases like:

- review phase
- audit phase implementation
- check Phase 3.1 or 3.3
- review a completed plan slice
- compare Django approach to Laravel
- highlight Django gotchas for this endpoint or model work
- identify missing tests, contract drift, or auth issues

Do not use this skill for broad repo review with no phase target, or for implementation requests that should use the implementation skill instead.

## Required Inputs

The user must specify which phase or subsection to review.

Examples:

- `Phase 2.2`
- `Phase 3.1 health endpoint`
- `Phase 3.3 registration endpoint`
- `Phase 7 start game endpoint`

If the user names only a broad phase, stop and ask which subsection to review before proceeding.

## Procedure

1. Read the controlling requirements.
   - Read the relevant section in `agents/implementation_plan.md`.
   - Read `agents/AGENTS.md` for architecture and testing standards.
   - Read the matching behavior in `agents/user_journeys.md`.
   - Read `api-contract.yaml` for the affected endpoints, schemas, status codes, and field names.

2. Read the implementation slice.
   - Find the owning code paths for the named phase: models, migrations, repositories, services, serializers, views, routes, tests, or config.
   - Prefer the local code that directly controls the behavior over broad exploration.

3. Review against the planned scope.
   - Check which required deliverables from the phase are fully implemented.
   - Identify missing requirements, scope drift, or partially implemented items.
   - Distinguish must-fix findings from optional follow-up.

4. Review against repo standards.
   - Check for slim controllers or views, service-layer logic, repository usage, centralized throttling, reusable validation, and appropriate test layering.
   - Verify the implementation matches the Django architecture and testing standards in `agents/AGENTS.md`.

5. Review contract and behavior alignment.
   - Compare request fields, response shapes, status codes, auth behavior, and error handling against `api-contract.yaml` and the relevant user journey.
   - Call out contract drift, naming drift, or frontend compatibility risk.

6. Review validation and tests.
   - Check whether the implementation has the expected feature tests and service or unit tests.
   - Highlight gaps in authentication, authorization, validation, throttling, persistence, or response assertions.
   - Run the narrowest relevant validation available when the environment supports it.

7. Add learning notes.
   - Summarize the production-oriented concerns that matter for this topic, but distinguish them from current must-fix issues.
   - Highlight common Django gotchas for the current area.
   - Compare the Django approach with the likely PHP Laravel equivalent so the user can transfer concepts.

8. Report findings in review order.
   - Findings first, ordered by severity.
   - Open questions or assumptions second.
   - Short summary of what is correct and what remains afterward.

## Review Output Shape

Structure the review using these sections when relevant:

1. `Findings`
   - Bugs, regressions, missing requirements, contract mismatches, security issues, or missing tests.

2. `Open questions`
   - Ambiguities in the plan, contract, or current implementation.

3. `Learning notes`
   - `Production follow-up`: important in a real deployment, but not necessarily required now.
   - `Django gotchas`: framework-specific pitfalls for the current topic.
   - `Laravel comparison`: similarities and differences in concepts, defaults, and common patterns.

4. `Short summary`
   - Brief statement of what is in good shape and what still needs work.

## Django Gotchas To Look For

Tailor these to the topic instead of dumping a generic list.

- Model field defaults, `null` versus `blank`, and UUID primary key setup.
- Migration ordering, data migrations, and accidental schema churn.
- Queryset laziness, N+1 queries, and missing `select_related` or `prefetch_related` where needed.
- Django REST Framework serializer validation versus model validation responsibilities.
- Authentication backend configuration, JWT middleware order, and permission class placement.
- CSRF assumptions leaking into token-based APIs.
- Transaction boundaries, `atomic` usage, and partial writes in service logic.
- Timezone-aware datetimes and inconsistent timestamp serialization.
- Signal overuse when explicit service logic would be clearer.
- Test isolation issues caused by fixtures, transactions, or database reuse.
- Swagger or OpenAPI docs drifting from actual serializers and views.
- CORS, trusted origins, and local dev settings masking deployment behavior.

## Laravel Comparison Prompts

Use these as review lenses, not as rigid rules.

- What is the Django equivalent of the Laravel pattern used here?
- Where does Django expect explicit wiring that Laravel often hides behind conventions?
- Which responsibilities live in serializers, forms, views, services, repositories, or model methods in Django versus Form Requests, Eloquent models, controllers, policies, and service classes in Laravel?
- How do authentication and authorization differ in defaults, extension points, and middleware behavior?
- How does test setup differ from Laravel feature tests and database refresh patterns?
- Which parts of the current Django code are more explicit, and which Laravel conveniences are intentionally absent?

## Decision Rules

### If the implementation is incomplete

- Review the code that exists.
- Distinguish `not implemented yet` from `implemented incorrectly`.
- Do not treat planned-but-missing work as a bug unless the user asked whether the phase is complete.

### If production-grade concerns are relevant but not required

- Mention them under learning notes.
- Do not elevate them above real correctness or contract issues unless they create an immediate defect or security problem.

### If the frontend differs from the backend contract

- Treat the frontend as an integration target.
- Call out the risk clearly, but keep the review centered on whether the backend slice satisfies the plan and contract.

### If there are no material findings

- State that explicitly.
- Still mention residual testing gaps, production follow-up, or framework gotchas worth knowing.

## Quality Bar

A good review from this skill should:

- identify real bugs, regressions, missing requirements, or testing gaps before summarizing
- tie findings back to the phase plan, user journey, repo standards, or API contract
- separate must-fix issues from optional production follow-up
- teach the user something useful about Django-specific pitfalls for the current topic
- explain the closest Laravel comparison where it improves understanding

## Example Prompts

- `/review-plan-phase Phase 3.1 health endpoint`
- `/review-plan-phase Review Phase 3.3 registration endpoint`
- `/review-plan-phase Audit Phase 2.2 model implementation`
- `/review-plan-phase Compare Phase 5.1 password update to how Laravel would usually structure it`