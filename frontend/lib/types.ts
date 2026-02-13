export interface User {
  id: string;
  email: string;
  name: string;
}

export interface AuthState {
  user: User | null;
  token: string | null;
}

export interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
  updated_at?: string;
  user_id: string;
}

export type TaskFilter = "all" | "pending" | "completed";
