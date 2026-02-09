# TODO AI Chatbot

A modern, AI-powered todo management application that allows users to manage tasks through both traditional UI and natural language conversation.

## Features

- Natural language task management via AI chatbot
- Traditional task management UI
- Secure authentication with JWT
- Persistent conversations
- Real-time task synchronization
- Beautiful glassmorphic UI design

## Tech Stack

- Frontend: Next.js 14+, TypeScript, Tailwind CSS, Framer Motion
- Backend: FastAPI, Python, SQLModel, Neon PostgreSQL
- AI: OpenAI Agents SDK, MCP Server
- Authentication: Better Auth

## Installation

1. Clone the repository
2. Install dependencies:
   - Frontend: `cd frontend && npm install`
   - Backend: `cd backend && uv install`
3. Set up environment variables
4. Start the development servers

## Environment Variables

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend (.env)
```env
DATABASE_URL=your_neon_database_url
OPENAI_API_KEY=your_openai_api_key
JWT_SECRET=your_jwt_secret
```

## Development

Start the backend:
```bash
cd backend
uv run uvicorn main:app --reload
```

Start the frontend:
```bash
cd frontend
npm run dev
```

## Architecture

The application follows a microservice architecture with:
- Frontend: Next.js 14+ with App Router
- Backend: FastAPI with REST API
- Database: Neon PostgreSQL
- AI Layer: OpenAI Agents with MCP tools

## Project Structure

```
todo-ai-chatbot/
├── backend/          # FastAPI backend
│   ├── models.py     # Database models
│   ├── db.py         # Database connection
│   ├── services/     # Business logic
│   ├── routes/       # API routes
│   ├── mcp/          # MCP server
│   └── middleware/   # Authentication middleware
├── frontend/         # Next.js frontend
│   ├── app/          # App Router pages
│   ├── components/   # Reusable components
│   │   ├── auth/     # Authentication components
│   │   ├── tasks/    # Task management components
│   │   ├── chat/     # Chat interface components
│   │   └── ui/       # Base UI components
│   └── lib/          # Utility functions
├── specs/            # Specification documents
│   └── todo-ai-chatbot/
│       ├── spec.md   # Requirements
│       ├── plan.md   # Architecture
│       └── tasks.md  # Implementation tasks
└── history/          # Prompt History Records
    └── prompts/
```

## MCP Tools

The application uses MCP (Model Context Protocol) to connect the AI agent with database operations:

- `add_task`: Create a new task
- `list_tasks`: List tasks with optional status filter
- `complete_task`: Mark a task as complete
- `delete_task`: Delete a task
- `update_task`: Update task title or description

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT