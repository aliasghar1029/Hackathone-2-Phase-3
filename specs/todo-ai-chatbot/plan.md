# TODO AI CHATBOT - TECHNICAL PLAN

## 1. System Architecture

### High-Level Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   AUTH      │  │    TASKS    │  │    CHAT     │            │
│  │   LAYER     │  │   UI        │  │   UI        │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
└─────────────────────────────────────────────────────────────────┘
                                │
                       HTTP/SSE │ API calls with JWT
                                │
┌─────────────────────────────────────────────────────────────────┐
│                        BACKEND                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │ AUTH        │  │ TASK        │  │   CHAT      │            │
│  │ SERVICE     │  │ SERVICE     │  │   SERVICE   │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
│         │               │                   │                  │
│         │               │                   │                  │
│         └───────────────┼───────────────────┘                  │
│                         │                                      │
│              ┌─────────────────────────┐                       │
│              │    MCP SERVER         │                       │
│              │  (5 AI TOOLS)         │                       │
│              └─────────────────────────┘                       │
└─────────────────────────────────────────────────────────────────┘
                                │
                           DATABASE │ Queries with user_id
                                │
┌─────────────────────────────────────────────────────────────────┐
│                      NEON POSTGRESQL                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   users     │  │   tasks     │  │ conversations│           │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
│                                    │  ┌─────────────┐         │
│                                    │  │   messages  │         │
│                                    │  └─────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

## 2. Component Breakdown

### 2.1 Frontend Components

#### Authentication Layer
**Components:**
- `SignupPage` - User registration form
- `SigninPage` - User login form
- `AuthGuard` - Protected route wrapper
- `AuthContext` - Global auth state

**Responsibilities:**
- Form validation
- API calls to auth endpoints
- JWT token storage (httpOnly cookies or localStorage)
- Redirect logic

**Files:**
```
frontend/
├── app/
│   ├── (auth)/
│   │   ├── signup/page.tsx
│   │   └── signin/page.tsx
│   └── (protected)/
│       ├── layout.tsx  # AuthGuard
│       ├── chat/page.tsx
│       └── tasks/page.tsx
├── components/
│   ├── auth/
│   │   ├── SignupForm.tsx
│   │   └── SigninForm.tsx
├── lib/
│   ├── auth.ts  # Better Auth config
│   └── api.ts   # API client with JWT
```

#### Task Management UI
**Components:**
- `TaskList` - Display all tasks
- `TaskCard` - Individual task item
- `TaskForm` - Add/edit task modal
- `TaskFilters` - Status filter buttons

**Responsibilities:**
- CRUD operations via REST API
- Optimistic UI updates
- Loading and error states
- Animations (framer-motion)

**Files:**
```
frontend/
├── components/
│   ├── tasks/
│   │   ├── TaskList.tsx
│   │   ├── TaskCard.tsx
│   │   ├── TaskForm.tsx
│   │   └── TaskFilters.tsx
│   └── ui/
│       ├── Button.tsx
│       ├── Input.tsx
│       ├── Modal.tsx
│       └── Card.tsx
```

#### Chat Interface
**Components:**
- `ChatInterface` - Main chat container (OpenAI ChatKit)
- `MessageBubble` - User/Assistant message
- `ChatInput` - Message input field
- `ConversationList` - Previous conversations

**Responsibilities:**
- Send messages to chat endpoint
- Display message history
- Handle streaming responses (if applicable)
- Auto-scroll to latest message

**Files:**
```
frontend/
├── components/
│   ├── chat/
│   │   ├── ChatInterface.tsx  # ChatKit wrapper
│   │   ├── MessageBubble.tsx
│   │   ├── ChatInput.tsx
│   │   └── ConversationList.tsx
```

### 2.2 Backend Components

#### Authentication Service
**Module:** `backend/services/auth.py`

**Functions:**
- `signup(email, name, password)` → Creates user, returns JWT
- `signin(email, password)` → Validates, returns JWT
- `verify_token(token)` → Decodes JWT, returns user_id
- `hash_password(password)` → Bcrypt hash
- `verify_password(password, hash)` → Bcrypt verify

**Dependencies:**
- `passlib[bcrypt]` for password hashing
- `python-jose[cryptography]` for JWT

#### Task Service (REST API)
**Module:** `backend/services/tasks.py`

**Functions:**
- `create_task(user_id, title, description)` → Task
- `get_tasks(user_id, status)` → List[Task]
- `get_task(user_id, task_id)` → Task
- `update_task(user_id, task_id, data)` → Task
- `delete_task(user_id, task_id)` → bool
- `toggle_complete(user_id, task_id)` → Task

