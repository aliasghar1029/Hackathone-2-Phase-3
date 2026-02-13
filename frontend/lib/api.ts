const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://white-000-hackatho-2-phase-2.hf.space';

export async function signup(name: string, email: string, password: string) {
  const res = await fetch(`${API_URL}/api/auth/signup`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, email, password })
  });
  if (!res.ok) {
    const error = await res.json().catch(() => ({ message: 'Signup failed' }));
    throw new Error(error.message || 'Signup failed');
  }
  return res.json();
}

export async function signin(email: string, password: string) {
  const res = await fetch(`${API_URL}/api/auth/signin`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  if (!res.ok) {
    const error = await res.json().catch(() => ({ message: 'Invalid credentials' }));
    throw new Error(error.message || 'Invalid credentials');
  }
  return res.json();
}

export async function getTasks(userId: string, token: string, status = 'all') {
  const res = await fetch(`${API_URL}/api/${userId}/tasks?status=${status}`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  if (!res.ok) throw new Error('Failed to fetch tasks');
  return res.json();
}

export async function createTask(userId: string, token: string, title: string, description: string) {
  const res = await fetch(`${API_URL}/api/${userId}/tasks`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ title, description })
  });
  if (!res.ok) throw new Error('Failed to create task');
  return res.json();
}

export async function updateTask(userId: string, token: string, taskId: number, title: string, description: string) {
  const res = await fetch(`${API_URL}/api/${userId}/tasks/${taskId}`, {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ title, description })
  });
  if (!res.ok) throw new Error('Failed to update task');
  return res.json();
}

export async function deleteTask(userId: string, token: string, taskId: number) {
  const res = await fetch(`${API_URL}/api/${userId}/tasks/${taskId}`, {
    method: 'DELETE',
    headers: { 'Authorization': `Bearer ${token}` }
  });
  if (!res.ok) throw new Error('Failed to delete task');
  return res.json();
}

export async function toggleComplete(userId: string, token: string, taskId: number) {
  const res = await fetch(`${API_URL}/api/${userId}/tasks/${taskId}/complete`, {
    method: 'PATCH',
    headers: { 'Authorization': `Bearer ${token}` }
  });
  if (!res.ok) throw new Error('Failed to toggle task');
  return res.json();
}

export interface ChatMessage {
  conversation_id: number;
  response: string;
  tool_calls: Array<{
    tool: string;
    args: any;
    result: any;
  }>;
}

export async function sendChatMessage(
  userId: string,
  token: string,
  message: string,
  conversationId?: number
): Promise<ChatMessage> {
  const res = await fetch(`${API_URL}/api/${userId}/chat`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      message,
      conversation_id: conversationId
    })
  });
  
  if (!res.ok) throw new Error('Failed to send message');
  return res.json();
}