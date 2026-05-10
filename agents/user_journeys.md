# User Journeys

## 1. Registration and Login

### Registration

**Goal**: A new user creates an account.

1. User navigates to `/register`.
   - If already authenticated, they are redirected to `/lobby`.
2. User enters a **username** (3–180 characters) and a **password** (minimum 10 characters, must contain letters, numbers, and symbols), then confirms the password.
3. Client validates that the two password fields match before submitting.
4. On submit, the client sends `POST /api/register` with `{ username, password }`.
   - **Rate limited** — excessive attempts return `429 Too Many Requests`.
5. **Success (201)**: Server returns `{ id, username, createdAt, updatedAt }` and auth tokens. User is authenticated and is redirected to `/lobby`.
6. **Failure**:
   - `400` — validation error (e.g. password too weak). Error message displayed inline.
   - `409` — username already taken. Error message displayed inline.

### Login

**Goal**: An existing user authenticates and receives tokens.

1. User navigates to `/login`.
   - If already authenticated, they are redirected to `/lobby`.
2. User enters **username** and **password**.
3. On submit, the client sends `POST /api/login` with `{ username, password }`.
   - **Rate limited** — excessive attempts return `429 Too Many Requests`.
4. **Success (200)**: Server returns `{ token, refresh_token, user }`.
   - The JWT access token and refresh token are stored (auth context / local storage).
   - User data (`id`, `username`) is stored in auth context.
   - User is redirected to `/lobby`.
5. **Failure**:
   - `401` — invalid credentials. Error message displayed inline.
   - `429` — rate limited. Error message displayed inline.

---

## 2. Token Refresh

**Goal**: Silently obtain a new JWT access token when the current one expires, without requiring the user to log in again.

1. The client detects that the JWT access token is expired or receives a `401` response from a protected endpoint.
2. The client sends `POST /api/token/refresh` with `{ refresh_token }` (the stored refresh token).
   - **Rate limited**.
3. **Success (200)**: Server returns `{ token, refresh_token, user }`.
   - The old refresh token is **revoked** (rotation strategy).
   - The new access token and new refresh token replace the old ones in the auth context / storage.
   - The original request is retried with the new access token.
4. **Failure**:
   - `400` — refresh token missing from request body.
   - `401` — refresh token is invalid, expired, or revoked. The user is logged out and redirected to `/login`.
   - `429` — rate limited.

---

## 3. Logout

**Goal**: User ends their session and all refresh tokens are invalidated.

1. User clicks the **Logout** button on `/lobby` (or any page with a logout control).
2. The client sends `POST /api/logout` with the JWT access token in the `Authorization: Bearer <token>` header.
3. **Success (204)**: Server revokes **all** refresh tokens for the user. No response body.
4. Client clears the access token, refresh token, and user data from auth context / storage.
5. User is redirected to `/login`.
6. **Failure**:
   - `401` — token missing or invalid. Client still clears local state and redirects to `/login`.

---

## 4. Starting a Game

**Goal**: An authenticated user creates a new quiz game.

1. User is on `/lobby`.
2. User fills in the `StartGameForm`:
   - Optional **game name** (string or left blank).
   - Optional **difficulty**: `easy`, `medium`, or `hard` (defaults to `medium`).
3. On submit, the client sends `POST /api/games` with `{ difficulty?, name? }` and the Bearer token.
   - **Rate limited**.
4. **Success (201)**: Server returns:
   ```json
   {
     "id": "<game-uuid>",
     "name": "<string|null>",
     "difficulty": "medium",
     "round": { "id": "<uuid>", "round_number": 1, "category": "General Knowledge" },
     "first_question": { "id": "<uuid>", "question_text": "...", "answers": [...] }
   }
   ```
   - The server creates one **Round** (General Knowledge category) and fetches **5 questions** from the Open Trivia DB.
   - The creating user is automatically recorded as both **host** and **participant** (via `UserGame`).
5. Client redirects to `/game/<game-id>`.
6. **Failure**:
   - `401` — unauthenticated.
   - `429` — rate limited.

---

## 5. Playing the Game, Completing and Viewing Results

### Playing the Game

**Goal**: Participant answers all questions in the game's round.

1. User lands on `/game/:id`. The client sends `GET /api/games/:id` to load the current game state.
   - Response includes game metadata, the round summary, and the `current_question` (first unanswered question).
2. The `GamePage` renders:
   - **GameHeader** — game name, round number, category, difficulty.
   - **QuestionCard** — question text.
   - **AnswerOptions** — four answer choices. Answers have four visual states:
     - Unselected / not submitted
     - Selected (UI only, not yet submitted)
     - Submitted (persisted to server)
     - Reviewed (navigating back to a previously answered question)
