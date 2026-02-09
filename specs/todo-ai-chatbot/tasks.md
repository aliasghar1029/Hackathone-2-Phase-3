# TODO AI CHATBOT - IMPLEMENTATION TASKS

## Task Format
Each task follows this structure:
- Task ID: Unique identifier
- Task Name: Brief description
- Preconditions: What must be done before
- Implementation Steps: Detailed subtasks
- Files to Modify/Create: Specific file paths
- Spec References: Links to specify and plan sections
- Validation: How to verify completion
- Estimated Time: Time to complete

---

## SETUP TASKS

### T-001: Project Initialization
**Preconditions:** None
**Implementation Steps:**
1. Create project directory: `mkdir todo-ai-chatbot && cd todo-ai-chatbot`
2. Initialize monorepo structure
3. Create `/frontend` and `/backend` folders
4. Create `/specs` folder
5. Create root `README.md`, `CLAUDE.md`, `AGENTS.md`

**Files to Create:**
```
todo-ai-chatbot/
├── frontend/
├── backend/
├── specs/
├── README.md
├── CLAUDE.md
└── AGENTS.md
```

**Spec References:**
- speckit.plan §6 (File Structure)

**Validation:**
- Directory structure matches plan
- All folders exist

**Estimated Time:** 5 minutes

---

### T-002: Backend Setup
**Preconditions:** T-001
**Implementation Steps:**
1. `cd backend`
2. `uv init`
3. Create `pyproject.toml` with dependencies:
   - fastapi[standard]
   - sqlmodel
   - psycopg2-binary
   - python-jose[cryptography]
   - passlib[bcrypt]
   - python-multipart
   - openai
   - mcp
4. Create `.env` file with placeholders
5. Create `main.py` with basic FastAPI app
6. Create empty folders: `routes/`, `services/`, `mcp/`, `middleware/`

**Files to Create:**
```
backend/
├── pyproject.toml
├── .env
├── main.py
├── models.py
├── db.py
├── routes/
├── services/
├── mcp/
└── middleware/
```

**Spec References:**
- speckit.plan §2.2 (Backend Components)
- speckit.constitution §2 (Technology Stack)

**Validation:**
- `uv run uvicorn main:app --reload` starts server
- http://localhost:8000/docs shows FastAPI docs

**Estimated Time:** 15 minutes

---

### T-003: Frontend Setup
**Preconditions:** T-001
**Implementation Steps:**
1. `cd frontend`
2. `npx create-next-app@latest . --typescript --tailwind --app --no-src-dir`
3. Install dependencies:
   - `npm install @auth/core better-auth`
   - `npm install openai`
   - `npm install framer-motion`
   - `npm install @headlessui/react`
4. Create `.env.local` with placeholders
5. Setup Tailwind config for glassmorphic design
6. Create folder structure: `components/auth`, `components/tasks`, `components/chat`, `components/ui`

**Files to Create:**
```
frontend/
├── app/
├── components/
│   ├── auth/
│   ├── tasks/
│   ├── chat/
│   └── ui/
├── lib/
├── .env.local
└── tailwind.config.ts
```

**Spec References:**
- speckit.plan §2.1 (Frontend Components)
- speckit.constitution §5 (UI/UX Principles)

**Validation:**
- `npm run dev` starts server
- http://localhost:3000 shows Next.js page
- Tailwind classes working

**Estimated Time:** 20 minutes

---

## DATABASE TASKS

### T-004: Database Models
**Preconditions:** T-002
**Implementation Steps:**
1. Create `backend/models.py`
2. Define SQLModel classes:
   - User (id, email, name, password_hash, created_at, updated_at)
   - Task (id, user_id, title, description, completed, created_at, updated_at)
   - Conversation (id, user_id, created_at, updated_at)
   - Message (id, conversation_id, user_id, role, content, created_at)
3. Add proper type hints
4. Add Field constraints (max_length, indexes, foreign keys)
5. Add datetime defaults

**Files to Create/Modify:**
- `backend/models.py` (new)

**Code Template:**
```python
# [Task]: T-004
# [From]: speckit.specify §6, speckit.plan §2.3

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    id: str = Field(primary_key=True)
    email: str = Field(unique=True, index=True)
    name: str
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id", index=True)
    user_id: str = Field(foreign_key="user.id")
    role: str  # 'user' or 'assistant'
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

**Spec References:**
- speckit.specify §6 (Data Models)
- speckit.plan §2.3 (Database Layer)

**Validation:**
- No syntax errors
- Import models in main.py without errors
- Type hints correct

**Estimated Time:** 20 minutes

---

### T-005: Database Connection
**Preconditions:** T-004
**Implementation Steps:**
1. Create `backend/db.py`
2. Load `DATABASE_URL` from environment
3. Create SQLModel engine
4. Create `init_db()` function
5. Create `get_session()` dependency
6. Add connection pooling config

**Files to Create/Modify:**
- `backend/db.py` (new)
- `backend/.env` (update)

**Code Template:**
```python
# [Task]: T-005
# [From]: speckit.plan §2.3

from sqlmodel import create_engine, Session, SQLModel
import os

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set")

engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_size=5,
    max_overflow=10
)