**Validation:**
- User owns the task
- Title length (1-200 chars)
- Description length (max 1000 chars)

#### Chat Service
**Module:** `backend/services/chat.py`

**Functions:**
- `send_message(user_id, conversation_id, message)` → Response
- `get_or_create_conversation(user_id, conversation_id)` → Conversation
- `load_history(conversation_id)` → List[Message]
- `save_message(conversation_id, role, content)` → Message
- `run_agent(messages, tools)` → Agent response

**Flow:**
1. Receive user message
2. Fetch conversation history from DB
3. Build message array (history + new message)
4. Store user message
5. Call OpenAI Agent with MCP tools
6. Store assistant response
7. Return response

#### MCP Server
**Module:** `backend/mcp/server.py`

**Tools:**
1. **add_task**
   - Input schema: `{user_id: str, title: str, description: str}`
   - Calls: `tasks.create_task()`
   - Returns: `{task_id, status, title}`

2. **list_tasks**
   - Input schema: `{user_id: str, status: str}`
   - Calls: `tasks.get_tasks()`
   - Returns: `[{id, title, completed, created_at}]`

3. **complete_task**
   - Input schema: `{user_id: str, task_id: int}`
   - Calls: `tasks.toggle_complete()`
   - Returns: `{task_id, status, title}`

4. **delete_task**
   - Input schema: `{user_id: str, task_id: int}`
   - Calls: `tasks.delete_task()`
   - Returns: `{task_id, status, title}`

5. **update_task**
   - Input schema: `{user_id: str, task_id: int, title: str, description: str}`
   - Calls: `tasks.update_task()`
   - Returns: `{task_id, status, title}`

**Implementation:**
- Use Official MCP Python SDK
- Each tool is stateless
- All tools validate user_id matches
- Proper error handling

### 2.3 Database Layer

#### Models (SQLModel)
**File:** `backend/models.py`
```python
# User (managed by Better Auth, read-only for us)
class User(SQLModel, table=True):
    id: str = Field(primary_key=True)
    email: str = Field(unique=True)
    name: str
    password_hash: str
    created_at: datetime
    updated_at: datetime

# Task
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(max_length=1000)
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Conversation
class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Message
class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id", index=True)
    user_id: str = Field(foreign_key="user.id")
    role: str = Field(regex="^(user|assistant)$")
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

#### Database Connection
**File:** `backend/db.py`
```python
from sqlmodel import create_engine, Session, SQLModel
import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
```

#### Indexes
- `tasks.user_id` - Filter by user
- `tasks.completed` - Filter by status
- `conversations.user_id` - Filter by user
- `messages.conversation_id` - Load chat history

## 3. API Design

### REST Endpoints

#### Authentication
```
POST /api/auth/signup
Body: {email, name, password}
Response: {user, token}

POST /api/auth/signin
Body: {email, password}
Response: {user, token}
```

#### Tasks
```
GET /api/{user_id}/tasks?status=all|pending|completed
Headers: Authorization: Bearer <token>
Response: [{id, title, description, completed, created_at}]

POST /api/{user_id}/tasks
Headers: Authorization: Bearer <token>
Body: {title, description?}
Response: {id, title, description, completed, created_at}

GET /api/{user_id}/tasks/{task_id}
Headers: Authorization: Bearer <token>
Response: {id, title, description, completed, created_at}

PUT /api/{user_id}/tasks/{task_id}
Headers: Authorization: Bearer <token>
Body: {title?, description?}
Response: {id, title, description, completed, created_at}

DELETE /api/{user_id}/tasks/{task_id}
Headers: Authorization: Bearer <token>
Response: {success: true}

