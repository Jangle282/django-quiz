## Project Overview
The goal of this project is for the user to learn about the Django backend framework, they are an experienced developer in PHP laravel and they want to learn about Python and Django through making an api for a simple 'pub quiz' game application. 

The steps to build the application are in ./implementation_plan.md. Each step will be a pull request. The user wants to know the plan for each phase to learn how that phase is implemented in Django.

User journeys are in ./user_journeys.md


## Project Tech stack
- **Backend**: Python Django with postgreSQL database, pytest. Needs to conform to ../api-contract.yaml
- **Frontend**: SPA React already created - can be found in ../frontend, built to ../api-contract.yaml
- **Infrastructure**: Docker & Docker Compose
- **API**: Open Trivia Database (https://opentdb.com/) but should be extensible to other API providers

## Backend Architecture & Standards
- Endpoints should be RESTFUL.
- Decide for standard practises in the Django framework.
- Unauthenticated endpoints should be covered by a throttle by IP. Authenticated routes by a throttle by user id. 
- Throttling should be handled by a global handler and not duplicated.
- Controllers should be slim, utilising service classes for logic. They should focus on Requests and Responses and orchestrating services.
- Services should avoid requiring other services, unless necessary. To avoid circular references. 
- Use Repository classes for database interactions. 
- Endpoints should be covered with feature tests concerned with authorisation, authentication, request validation and responses. 
- Service classes should be covered with unit tests which also test database layer persistence. There is no need to mock the database.
- Tests should use the same database as the application but utilise transactions, rolling back changes made during the test.
- The backend is responsible for returning error messages to be shown in the Front end.
- Create swagger documentation for the API.
- Responses and Requests should have a class or definition which can be documented by swagger outside the controller to avoid cluttering the controller with swagger documentation. 


## Frontend Architecture & Standards
- The frontend is a Single Page Application (SPA)
- Uses the backend as an API-only service for authentication and quiz data
- Prefers storing JWT tokens outside of cookies and sends them in the `Authorization` header
- Protects the app against XSS by keeping tokens in safe client storage, avoids insecure script injection, and uses secure coding patterns


## Patterns
- Review instructions against this file for conflicts. Request resolution before starting
- Always write tests