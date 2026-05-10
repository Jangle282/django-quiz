# Quiz Implementation Plan

## Phase 1: Project Setup & Infrastructure

### 1.1 Docker Configuration & Backend Skeleton
- Create a dockerised 
  - Django backend for this project
  - A postgres database
  - A node server for the frontend project
- initialise and install dependencies
- Configure database connection

## Phase 2: Database Schema & Models

### 2.1 Database Design
Create migrations and models the following entities:

#### User Entity
```
- table name users
- entity name User
Columns
- id (uuid, primary key)
- username (string, unique)
- password (string, hashed)
- created_at (datetime)
- updated_at (datetime)
```

#### Difficulty Entity
```
- table name quiz_difficulty
- entity name Difficulty
Columns
- id (uuid, primary key)
- name (string, not nullable)
```

#### Game Entity
```
- table name quiz_games
- entity name Game
Columns
- id (uuid, primary key)
- name (string, nullable) - optional game name
- difficulty (Foreign key to quiz_difficulty)
- created_by (uuid, foreign key to user) - user who created the game
- started_at (datetime)
- completed_at (datetime, nullable)
- created_at (datetime)

Note: `total_score` is NOT a stored column — it is calculated dynamically by counting correct answers across all rounds.
```

#### UserGame Entity (Join table for many-to-many User-Game with additional data)
```
- table name user_game
- entity name UserGame
Columns
- id (uuid, primary key)
- user_id (uuid, foreign key to user)
- game_id (uuid, foreign key to quiz_games)
- joined_at (datetime)
- role (string, enum: 'host', 'participant')
```

#### Round Category
```
- table name quiz_category
- entity name Category
Columns
- id (uuid, primary key)
- name (string, not nullable)
```

#### Round Entity
```
- table name quiz_rounds
- entity name Round
Columns
- id (uuid, primary key)
- game_id (foreign key to quiz_games)
- category_id (foreign key to quiz_category)
- round_number (integer)
- created_at (datetime)
```

#### Question Entity
```
- table name quiz_questions
- entity name Question
Columns
- id (uuid, primary key)
- round_id (foreign key to quiz_rounds)
- question_text (text)
```

#### Answer Entity
```
- table name quiz_answers
- entity name Answer
Columns
- id (uuid, primary key)
- question_id (foreign key to quiz_questions)
- answer_text (string)
- user_selected (boolean)
- is_correct (boolean)
```

### 2.2 Entity/Model Implementation
- Create Models and relationships
- Ensure cascade operations are setu p

### 2.3 Seeders and Factories
- Configure Seeders
- Create a basic factory for each model for use in tests and seeders
- Create a set of seeders which can be run during project initialisation via a command. 
- Difficulties seeded
- A user with a game which has 1 round with 5 questions and answers


---

## Phase 3: Create skeleton API 

### 3.1 Health endpoint and basic test set up
- Implement `/api/health` endpoint for readiness/liveness checks
  - The route is unauthenticated
  - Returns a success response
- Set up Swagger
  - Add swagger docs for the endpoint, generate docs and verify against openapi-spec.yml that this endpoint conforms to the contract
- Create a feature test class for the health endpoint
  - Research the best practices for setting up tests in this framework with vsCode using DevContainers
  - Implement a framework for feature and unit tests in the backend. In line with the Backend Architecture & Standards in the adjacent agents files. 
  - Ensure tests can be run inside the docker container directly from VScode UI 'run' buttons.
- Investigate ways to set up the structures for applying throttles to api routes, add a generalist throttle to the health endpoint. 

### 3.2 Create Authentication structures
- The app should use JWT tokens to for authenticated endpoints, with standard authentication and authorization checks rather than CSRF tokens, 
- The app uses `Authorization` header bearer tokens instead of cookie-based auth.

### 3.3 Create Authentication endpoints
- Implement User registration endpoint (`POST /api/register`)
  - The route is unauthenticated
  - Validate username uniqueness
  - Validate password strength (minimum 10 characters, mix of letters, numbers, symbols)
  - username and password validation must be exracted to place where it can be reused
  - Hash password
  - Create user
  - Return user data (without password)
  - set an appropriate throttle
  - generate swagger docs and verify against openapi-spec.yml that this endpoint conforms to the contract
- Create dedicated feature test class covering endpoint testing
- Create dedicated Service class tests coving business logic - Verify that the front end application can POST to this endpoint without CORS errors

- Implement login endpoint (`POST /api/login`)
  - The route is unauthenticated
  - Validate credentials
  - Generate JWT token and refresh token
  - Return tokens
  - The route is unauthenticated
  - Create dedicated feature test class covering endpoint testing
  - Create dedicated Service class tests coving business logic - set an appropriate throttle
  - generate swagger docs and verify against openapi-spec.yml that this endpoint conforms to the contract

- Implement logout endpoint (`POST /api/logout`)
  - request could be authenticated or unauthenticated
  - Invalidate token (if using token blacklist)
  - Create dedicated feature test class covering endpoint testing
  - Create dedicated Service class tests coving business logic   - set an appropriate throttle
  - generate swagger docs and verify against openapi-spec.yml that this endpoint conforms to the contract