PATCH /api/{user_id}/tasks/{task_id}/complete
Headers: Authorization: Bearer <token>
Response: {id, completed, updated_at}
```

#### Chat
```
POST /api/{user_id}/chat
Headers: Authorization: Bearer <token>
Body: {conversation_id?, message}
Response: {
  conversation_id,
  response,
  tool_calls: [{tool, args, result}]
}
```

### Authentication Flow

1. **User signs up** → POST /api/auth/signup
   - Backend hashes password
   - Stores user in database
   - Generates JWT with `{user_id, email, exp}`
   - Returns token

2. **User signs in** → POST /api/auth/signin
   - Backend verifies password
   - Generates JWT
   - Returns token

3. **Protected request** → Any /api/{user_id}/* endpoint
   - Frontend sends: `Authorization: Bearer <token>`
   - Backend middleware:
     - Extracts token
     - Verifies signature
     - Decodes user_id
     - Matches user_id in URL
     - If mismatch → 403 Forbidden
     - If valid → Proceeds to handler

## 4. Data Flow Diagrams

### Task Creation via Chat
```
User: "Add a task to buy groceries"
  │
  ├─> Frontend: POST /api/user123/chat
  │   Body: {message: "Add a task to buy groceries"}
  │
  ├─> Backend: Chat Endpoint
  │   ├─> Load conversation history from DB
  │   ├─> Store user message
  │   └─> Call OpenAI Agent
  │       ├─> Agent analyzes message
  │       ├─> Agent decides to call add_task tool
  │       └─> MCP Server: add_task({user_id: "user123", title: "Buy groceries"})
  │           ├─> Validate user_id
  │           ├─> Insert into tasks table
  │           └─> Return {task_id: 42, status: "created", title: "Buy groceries"}
  │
  ├─> Agent receives tool result
  ├─> Agent generates response: "I've added 'Buy groceries' to your tasks."
  ├─> Backend stores assistant message
  │
  └─> Frontend receives: {conversation_id: 1, response: "I've added 'Buy groceries' to your tasks."}
```

### Task Listing via UI
```
User: Clicks "View Tasks"
  │
  ├─> Frontend: GET /api/user123/tasks?status=all
  │
  ├─> Backend: Task Endpoint
  │   ├─> Verify JWT (user_id matches)
  │   ├─> Query: SELECT * FROM tasks WHERE user_id = 'user123'
  │   └─> Return [{id: 42, title: "Buy groceries", completed: false}]
  │
  └─> Frontend: Displays task cards with animations
```

## 5. Technology Integration Details

### Better Auth + FastAPI JWT

**Setup:**
1. Better Auth on frontend issues JWT after login
2. Frontend stores token (localStorage or httpOnly cookie)
3. Frontend sends token in `Authorization: Bearer <token>` header
4. Backend validates token using shared secret

**Backend Middleware:**
```python
from fastapi import Header, HTTPException
from jose import jwt

async def verify_jwt(authorization: str = Header()):
    try:
        token = authorization.replace("Bearer ", "")
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except:
        raise HTTPException(401, "Invalid token")
```

### OpenAI Agents SDK + MCP

**Setup:**
1. Create MCP server with 5 tools
2. Initialize OpenAI Agent with tools
3. Agent receives user message
4. Agent calls appropriate tool(s)
5. MCP server executes tool logic
6. Agent receives result and responds

**Code Structure:**
```python
from openai_agents_sdk import Agent, Runner
from mcp import MCPServer, Tool

# Define MCP tools
mcp_server = MCPServer()

@mcp_server.tool()
def add_task(user_id: str, title: str, description: str = ""):
    # Implementation
    pass

# Create agent
agent = Agent(
    name="Todo Assistant",
    model="gpt-4",
    instructions="You help users manage their tasks...",
    tools=[mcp_server.get_tools()]
)

# Run agent
response = Runner.run(agent, messages=[{"role": "user", "content": message}])
```

### Neon PostgreSQL

**Connection:**
```python
DATABASE_URL = "postgresql://user:pass@ep-xyz.us-east-2.aws.neon.tech/dbname?sslmode=require"
engine = create_engine(DATABASE_URL)
```

**Migration:**
```python
# backend/migrations/init_db.py
from sqlmodel import SQLModel
from db import engine

def migrate():
    SQLModel.metadata.create_all(engine)