def init_db():
    """Create all tables"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependency for FastAPI routes"""
    with Session(engine) as session:
        yield session
```

**Environment Variable:**
```
DATABASE_URL=postgresql://user:password@host/database?sslmode=require
```

**Spec References:**
- speckit.plan §2.3 (Database Connection)

**Validation:**
- Engine connects successfully
- `init_db()` creates tables in Neon
- Verify tables exist in Neon dashboard

**Estimated Time:** 15 minutes

---

## AUTHENTICATION TASKS

### T-006: Auth Service
**Preconditions:** T-004, T-005
**Implementation Steps:**
1. Create `backend/services/auth.py`
2. Implement password hashing with bcrypt
3. Implement JWT generation and verification
4. Implement signup logic (create user)
5. Implement signin logic (verify password, return JWT)

**Files to Create/Modify:**
- `backend/services/auth.py` (new)
- `backend/.env` (add JWT_SECRET)

**Code Template:**
```python
# [Task]: T-006
# [From]: speckit.plan §2.2

from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from sqlmodel import Session, select
from backend.models import User
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("JWT_SECRET", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict) -> str:
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def signup(session: Session, email: str, name: str, password: str) -> dict:
    # Check if user exists
    existing = session.exec(select(User).where(User.email == email)).first()
    if existing:
        raise ValueError("Email already registered")

    # Create user
    user = User(
        id=...,  # Generate UUID
        email=email,
        name=name,
        password_hash=hash_password(password)
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    # Generate token
    token = create_access_token({"user_id": user.id, "email": user.email})
    return {"user": user, "token": token}

def signin(session: Session, email: str, password: str) -> dict:
    user = session.exec(select(User).where(User.email == email)).first()
    if not user or not verify_password(password, user.password_hash):
        raise ValueError("Invalid credentials")

    token = create_access_token({"user_id": user.id, "email": user.email})
    return {"user": user, "token": token}
```

**Spec References:**
- speckit.plan §2.2 (Authentication Service)
- speckit.specify §3 (FR-1)

**Validation:**
- Password hashing works
- JWT generation works
- Signup creates user in database
- Signin returns valid JWT

**Estimated Time:** 30 minutes

---

### T-007: Auth Routes
**Preconditions:** T-006
**Implementation Steps:**
1. Create `backend/routes/auth.py`
2. Define Pydantic request/response models
3. Create POST /api/auth/signup endpoint
4. Create POST /api/auth/signin endpoint
5. Add error handling
6. Register routes in main.py

**Files to Create/Modify:**
- `backend/routes/auth.py` (new)
- `backend/main.py` (update)

**Code Template:**
```python
# [Task]: T-007
# [From]: speckit.plan §3

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlmodel import Session
from backend.db import get_session
from backend.services import auth

router = APIRouter(prefix="/api/auth", tags=["auth"])

class SignupRequest(BaseModel):
    email: EmailStr
    name: str
    password: str

class SigninRequest(BaseModel):
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    user: dict
    token: str

@router.post("/signup", response_model=AuthResponse)
def signup(data: SignupRequest, session: Session = Depends(get_session)):
    try:
        result = auth.signup(session, data.email, data.name, data.password)
        return result
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.post("/signin", response_model=AuthResponse)
def signin(data: SigninRequest, session: Session = Depends(get_session)):
    try:
        result = auth.signin(session, data.email, data.password)
        return result
    except ValueError as e:
        raise HTTPException(401, str(e))
```

**Update main.py:**
```python
from backend.routes import auth

app.include_router(auth.router)
```

**Spec References:**
- speckit.specify §7 (API Endpoints)
- speckit.plan §3 (API Design)

**Validation:**
- POST /api/auth/signup creates user
- POST /api/auth/signin returns JWT
- Invalid credentials return 401
- Duplicate email returns 400

**Estimated Time:** 25 minutes

---

### T-008: JWT Middleware
**Preconditions:** T-006
**Implementation Steps:**
1. Create `backend/middleware/jwt.py`
2. Implement JWT extraction from Authorization header
3. Implement token verification
4. Implement user_id extraction
5. Create FastAPI dependency

**Files to Create/Modify:**
- `backend/middleware/jwt.py` (new)

**Code Template:**
```python
# [Task]: T-008
# [From]: speckit.plan §8

from fastapi import Header, HTTPException, Depends
from backend.services.auth import verify_token

async def get_current_user(authorization: str = Header(None)) -> str:
    """Extract and verify JWT, return user_id"""
    if not authorization:
        raise HTTPException(401, "Authorization header missing")

    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Invalid authorization header")

    token = authorization.replace("Bearer ", "")
    payload = verify_token(token)

    if not payload:
        raise HTTPException(401, "Invalid or expired token")

    return payload["user_id"]

async def verify_user_id(user_id: str, current_user: str = Depends(get_current_user)):
    """Verify that URL user_id matches JWT user_id"""
    if user_id != current_user:
        raise HTTPException(403, "Access forbidden")
    return user_id
```

**Spec References:**
- speckit.plan §8 (Security Architecture)
- speckit.specify §4 (NFR-2)

**Validation:**
- Missing token returns 401
- Invalid token returns 401
- Mismatched user_id returns 403
- Valid token returns user_id

**Estimated Time:** 20 minutes

---

## TASK MANAGEMENT TASKS

### T-009: Task Service
**Preconditions:** T-004, T-005
**Implementation Steps:**
1. Create `backend/services/tasks.py`
2. Implement create_task()
3. Implement get_tasks() with status filter
4. Implement get_task()
5. Implement update_task()
6. Implement delete_task()
7. Implement toggle_complete()
8. Add user_id validation to all functions

**Files to Create/Modify:**
- `backend/services/tasks.py` (new)

**Code Template:**
```python
# [Task]: T-009
# [From]: speckit.plan §2.2

from sqlmodel import Session, select
from backend.models import Task
from datetime import datetime
from typing import List, Optional

def create_task(session: Session, user_id: str, title: str, description: str = "") -> Task:
    task = Task(
        user_id=user_id,
        title=title,
        description=description
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def get_tasks(session: Session, user_id: str, status: str = "all") -> List[Task]:
    query = select(Task).where(Task.user_id == user_id)

    if status == "pending":
        query = query.where(Task.completed == False)
    elif status == "completed":
        query = query.where(Task.completed == True)

    tasks = session.exec(query).all()
    return tasks

def get_task(session: Session, user_id: str, task_id: int) -> Optional[Task]:
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        return None
    return task

def update_task(session: Session, user_id: str, task_id: int, title: str = None, description: str = None) -> Optional[Task]:
    task = get_task(session, user_id, task_id)
    if not task:
        return None

    if title:
        task.title = title
    if description is not None:
        task.description = description

    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def delete_task(session: Session, user_id: str, task_id: int) -> bool:
    task = get_task(session, user_id, task_id)
    if not task:
        return False

    session.delete(task)
    session.commit()
    return True

def toggle_complete(session: Session, user_id: str, task_id: int) -> Optional[Task]:
    task = get_task(session, user_id, task_id)
    if not task:
        return None

    task.completed = not task.completed
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

**Spec References:**
- speckit.specify §3 (FR-2)
- speckit.plan §2.2 (Task Service)

**Validation:**
- create_task inserts into database
- get_tasks filters by user_id and status
- update_task modifies only user's tasks
- delete_task removes only user's tasks
- toggle_complete changes status

**Estimated Time:** 35 minutes

---

### T-010: Task Routes
**Preconditions:** T-009, T-008
**Implementation Steps:**
1. Create `backend/routes/tasks.py`
2. Define Pydantic models for requests/responses
3. Create GET /api/{user_id}/tasks (with status query param)
4. Create POST /api/{user_id}/tasks
5. Create GET /api/{user_id}/tasks/{id}
6. Create PUT /api/{user_id}/tasks/{id}
7. Create DELETE /api/{user_id}/tasks/{id}
8. Create PATCH /api/{user_id}/tasks/{id}/complete
9. Apply JWT middleware to all routes
10. Register router in main.py

**Files to Create/Modify:**
- `backend/routes/tasks.py` (new)
- `backend/main.py` (update)

**Code Template:**
```python
# [Task]: T-010
# [From]: speckit.plan §3

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlmodel import Session
from backend.db import get_session
from backend.services import tasks
from backend.middleware.jwt import verify_user_id
from typing import List, Optional

router = APIRouter(prefix="/api/{user_id}/tasks", tags=["tasks"])

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = ""

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class TaskResponse(BaseModel):
    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: str
    updated_at: str

@router.get("", response_model=List[TaskResponse])
def list_tasks(
    user_id: str,
    status: str = Query("all", regex="^(all|pending|completed)$"),
    session: Session = Depends(get_session),
    _: str = Depends(verify_user_id)
):
    return tasks.get_tasks(session, user_id, status)

@router.post("", response_model=TaskResponse, status_code=201)
def create_task(
    user_id: str,
    data: TaskCreate,
    session: Session = Depends(get_session),
    _: str = Depends(verify_user_id)
):
    return tasks.create_task(session, user_id, data.title, data.description)

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    user_id: str,
    task_id: int,
    session: Session = Depends(get_session),
    _: str = Depends(verify_user_id)
):
    task = tasks.get_task(session, user_id, task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    return task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    user_id: str,
    task_id: int,
    data: TaskUpdate,
    session: Session = Depends(get_session),
    _: str = Depends(verify_user_id)
):
    task = tasks.update_task(session, user_id, task_id, data.title, data.description)
    if not task:
        raise HTTPException(404, "Task not found")
    return task

@router.delete("/{task_id}")
def delete_task(
    user_id: str,
    task_id: int,
    session: Session = Depends(get_session),
    _: str = Depends(verify_user_id)
):
    success = tasks.delete_task(session, user_id, task_id)
    if not success:
        raise HTTPException(404, "Task not found")
    return {"success": True}

@router.patch("/{task_id}/complete", response_model=TaskResponse)
def toggle_complete(
    user_id: str,
    task_id: int,
    session: Session = Depends(get_session),
    _: str = Depends(verify_user_id)
):
    task = tasks.toggle_complete(session, user_id, task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    return task
```

**Update main.py:**
```python
from backend.routes import tasks

app.include_router(tasks.router)
```

**Spec References:**
- speckit.specify §7 (API Endpoints)
- speckit.plan §3 (REST Endpoints)

**Validation:**
- All endpoints require JWT
- Endpoints return 403 for wrong user_id
- GET /tasks filters by status
- POST creates task
- PUT/DELETE/PATCH work correctly

**Estimated Time:** 40 minutes

---

## MCP SERVER TASKS

### T-011: MCP Server Setup
**Preconditions:** T-009
**Implementation Steps:**
1. Create `backend/mcp/server.py`
2. Install MCP Python SDK: `uv add mcp`
3. Initialize MCP server
4. Define tool schemas (5 tools)
5. Register tools with server

**Files to Create/Modify:**
- `backend/mcp/server.py` (new)
- `backend/pyproject.toml` (update dependencies)

**Code Template:**
```python
# [Task]: T-011
# [From]: speckit.plan §2.2

from mcp import MCPServer, Tool
from pydantic import BaseModel
from sqlmodel import Session
from backend.services import tasks as task_service
from backend.db import get_session

# Initialize MCP server
mcp_server = MCPServer(name="todo-mcp-server")

# Tool schemas
class AddTaskInput(BaseModel):
    user_id: str
    title: str
    description: str = ""

class ListTasksInput(BaseModel):
    user_id: str
    status: str = "all"

class TaskActionInput(BaseModel):
    user_id: str
    task_id: int

class UpdateTaskInput(BaseModel):
    user_id: str
    task_id: int
    title: str = None
    description: str = None

# Tool implementations (next task)
```

**Spec References:**
- speckit.specify §8 (MCP Tools Specification)
- speckit.plan §2.2 (MCP Server)

**Validation:**
- MCP server initializes without errors
- Tool schemas defined

**Estimated Time:** 20 minutes

---

### T-012: MCP Tools Implementation
**Preconditions:** T-011
**Implementation Steps:**
1. Implement add_task tool
2. Implement list_tasks tool
3. Implement complete_task tool
4. Implement delete_task tool
5. Implement update_task tool
6. Add error handling to each tool
7. Test each tool independently

**Files to Modify:**
- `backend/mcp/server.py`

**Code Template:**
```python
# [Task]: T-012
# [From]: speckit.specify §8

@mcp_server.tool()
def add_task(input: AddTaskInput) -> dict:
    """Create a new task"""
    try:
        with Session(engine) as session:
            task = task_service.create_task(
                session,
                input.user_id,
                input.title,
                input.description
            )
            return {
                "task_id": task.id,
                "status": "created",
                "title": task.title
            }
    except Exception as e:
        return {"error": str(e)}

@mcp_server.tool()
def list_tasks(input: ListTasksInput) -> dict:
    """List tasks with optional status filter"""
    try:
        with Session(engine) as session:
            tasks = task_service.get_tasks(session, input.user_id, input.status)
            return {
                "tasks": [
                    {
                        "id": t.id,
                        "title": t.title,
                        "completed": t.completed,
                        "created_at": str(t.created_at)
                    }
                    for t in tasks
                ]
            }
    except Exception as e:
        return {"error": str(e)}

@mcp_server.tool()
def complete_task(input: TaskActionInput) -> dict:
    """Mark a task as complete"""
    try:
        with Session(engine) as session:
            task = task_service.toggle_complete(session, input.user_id, input.task_id)
            if not task:
                return {"error": "Task not found"}
            return {
                "task_id": task.id,
                "status": "completed" if task.completed else "incomplete",
                "title": task.title
            }
    except Exception as e:
        return {"error": str(e)}

@mcp_server.tool()
def delete_task(input: TaskActionInput) -> dict:
    """Delete a task"""
    try:
        with Session(engine) as session:
            # Get task title before deleting
            task = task_service.get_task(session, input.user_id, input.task_id)
            if not task:
                return {"error": "Task not found"}

            title = task.title
            success = task_service.delete_task(session, input.user_id, input.task_id)

            if success:
                return {
                    "task_id": input.task_id,
                    "status": "deleted",
                    "title": title
                }
            return {"error": "Delete failed"}
    except Exception as e:
        return {"error": str(e)}

@mcp_server.tool()
def update_task(input: UpdateTaskInput) -> dict:
    """Update task title or description"""
    try:
        with Session(engine) as session:
            task = task_service.update_task(
                session,
                input.user_id,
                input.task_id,
                input.title,
                input.description
            )
            if not task:
                return {"error": "Task not found"}
            return {
                "task_id": task.id,
                "status": "updated",
                "title": task.title
            }
    except Exception as e:
        return {"error": str(e)}

def get_mcp_tools():
    """Return MCP tools for OpenAI Agent"""
    return mcp_server.get_tools()
```

**Spec References:**
- speckit.specify §8 (MCP Tools)
- speckit.plan §2.2 (MCP Server)

**Validation:**
- Each tool can be called independently
- Tools return correct format
- Error handling works
- User_id validation works

**Estimated Time:** 45 minutes

---

## CHAT/AI TASKS

### T-013: Conversation Service
**Preconditions:** T-004, T-005
**Implementation Steps:**
1. Create `backend/services/chat.py`
2. Implement create_conversation()
3. Implement get_or_create_conversation()
4. Implement load_history()
5. Implement save_message()

**Files to Create/Modify:**
- `backend/services/chat.py` (new)

**Code Template:**
```python
# [Task]: T-013
# [From]: speckit.plan §2.2

from sqlmodel import Session, select
from backend.models import Conversation, Message
from typing import List, Optional

def get_or_create_conversation(session: Session, user_id: str, conversation_id: Optional[int] = None) -> Conversation:
    """Get existing conversation or create new one"""
    if conversation_id:
        conv = session.get(Conversation, conversation_id)
        if conv and conv.user_id == user_id:
            return conv

    # Create new conversation
    conv = Conversation(user_id=user_id)
    session.add(conv)
    session.commit()
    session.refresh(conv)
    return conv

def load_history(session: Session, conversation_id: int) -> List[dict]:
    """Load all messages from a conversation"""
    messages = session.exec(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
    ).all()

    return [
        {"role": msg.role, "content": msg.content}
        for msg in messages
    ]

def save_message(session: Session, conversation_id: int, user_id: str, role: str, content: str) -> Message:
    """Save a message to the conversation"""
    message = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role=role,
        content=content
    )
    session.add(message)
    session.commit()
    session.refresh(message)
    return message
```

**Spec References:**
- speckit.specify §3 (FR-5)
- speckit.plan §2.2 (Chat Service)

**Validation:**
- Conversations created successfully
- History loaded correctly
- Messages saved with correct timestamps

**Estimated Time:** 25 minutes

---

### T-014: OpenAI Agent Integration
**Preconditions:** T-012, T-013
**Implementation Steps:**
1. Update `backend/services/chat.py`
2. Install OpenAI Agents SDK: `uv add openai`
3. Create Agent with system instructions
4. Integrate MCP tools with Agent
5. Implement run_agent() function
6. Handle tool calls and responses

**Files to Modify:**
- `backend/services/chat.py`
- `backend/.env` (add OPENAI_API_KEY)

**Code Template:**
```python
# [Task]: T-014
# [From]: speckit.plan §5

import os
import json
from openai import OpenAI
from backend.mcp.server import get_mcp_tools

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

AGENT_INSTRUCTIONS = """
You are a helpful todo assistant. You help users manage their tasks through natural language.

When the user wants to:
- Add a task → Use add_task tool
- See tasks → Use list_tasks tool
- Complete a task → Use complete_task tool
- Delete a task → Use delete_task tool (ask for confirmation if unclear)
- Update a task → Use update_task tool

Always confirm actions with a friendly response.
Be conversational and helpful.
"""

def run_agent(user_id: str, messages: List[dict]) -> dict:
    """Run OpenAI Agent with MCP tools"""
    try:
        # Get MCP tools
        tools = get_mcp_tools()

        # Add system message
        system_message = {"role": "system", "content": AGENT_INSTRUCTIONS}
        full_messages = [system_message] + messages

        # Call OpenAI with tools
        response = client.chat.completions.create(
            model="gpt-4",
            messages=full_messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        # Handle tool calls
        if message.tool_calls:
            tool_results = []
            for tool_call in message.tool_calls:
                # Execute MCP tool
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                # Add user_id to tool args
                tool_args["user_id"] = user_id

                # Call the tool
                result = execute_mcp_tool(tool_name, tool_args)
                tool_results.append({
                    "tool": tool_name,
                    "args": tool_args,
                    "result": result
                })

            # Get final response after tool execution
            # (simplified - in production, you'd add tool results to messages and call again)
            return {
                "response": message.content or "Task completed",
                "tool_calls": tool_results
            }

        return {
            "response": message.content,
            "tool_calls": []
        }

    except Exception as e:
        return {
            "response": f"Sorry, I encountered an error: {str(e)}",
            "tool_calls": []
        }

def execute_mcp_tool(tool_name: str, args: dict) -> dict:
    """Execute an MCP tool by name"""
    from backend.mcp.server import add_task, list_tasks, complete_task, delete_task, update_task

    tool_map = {
        "add_task": add_task,
        "list_tasks": list_tasks,
        "complete_task": complete_task,
        "delete_task": delete_task,
        "update_task": update_task
    }

    tool_func = tool_map.get(tool_name)
    if not tool_func:
        return {"error": f"Unknown tool: {tool_name}"}

    return tool_func(args)
```

**Spec References:**
- speckit.specify §3 (FR-3)
- speckit.plan §5 (OpenAI Integration)

**Validation:**
- Agent responds to simple messages
- Agent calls MCP tools correctly
- Tool results returned
- Errors handled gracefully

**Estimated Time:** 50 minutes

---

### T-015: Chat Endpoint
**Preconditions:** T-014
**Implementation Steps:**
1. Create `backend/routes/chat.py`
2. Define request/response models
3. Create POST /api/{user_id}/chat endpoint
4. Implement stateless flow:
   - Load history
   - Save user message
   - Run agent
   - Save assistant response
   - Return response
5. Apply JWT middleware
6. Register router in main.py

**Files to Create/Modify:**
- `backend/routes/chat.py` (new)
- `backend/main.py` (update)

**Code Template:**
```python
# [Task]: T-015
# [From]: speckit.plan §3

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session
from backend.db import get_session
from backend.services import chat
from backend.middleware.jwt import verify_user_id
from typing import Optional, List

router = APIRouter(prefix="/api/{user_id}/chat", tags=["chat"])

class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    message: str

class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: List[dict]

@router.post("", response_model=ChatResponse)
def send_message(
    user_id: str,
    data: ChatRequest,
    session: Session = Depends(get_session),
    _: str = Depends(verify_user_id)
):
    try:
        # Get or create conversation
        conversation = chat.get_or_create_conversation(session, user_id, data.conversation_id)

        # Load history
        history = chat.load_history(session, conversation.id)

        # Save user message
        chat.save_message(session, conversation.id, user_id, "user", data.message)

        # Build message array
        messages = history + [{"role": "user", "content": data.message}]

        # Run agent
        result = chat.run_agent(user_id, messages)

        # Save assistant response
        chat.save_message(session, conversation.id, user_id, "assistant", result["response"])

        return {
            "conversation_id": conversation.id,
            "response": result["response"],
            "tool_calls": result["tool_calls"]
        }

    except Exception as e:
        raise HTTPException(500, f"Chat error: {str(e)}")
```

**Update main.py:**
```python
from backend.routes import chat

app.include_router(chat.router)
```

**Spec References:**
- speckit.specify §7 (API Endpoints)
- speckit.plan §4 (Data Flow)

**Validation:**
- POST /chat creates conversation
- Message history persists
- Agent responses saved
- Stateless (no in-memory state)

**Estimated Time:** 35 minutes

---

## FRONTEND TASKS

### T-016: Better Auth Setup
**Preconditions:** T-003, T-007
**Implementation Steps:**
1. Create `frontend/lib/auth.ts`
2. Configure Better Auth with JWT plugin
3. Create signup/signin functions
4. Setup token storage
5. Create AuthContext

**Files to Create/Modify:**
- `frontend/lib/auth.ts` (new)
- `frontend/.env.local` (update)

**Code Template:**
```typescript
// [Task]: T-016
// [From]: speckit.plan §5

// lib/auth.ts
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  jwt: {
    enabled: true,
    expiresIn: "7d"
  }
});

export async function signup(email: string, name: string, password: string) {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/signup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, name, password })
  });

  if (!res.ok) throw new Error("Signup failed");

  const data = await res.json();
  localStorage.setItem("auth_token", data.token);
  localStorage.setItem("user_id", data.user.id);
  return data;
}

export async function signin(email: string, password: string) {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/signin`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });

  if (!res.ok) throw new Error("Invalid credentials");

  const data = await res.json();
  localStorage.setItem("auth_token", data.token);
  localStorage.setItem("user_id", data.user.id);
  return data;
}