- Implement token refresh endpoint (`POST /api/token/refresh`)
  - request could be authenticated or unauthenticated
  - uses a refresh token to regenerate a valid JWT token, normal JWT authentication flow. 
  - revokes all refresh tokens
  - Create dedicated feature test class covering endpoint testing
  - Create dedicated Service class tests coving business logic   - set an appropriate throttle
  - generate swagger docs and verify against openapi-spec.yml that this endpoint conforms to the contract

### 3.4 First authenticated route
- Create get user endpoint (`GET /api/user/{user_id}`)
  - request is authenticated
  - Return user data
  - Return games participated in (via UserGame)
  - generate swagger docs and verify against openapi-spec.yml that this endpoint conforms to the contract
- Set up access control structure foundations. Add checks that this endpoint may only be accessed by the user_id
- Create dedicated feature test class 

## Phase 5: Backend - User management endpoints

### 5.1 Authorization & Security 
- For each endpoint
  - Are authenticated, authenticated user and user_id must match
  - Create dedicated feature test class covering endpoint testing
  - Create dedicated Service class tests coving business logic 
  - set an approproate throttle
  - generate swagger docs and verify against openapi-spec.yml that this endpoint conforms to the contract
- Create get user endpoint (`GET /api/user/{user_id}`)
  - Return user data
  - Return games participated in (via UserGame)
- Update username endpoint (`PATCH /api/user/{user_id}/username`)
  - Validate uniqueness
  - Update user
- Update password endpoint (`PATCH /api/user/{user_id}/password`)
  - Validate old password
  - Validate new password strength
  - Hash new password
  - Update user
- Delete game endpoint (`DELETE /api/games/{id}`)
  - Check user is host of the game
  - Soft delete or hard delete game

---

## Phase 6: Backend - Question external API Service Layer

### 6.1 Question Provider Interface
Create abstraction layer for question sources:

- Create `QuestionProviderInterface` with methods:
  - `createQuestionsAndAnswers(rounds, difficulty, amount): void`

### 6.2 Open Trivia DB Implementation
- Create `OpenTriviaDBProvider` implementing `QuestionProviderInterface`
- Implement HTTP client for API calls
- Implement API authentication and refreshing mechanisms if necessary
- Add response parsing and validation
- Handle API errors and rate limiting
- Decode HTML entities in questions/answers
- CreateQuestionsAndAnswers() should:
  - Map the category of the Round to the categories available from the api 
  - Map the difficulty of the game to the difficulties available from the api
  - Fetch 5 questions per round by default 
  - Map API responses to Question and Answer DTOs ready for storing in the database.
- Create unit tests for OpenTriviaDBProvider which mock the responses from the api.

### 6.3 Question Service
- Create `QuestionService` that uses `QuestionProviderInterface`
- Implement method to fetch and store questions and answers for a round
- Shuffle answer options (mix correct with incorrect)
- Create unit tests covering the QuestionService

---

## Phase 7: Backend - Game Logic
- For each endpoint
  - Are authenticated, users may only access games they are a participant of. 
  - Create dedicated feature test classes for endpoint testsing
  - Create dedicated Service class tests coving business logic 
  - set an approproate throttle
  - generate swagger docs and verify against openapi-spec.yml that this endpoint conforms to the contract

- GameController endpoints. Using a GameService for business Logic. 
  - Start new game (`POST /api/games`)
    - Create Game entity
    - Create UserGame entity for creator (role: host)
    - Create Round entity (1 round, general knowledge)
    - Fetch 5 questions from provider
    - Store questions and answers in database
    - Return game ID and first question
    - The returned question cannot contain the correct answer
  - Get current game state (`GET /api/games/{id}`)
    - Return game progress
    - Return current question
    - Check user is participant
  - Complete game endpoint (`POST /api/games/{id}/complete`)
    - Mark game as completed
  - Get game results (`GET /api/games/{id}/results`)
    - Return total team score
    - Return question breakdown (question, team answer, correct answer, is_correct)
    - Check user is participant
- UserGameController Using a UserGame Service for logic
  - Join game (`POST /api/games/{id}/join`) - for future multi-user
    - Add user as participant
- QuestionController using QuestionService for logic
  - Get next question (`GET /api/games/{id}/rounds/{id}/questions/{id}/next`)
    - Questions are ordered by id
    - Return next question of the round with which answer was previously selected (if any given)
    - Return null if all answered
    - Do not return which answer is correct in the response
    - Check the User has joined the game
  - Get previous question (`GET /api/games/{id}/rounds/{id}/questions/{id}/previous`)
    - Questions are ordered by id within a round
    - Return previous question in the round with which answer was previously selected (if any given)
    - Return null if there is no previous question
    - Do not return which answer is correct in the response
    - Check the User has joined the game
- AnswerController using an AnswerService for logic
  - Submit answer endpoint (`POST /api/games/{id}/rounds/{id}/questions/{id}/answers/{id}/select`)
    - Validate question belongs to game
    - Validate the answer relates to the question
    - Validate the user is a participant of the game
    - Validate the Game is not already completed
    - update user_selection in Answer entity.
    - removed user_selection from other answers to the same question