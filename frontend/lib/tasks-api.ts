// lib/tasks-api.ts
import { apiClient } from './api';

export interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

export interface TaskCreate {
  title: string;
  description?: string;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  completed?: boolean;
}

// Tasks API functions
export const tasksApi = {
  // Get all tasks for a user
  getTasks: async (userId: string, statusParam: 'all' | 'completed' | 'pending' = 'all'): Promise<{ data?: Task[]; error?: string }> => {
    return apiClient.get<Task[]>(`/api/${userId}/tasks?status_param=${statusParam}`);
  },

  // Create a new task
  createTask: async (userId: string, taskData: TaskCreate): Promise<{ data?: Task; error?: string }> => {
    return apiClient.post<Task>(`/api/${userId}/tasks`, taskData);
  },

  // Update an existing task
  updateTask: async (userId: string, taskId: string, taskData: TaskUpdate): Promise<{ data?: Task; error?: string }> => {
    return apiClient.put<Task>(`/api/${userId}/tasks/${taskId}`, taskData);
  },

  // Delete a task
  deleteTask: async (userId: string, taskId: string): Promise<{ data?: any; error?: string }> => {
    return apiClient.delete<any>(`/api/${userId}/tasks/${taskId}`);
  },

  // Toggle task completion status
  toggleTaskCompletion: async (userId: string, taskId: string): Promise<{ data?: Task; error?: string }> => {
    return apiClient.patch<Task>(`/api/${userId}/tasks/${taskId}/complete`, {});
  },
};