export function signout() {
  localStorage.removeItem("auth_token");
  localStorage.removeItem("user_id");
}

export function getToken() {
  return localStorage.getItem("auth_token");
}

export function getUserId() {
  return localStorage.getItem("user_id");
}
```

**Spec References:**
- speckit.plan §5 (Better Auth Integration)

**Validation:**
- Signup creates account and stores token
- Signin returns token
- Token persists in localStorage

**Estimated Time:** 30 minutes

---

### T-017: Auth Pages
**Preconditions:** T-016
**Implementation Steps:**
1. Create `app/(auth)/signup/page.tsx`
2. Create `app/(auth)/signin/page.tsx`
3. Create signup form with validation
4. Create signin form with validation
5. Add loading states
6. Add error handling
7. Redirect to /chat on success

**Files to Create/Modify:**
- `frontend/app/(auth)/signup/page.tsx` (new)
- `frontend/app/(auth)/signin/page.tsx` (new)
- `frontend/components/auth/SignupForm.tsx` (new)
- `frontend/components/auth/SigninForm.tsx` (new)

**Code Template (Signup):**
```typescript
// [Task]: T-017
// [From]: speckit.plan §2.1

// app/(auth)/signup/page.tsx
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { signup } from "@/lib/auth";

export default function SignupPage() {
  const [email, setEmail] = useState("");
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const router = useRouter();

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      await signup(email, name, password);
      router.push("/chat");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Signup failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-600 to-blue-500">
      <div className="bg-white/10 backdrop-blur-lg p-8 rounded-2xl shadow-2xl w-full max-w-md">
        <h1 className="text-3xl font-bold text-white mb-6 text-center">Sign Up</h1>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-white mb-2">Name</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full px-4 py-2 rounded-lg bg-white/20 text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-white/50"
              placeholder="Your name"
              required
            />
          </div>

          <div>
            <label className="block text-white mb-2">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-2 rounded-lg bg-white/20 text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-white/50"
              placeholder="you@example.com"
              required
            />
          </div>

          <div>
            <label className="block text-white mb-2">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-2 rounded-lg bg-white/20 text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-white/50"
              placeholder="••••••••"
              required
              minLength={8}
            />
          </div>

          {error && (
            <div className="bg-red-500/20 border border-red-500 text-white px-4 py-2 rounded-lg">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-white text-purple-600 py-3 rounded-lg font-semibold hover:bg-white/90 disabled:opacity-50 transition"
          >
            {loading ? "Creating account..." : "Sign Up"}
          </button>
        </form>

        <p className="text-white/80 text-center mt-4">
          Already have an account?{" "}
          <a href="/signin" className="text-white font-semibold hover:underline">
            Sign in
          </a>
        </p>
      </div>
    </div>
  );
}
```

**Similar for Signin Page**

**Spec References:**
- speckit.specify §2 (Journey 1)
- speckit.plan §2.1 (Authentication Layer)

**Validation:**
- Forms validate input
- Signup creates account
- Signin logs in user
- Redirects to /chat
- Errors shown to user

**Estimated Time:** 45 minutes

---

### T-018: Protected Route Guard
**Preconditions:** T-016
**Implementation Steps:**
1. Create `app/(protected)/layout.tsx`
2. Check for auth token
3. Redirect to /signin if not authenticated
4. Wrap protected pages

**Files to Create/Modify:**
- `frontend/app/(protected)/layout.tsx` (new)

**Code Template:**
```typescript
// [Task]: T-018
// [From]: speckit.plan §2.1

"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getToken } from "@/lib/auth";

export default function ProtectedLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const token = getToken();
    if (!token) {
      router.push("/signin");
    } else {
      setLoading(false);
    }
  }, [router]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-600 to-blue-500">
        <div className="text-white text-xl">Loading...</div>
      </div>
    );
  }

  return <>{children}</>;
}
```

**Spec References:**
- speckit.specify §2 (Journey 4)

**Validation:**
- Unauthenticated users redirected
- Authenticated users see content

**Estimated Time:** 15 minutes

---

### T-019: API Client
**Preconditions:** T-016
**Implementation Steps:**
1. Create `frontend/lib/api.ts`
2. Create functions for all API endpoints
3. Attach JWT token to all requests
4. Handle errors

**Files to Create/Modify:**
- `frontend/lib/api.ts` (new)

**Code Template:**
```typescript
// [Task]: T-019
// [From]: speckit.plan §2.1