```

## 6. File Structure
```
todo-ai-chatbot/
├── frontend/
│   ├── app/
│   │   ├── (auth)/
│   │   │   ├── signup/page.tsx
│   │   │   └── signin/page.tsx
│   │   ├── (protected)/
│   │   │   ├── layout.tsx  # AuthGuard
│   │   │   ├── chat/page.tsx
│   │   │   └── tasks/page.tsx
│   │   └── globals.css
│   ├── components/
│   │   ├── auth/
│   │   │   ├── SignupForm.tsx
│   │   │   └── SigninForm.tsx
│   │   ├── tasks/
│   │   │   ├── TaskList.tsx
│   │   │   ├── TaskCard.tsx
│   │   │   ├── TaskForm.tsx
│   │   │   └── TaskFilters.tsx
│   │   ├── chat/
│   │   │   ├── ChatInterface.tsx  # ChatKit wrapper
│   │   │   ├── MessageBubble.tsx
│   │   │   ├── ChatInput.tsx
│   │   │   └── ConversationList.tsx
│   │   └── ui/
│   │       ├── Button.tsx
│   │       ├── Input.tsx
│   │       ├── Modal.tsx
│   │       └── Card.tsx
│   ├── lib/
│   │   ├── auth.ts  # Better Auth config
│   │   └── api.ts   # API client with JWT
│   ├── public/
│   └── package.json
├── backend/
│   ├── app.py
│   ├── models.py
│   ├── db.py
│   ├── services/
│   │   ├── auth.py
│   │   ├── tasks.py
│   │   └── chat.py
│   ├── mcp/
│   │   └── server.py
│   ├── middleware/
│   │   └── jwt.py
│   ├── .env
│   ├── requirements.txt
│   └── pyproject.toml
├── specs/
│   └── todo-ai-chatbot/
│       ├── spec.md
│       └── plan.md  # This file
├── .env.local
├── CLAUDE.md
├── AGENTS.md
└── README.md
```

## 7. Deployment Architecture

### Local Development
```
Frontend: http://localhost:3000 (Next.js dev server)
Backend: http://localhost:8000 (Uvicorn)
Database: Neon cloud (no local DB needed)
```

### Production (Phase IV & V)
```
Frontend: Vercel (auto-deploy from main branch)
Backend: Docker → Kubernetes → DigitalOcean
Database: Neon production tier
```

## 8. Security Architecture

### JWT Flow
1. User logs in → Backend generates JWT
2. JWT contains: `{user_id, email, exp: 7days}`
3. Frontend stores JWT
4. Every API call includes: `Authorization: Bearer <JWT>`
5. Backend middleware validates signature
6. Backend extracts user_id from token
7. Backend compares token user_id with URL user_id
8. If mismatch → 403, else proceed

### Data Isolation
- All queries filtered by `user_id`
- No way for user A to access user B's tasks
- MCP tools validate user_id on every call

## 9. Implementation Phases

### Phase 1: Foundation (Console App - Conceptual)
- Setup project structure
- Define models
- Basic CRUD logic (not implemented in web version)

### Phase 2: Web Application
- Build authentication flow
- Create task REST API
- Build task management UI
- Setup database with Neon

### Phase 3: AI Chatbot (Current)
- Implement MCP server with 5 tools
- Integrate OpenAI Agents SDK
- Create chat endpoint
- Build ChatKit interface
- Add conversation persistence

## 10. Testing Strategy

### Unit Tests
- Auth service (signup, signin, token verification)
- Task service (CRUD operations)
- MCP tools (each tool independently)

### Integration Tests
- Auth flow (signup → signin → protected route)
- Chat flow (message → agent → tool → response)
- Task lifecycle (create → list → update → complete → delete)

### E2E Tests
- User signup → Create task via chat → View in UI
- User login → Create task in UI → Ask about it in chat
- Multiple conversations persist correctly

## 11. Performance Optimizations

### Frontend
- Server Components for static content
- Dynamic imports for heavy components
- Image optimization (next/image)
- API response caching (SWR or React Query)

### Backend
- Database connection pooling
- Async/await throughout
- Indexed queries
- Pagination for task lists (limit 100)

### Database
- Indexes on foreign keys
- Efficient queries (no N+1)
- Connection pooling via SQLModel

## 12. Monitoring & Observability

### Logs
- Structured logging (JSON)
- Request/response logging
- Error tracking

### Metrics
- API response times
- Chat response times
- Tool call frequency
- Database query performance

### Health Checks
- GET /health → {status: "ok", db: "connected"}

## 13. Error Handling Strategy

### Frontend
- Try/catch on all API calls
- Toast notifications for errors
- Error boundaries for component crashes
- Fallback UI for failed loads

### Backend
- Custom exception classes
- HTTP exception handlers
- Database transaction rollback
- Graceful degradation

## 14. Environment Configuration

### Development
```
Frontend: .env.local
Backend: .env
Database: Neon development branch
```

### Production
```
Frontend: Vercel environment variables
Backend: Kubernetes secrets
Database: Neon production
```

## 15. Success Criteria

### Functional
- ✓ All CRUD operations work via UI
- ✓ All CRUD operations work via chat
- ✓ Authentication flow complete
- ✓ JWT validation working
- ✓ Conversation persistence working
- ✓ MCP tools executing correctly

### Non-Functional
- ✓ API response < 200ms (non-AI)
- ✓ Chat response < 3s
- ✓ UI responsive on all devices
- ✓ No user data leakage
- ✓ Graceful error handling

### Code Quality
- ✓ Type safety (TypeScript + Python type hints)
- ✓ Code references spec sections
- ✓ Proper error handling
- ✓ Clean architecture (separation of concerns)