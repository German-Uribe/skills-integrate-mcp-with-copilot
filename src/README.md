# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Features

- View all available extracurricular activities
- Sign up for activities

## Getting Started

1. Install the dependencies from the repository root:

   ```
   pip install -r requirements.txt
   ```

2. Create a teacher account. The password is stored as a salted hash in the local, git-ignored `src/teachers.json` file:

   ```
   cd src
   python create_teacher.py
   ```

3. Run the application from `src`:

   ```
   uvicorn app:app --reload
   ```

4. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| POST   | `/auth/login`                                                      | Verify teacher credentials using HTTP Basic authentication          |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Teacher-only activity signup                                        |
| DELETE | `/activities/{activity_name}/unregister?email=student@mergington.edu` | Teacher-only activity removal                                    |

Activity listings and participant names remain public. Teachers must sign in to add or remove participants. Teacher credentials are assigned with `create_teacher.py`; the password file is excluded from Git.

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Activities** - Uses activity name as identifier:

   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of student emails who are signed up

2. **Students** - Uses email as identifier:
   - Name
   - Grade level

All data is stored in memory, which means data will be reset when the server restarts.