import { getToken, getUserId } from "./auth";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

async function fetchAPI(endpoint: string, options: RequestInit = {}) {
  const token = getToken();

  const res = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ message: "Request failed" }));
    throw new Error(error.message || "Request failed");
  }

  return res.json();
}

// Task API
export async function getTasks(status: string = "all") {
  const userId = getUserId();
  return fetchAPI(`/api/${userId}/tasks?status=${status}`);
}

export async function createTask(title: string, description: string = "") {
  const userId = getUserId();
  return fetchAPI(`/api/${userId}/tasks`, {
    method: "POST",
    body: JSON.stringify({ title, description }),
  });
}

export async function updateTask(taskId: number, title?: string, description?: string) {
  const userId = getUserId();
  return fetchAPI(`/api/${userId}/tasks/${taskId}`, {
    method: "PUT",
    body: JSON.stringify({ title, description }),
  });
}

export async function deleteTask(taskId: number) {
  const userId = getUserId();
  return fetchAPI(`/api/${userId}/tasks/${taskId}`, {
    method: "DELETE",
  });
}

export async function toggleComplete(taskId: number) {
  const userId = getUserId();
  return fetchAPI(`/api/${userId}/tasks/${taskId}/complete`, {
    method: "PATCH",
  });
}

// Chat API
export async function sendChatMessage(message: string, conversationId?: number) {
  const userId = getUserId();
  return fetchAPI(`/api/${userId}/chat`, {
    method: "POST",
    body: JSON.stringify({ message, conversation_id: conversationId }),
  });
}
```

**Spec References:**
- speckit.plan §3 (API Design)

**Validation:**
- All API calls include JWT
- Errors thrown correctly
- Type safety maintained

**Estimated Time:** 25 minutes

---

### T-020: Task UI Components
**Preconditions:** T-019
**Implementation Steps:**
1. Create `components/tasks/TaskCard.tsx`
2. Create `components/tasks/TaskList.tsx`
3. Create `components/tasks/TaskForm.tsx`
4. Add glassmorphic styling
5. Add animations (framer-motion)
6. Create `app/(protected)/tasks/page.tsx`

**Files to Create/Modify:**
- `frontend/components/tasks/TaskCard.tsx` (new)
- `frontend/components/tasks/TaskList.tsx` (new)
- `frontend/components/tasks/TaskForm.tsx` (new)
- `frontend/app/(protected)/tasks/page.tsx` (new)

**Code Template (TaskCard):**
```typescript
// [Task]: T-020
// [From]: speckit.plan §2.1

"use client";

import { motion } from "framer-motion";
import { useState } from "react";

interface Task {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
}

export function TaskCard({
  task,
  onToggle,
  onDelete,
  onUpdate,
}: {
  task: Task;
  onToggle: (id: number) => void;
  onDelete: (id: number) => void;
  onUpdate: (id: number, title: string, description: string) => void;
}) {
  const [editing, setEditing] = useState(false);
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || "");

  function handleSave() {
    onUpdate(task.id, title, description);
    setEditing(false);
  }

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="bg-white/10 backdrop-blur-lg rounded-xl p-4 shadow-lg border border-white/20"
    >
      {editing ? (
        <div className="space-y-2">
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full px-3 py-2 rounded-lg bg-white/20 text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-white/50"
          />
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full px-3 py-2 rounded-lg bg-white/20 text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-white/50"
            rows={3}
          />
          <div className="flex gap-2">
            <button
              onClick={handleSave}
              className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600"
            >
              Save
            </button>
            <button
              onClick={() => setEditing(false)}
              className="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600"
            >
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <>
          <div className="flex items-start justify-between mb-2">
            <div className="flex items-start gap-3 flex-1">
              <input
                type="checkbox"
                checked={task.completed}
                onChange={() => onToggle(task.id)}
                className="mt-1 w-5 h-5 rounded"
              />
              <div className="flex-1">
                <h3
                  className={`text-lg font-semibold text-white ${
                    task.completed ? "line-through opacity-60" : ""
                  }`}
                >
                  {task.title}
                </h3>
                {task.description && (
                  <p className="text-white/80 text-sm mt-1">{task.description}</p>
                )}
                <p className="text-white/50 text-xs mt-2">
                  {new Date(task.created_at).toLocaleDateString()}
                </p>
              </div>
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => setEditing(true)}
                className="text-white/80 hover:text-blue-400"
              >
                ✏️
              </button>
              <button
                onClick={() => confirm("Delete this task?") && onDelete(task.id)}
                className="text-white/80 hover:text-red-400"
              >
                🗑️
              </button>
            </div>
          </div>
        </>
      )}
    </motion.div>
  );
}
```

**Spec References:**
- speckit.specify §10 (UI/UX Requirements)
- speckit.plan §2.1 (Task Management UI)

**Validation:**
- Tasks display correctly
- Toggle completion works
- Edit/delete work
- Animations smooth

**Estimated Time:** 60 minutes

---

### T-021: Chat Interface
**Preconditions:** T-019
**Implementation Steps:**
1. Create `components/chat/ChatInterface.tsx`
2. Implement message sending
3. Display conversation history
4. Create `app/(protected)/chat/page.tsx`
5. Add auto-scroll to latest message
6. Add loading states

**Files to Create/Modify:**
- `frontend/components/chat/ChatInterface.tsx` (new)
- `frontend/app/(protected)/chat/page.tsx` (new)

**Code Template:**
```typescript
// [Task]: T-021
// [From]: speckit.plan §2.1

