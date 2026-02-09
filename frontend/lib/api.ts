// [Task]: T-019
// [From]: speckit.plan §2.1

import { getToken, getUserId } from "./auth";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

async function fetchAPI(endpoint: string, options: RequestInit = {}) {
  const token = getToken();
  const userId = getUserId();

  // Check if user is authenticated for protected routes
  if (endpoint.includes('/api/') && !endpoint.includes('/api/auth/') && !token) {
    throw new Error("Authentication required");
  }

  const res = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  });

  if (!res.ok) {
    if (res.status === 401) {
      // Clear auth data if unauthorized
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user_id');
      window.location.href = '/signin';
      throw new Error("Session expired. Please sign in again.");
    }
    
    let error;
    try {
      error = await res.json();
    } catch (e) {
      error = { message: `Request failed with status ${res.status}` };
    }
    
    throw new Error(error.message || `Request failed with status ${res.status}`);
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