// lib/api.ts
import { toast } from 'sonner';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://white-000-cahtbot.hf.space';

interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
}

class ApiClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = `${API_BASE_URL}`;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    const url = `${this.baseUrl}${endpoint}`;

    // Get token from localStorage if available
    const token = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null;

    const headers = {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
      ...options.headers,
    };

    try {
      const response = await fetch(url, {
        ...options,
        headers,
      });

      // Handle different response status codes appropriately
      if (response.status === 401) {
        // Unauthorized - check if this is an auth endpoint (signin/signup) or a protected endpoint
        const isAuthEndpoint = endpoint.includes('/auth/signin') || endpoint.includes('/auth/signup');
        
        if (!isAuthEndpoint) {
          // This is a protected endpoint, so token likely expired
          // Only clear local storage if we're certain it's an expired token scenario
          // Check if we had a token before making this request
          const hadToken = token && token.length > 0;
          
          if (hadToken) {
            localStorage.removeItem('auth_token');
            localStorage.removeItem('user');
          }
          
          const errorMessage = 'Session expired. Please sign in again.';
          toast.error(errorMessage);
          throw new Error(errorMessage);
        } else {
          // This is an auth endpoint, so it's a login/signup failure, not an expired session
          let errorMessage = 'Unauthorized: Invalid credentials';
          
          try {
            const errorData = await response.json();
            errorMessage = errorData.detail || errorData.message || errorMessage;
          } catch (parseError) {
            console.warn('Could not parse auth error response:', parseError);
          }
          
          // Don't clear tokens on auth failure - they might still be valid for other purposes
          toast.error(errorMessage);
          throw new Error(errorMessage);
        }
      }

      if (response.status === 403) {
        // Forbidden - user doesn't have permission
        toast.error('Access forbidden. You do not have permission to perform this action.');
        throw new Error('Forbidden: Access denied');
      }

      if (response.status >= 400 && response.status < 600) {
        // Handle other error statuses
        let errorMessage = `HTTP error! status: ${response.status}`;
        
        try {
          const errorData = await response.json();
          errorMessage = errorData.detail || errorData.message || errorMessage;
        } catch (parseError) {
          // If we can't parse the error response, use the status code
          console.warn('Could not parse error response:', parseError);
        }

        toast.error(errorMessage);
        throw new Error(errorMessage);
      }

      const responseData = await response.json();
      return { data: responseData };
    } catch (error: any) {
      console.error(`API request failed: ${endpoint}`, error);
      
      // Handle network errors specifically
      if (error instanceof TypeError && error.message.includes('fetch')) {
        const networkErrorMessage = 'Network error. Please check your connection and try again.';
        toast.error(networkErrorMessage);
        throw new Error(networkErrorMessage);
      }
      
      // Show error toast for other errors
      const errorMessage = error.message || 'An error occurred while making the request';
      toast.error(errorMessage);
      
      return { error: errorMessage };
    }
  }

  get<T>(endpoint: string) {
    return this.request<T>(endpoint, { method: 'GET' });
  }

  post<T>(endpoint: string, body: any) {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(body),
    });
  }

  put<T>(endpoint: string, body: any) {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: JSON.stringify(body),
    });
  }

  patch<T>(endpoint: string, body: any) {
    return this.request<T>(endpoint, {
      method: 'PATCH',
      body: JSON.stringify(body),
    });
  }

  delete<T>(endpoint: string) {
    return this.request<T>(endpoint, { method: 'DELETE' });
  }
}

export const apiClient = new ApiClient();

// Health check function
export const checkApiHealth = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    return response.ok;
  } catch (error) {
    console.error('API health check failed:', error);
    return false;
  }
};