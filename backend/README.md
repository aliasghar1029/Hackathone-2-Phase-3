# Todo Application Backend

A FastAPI backend for a Todo application with authentication and task management features.

## Features

- User authentication (signup/signin)
- JWT-based authentication
- Task CRUD operations
- Task filtering by status
- Secure password hashing
- PostgreSQL database with Neon

## Prerequisites

- Python 3.8+
- PostgreSQL database (Neon serverless used in this project)

## Setup Instructions

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Copy the `.env.example` file to `.env` and update the values:

```bash
cp .env.example .env
```

Edit `.env` and set your database URL and JWT secret.

### 5. Run the application

```bash
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

API documentation will be available at `http://localhost:8000/docs`.

## API Endpoints

### Authentication

- `POST /api/auth/signup` - Create a new user account
- `POST /api/auth/signin` - Login to an existing account

### Tasks

All task endpoints require a valid JWT token in the Authorization header: `Authorization: Bearer {token}`

- `GET /api/{user_id}/tasks?status={all|pending|completed}` - Get user's tasks
- `POST /api/{user_id}/tasks` - Create a new task
- `PUT /api/{user_id}/tasks/{task_id}` - Update a task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{task_id}/complete` - Toggle task completion

## Environment Variables

- `DATABASE_URL` - PostgreSQL database connection string
- `JWT_SECRET` - Secret key for JWT token signing
- `ENVIRONMENT` - Environment (development/production)

## Project Structure

```
.
├── main.py                 # Main FastAPI application
├── models.py              # Database models using SQLModel
├── db.py                  # Database connection and session
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── routes/                # API route definitions
│   ├── auth.py            # Authentication routes
│   └── tasks.py           # Task management routes
├── services/              # Business logic
│   ├── auth.py            # Authentication services
│   └── tasks.py           # Task services
└── middleware/            # Custom middleware
    └── jwt.py             # JWT authentication middleware
```

## Frontend Integration

This backend is designed to work seamlessly with a Next.js Todo frontend. The API endpoints match the exact specifications required by the frontend.

## Development

For development, use the `--reload` flag with uvicorn to enable auto-reloading when files change:

```bash
uvicorn main:app --reload --port 8000
```

## Deployment

To deploy this application:

1. Update the CORS origins in `main.py` to include your production domain
2. Set the appropriate environment variables in your deployment environment
3. Run migrations if needed (currently handled automatically on startup)
4. Deploy using your preferred platform (Heroku, Vercel, AWS, etc.)

## Security

- Passwords are securely hashed using bcrypt
- JWT tokens are signed with HS256 algorithm
- Input validation is performed on all endpoints
- SQL injection is prevented through ORM usage
- User authorization is enforced on all task endpoints