3. User selects an answer (UI state only — `selectedAnswerId` updated locally).
4. User clicks **Submit Answer**. The client sends:
   ```
   POST /api/games/:game_id/rounds/:round_id/questions/:question_id/answers/:answer_id/select
   ```
   - **Rate limited**.
   - Server marks the chosen answer as `userSelected = true` and deselects any previously selected answer for that question.
   - **Success (200)**: `{ message, question_id, selected_answer_id }`. UI transitions answer to "submitted" state.
5. **Next Question** button becomes active. User clicks it. Client sends:
   ```
   GET /api/games/:game_id/rounds/:round_id/questions/:question_id/next
   ```
   - **Rate limited**.
   - Response: `{ question: { id, question_text, answers[] } | null }`.
   - `answers[].user_selected` reflects any previously submitted answer.
6. User may also navigate backwards with **Previous Question**:
   ```
   GET /api/games/:game_id/rounds/:round_id/questions/:question_id/previous
   ```
7. User may change a previously submitted answer by selecting a different option and submitting again (the select endpoint deselects the old choice).
8. Steps 3–7 repeat until all 5 questions have been answered.

### Completing the Game

9. On the last question, after submitting an answer, the **View Results** button replaces Next Question.
10. User clicks **View Results**. The client sends `POST /api/games/:id/complete`.
    - **Rate limited**.
    - Server sets `completedAt` on the game and returns `{ message, game_id, total_score, completed_at }`.
    - **Failure**: `400` if game is already completed.
11. Client redirects to `/results/:id`.

### Viewing Results

12. On `/results/:id`, the client sends `GET /api/games/:id/results`.
    - Response:
      ```json
      {
        "game_id": "<uuid>",
        "total_score": 3,
        "total_questions": 5,
        "questions": [
          {
            "question_id": "<uuid>",
            "question_text": "...",
            "correct_answer": "...",
            "selected_answer": "...",
            "is_correct": true
          }
        ]
      }
      ```
13. The `ResultsPage` displays:
    - **Score card** — `X out of Y` correct.
    - **Percentage card** — percentage score.
    - **QuestionBreakdown** — each question with the user's answer, the correct answer, and a correctness indicator.
14. User can optionally **delete the game** (see Journey 7).

---

## 6. Viewing Profile

**Goal**: Authenticated user views and optionally updates their profile.

1. User navigates to `/user` (e.g. via the Profile button on `/lobby`).
2. Client sends `GET /api/user/:user_id` (using the authenticated user's ID from auth context).
   - **Rate limited**.
   - Response: `{ user: { id, username, createdAt, updatedAt }, games: [...] }`.
3. `ProfilePage` displays:
   - **User info** — username, account creation date.
   - **UpdateUsernameForm** — user enters a new username and submits.
     - `PATCH /api/user/:user_id/username` with `{ username }`.
     - **Success (200)**: auth context updated with new username.
     - **Failure**: `400` (invalid), `409` (already taken).
   - **UpdatePasswordForm** — user enters current password and new password, then submits.
     - `PATCH /api/user/:user_id/password` with `{ current_password, new_password }`.
     - **Success (200)**: confirmation message displayed.
     - **Failure**: `400` (incorrect current password or weak new password).
   - **GameHistory** — list of all games the user has participated in or hosted (see Journey 7).

---

## 7. Viewing Game Results

**Goal**: User reviews results for a past game from their profile's game history.

1. From `/user`, the **GameHistory** section lists all games associated with the user.
   - Each entry shows: game name (or unnamed), role (`host` / `participant`), score, start date, completion date, and completion status.
2. User clicks on a completed game entry. Client navigates to `/results/:game_id`.
3. Client sends `GET /api/games/:game_id/results`.
   - **Auth**: required — user must be a participant in the game.
   - **Failure**: `403` if not a participant; `404` if game not found.
4. `ResultsPage` renders the score summary and full `QuestionBreakdown` (same view as post-game completion — see Journey 5, steps 12–13).
5. User may **delete the game**:
   - A **Delete Game** button opens a `ConfirmModal`.
   - On confirmation, client sends `DELETE /api/games/:game_id`.
     - **Auth**: user must be the game **host** (creator).
     - **Success (204)**: game and all associated rounds, questions, and answers are deleted (cascade).
     - **Failure**: `403` (not the host), `404` (not found).
   - After deletion, user is redirected to `/lobby`.
