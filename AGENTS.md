# TODO AI Chatbot - MCP Integration

## Project Description
An AI-powered todo management application that allows users to manage tasks through both traditional UI and natural language conversation.

## Agent Configuration
- **Name**: TODO AI Chatbot Agent
- **Description**: Helps users manage their tasks through natural language conversation
- **Instructions**: You are a helpful todo assistant. You help users manage their tasks through natural language.
- **Model**: gpt-4
- **Tools**: MCP server tools for task management

## MCP Server Tools
- add_task: Create a new task
- list_tasks: List tasks with optional status filter
- complete_task: Mark a task as complete
- delete_task: Delete a task
- update_task: Update task title or description

## Capabilities
- Create tasks via natural language
- List existing tasks
- Mark tasks as complete/incomplete
- Delete tasks
- Update task details
- Maintain conversation context