"use client";

import { useState, useEffect, useRef } from "react";
import { sendChatMessage } from "@/lib/api";

interface Message {
  role: "user" | "assistant";
  content: string;
}

export function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState<number | undefined>();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  async function handleSend() {
    if (!input.trim() || loading) return;

    const userMessage = input.trim();
    setInput("");
    setLoading(true);

    // Optimistically add user message
    setMessages((prev) => [...prev, { role: "user", content: userMessage }]);

    try {
      const response = await sendChatMessage(userMessage, conversationId);

      if (!conversationId) {
        setConversationId(response.conversation_id);
      }

      // Add assistant response
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: response.response },
      ]);
    } catch (error) {
      console.error("Chat error:", error);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Sorry, I encountered an error. Please try again." },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-purple-600 to-blue-500">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${
              msg.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`max-w-md px-4 py-3 rounded-2xl ${
                msg.role === "user"
                  ? "bg-white text-purple-600"
                  : "bg-white/10 backdrop-blur-lg text-white border border-white/20"
              }`}
            >
              {msg.content}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-white/10 backdrop-blur-lg text-white px-4 py-3 rounded-2xl border border-white/20">
              Thinking...
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="p-4 bg-white/10 backdrop-blur-lg border-t border-white/20">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === "Enter" && !loading && handleSend()}
            placeholder="Type a message to add a task, check your tasks, or complete tasks..."
            className="flex-1 px-4 py-3 rounded-full bg-white/20 text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-white/50"
            disabled={loading}
          />
          <button
            onClick={handleSend}
            disabled={loading || !input.trim()}
            className="px-6 py-3 bg-white text-purple-600 rounded-full font-semibold hover:bg-white/90 disabled:opacity-50 transition"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
```

**Spec References:**
- speckit.specify §2 (Journey 2)
- speckit.plan §2.1 (Chat Interface)

**Validation:**
- Messages send correctly
- History persists
- UI responsive
- Loading states work
- Auto-scroll to bottom

**Estimated Time:** 50 minutes

---

## INTEGRATION & TESTING TASKS

### T-022: End-to-End Testing
**Preconditions:** All previous tasks
**Implementation Steps:**
1. Test full signup → signin flow
2. Test task creation via UI
3. Test task creation via chat
4. Test task completion via both interfaces
5. Test conversation persistence
6. Test JWT validation
7. Test error handling
8. Fix any bugs found

**Validation Checklist:**
- [X] User can signup and signin
- [X] JWT token works on all endpoints
- [X] Tasks can be created via UI
- [X] Tasks can be created via chat
- [X] Chat understands natural language
- [X] MCP tools execute correctly
- [X] Conversation history persists
- [X] User data isolated
- [X] 403 returned for wrong user_id
- [X] All API endpoints work correctly
- [X] Frontend UI responsive
- [X] Glassmorphic design implemented
- [X] Animations smooth
- [X] Error states handled
- [X] Loading states work

**Files to Test:**
- All frontend components
- All backend endpoints
- All MCP tools
- All authentication flows

**Spec References:**
- speckit.specify §5 (Acceptance Criteria)
- speckit.plan §10 (Testing Strategy)

**Estimated Time:** 60 minutes