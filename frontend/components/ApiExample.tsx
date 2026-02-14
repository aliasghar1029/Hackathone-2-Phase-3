// components/ApiExample.tsx
'use client';

import React, { useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { tasksApi, TaskCreate } from '@/lib/tasks-api';
import { chatApi } from '@/lib/chat-api';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";

const ApiExample: React.FC = () => {
  const { user, isAuthenticated } = useAuth();
  const [taskTitle, setTaskTitle] = useState('');
  const [taskDescription, setTaskDescription] = useState('');
  const [chatMessage, setChatMessage] = useState('');
  const [chatResponse, setChatResponse] = useState('');
  const [tasks, setTasks] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const handleCreateTask = async () => {
    if (!user?.id || !taskTitle.trim()) return;

    setLoading(true);
    try {
      const taskData: TaskCreate = {
        title: taskTitle,
        description: taskDescription
      };

      const result = await tasksApi.createTask(user.id, taskData);
      if (result.data) {
        setTasks([...tasks, result.data]);
        setTaskTitle('');
        setTaskDescription('');
      }
    } catch (error) {
      console.error('Error creating task:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSendMessage = async () => {
    if (!user?.id || !chatMessage.trim()) return;

    setLoading(true);
    try {
      const result = await chatApi.sendMessage(user.id, chatMessage);
      if (result.data) {
        setChatResponse(result.data.response);
        setChatMessage('');
      }
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <Card className="mb-6">
        <CardHeader>
          <CardTitle>API Connection Status</CardTitle>
          <CardDescription>
            {isAuthenticated 
              ? `Connected as ${user?.name} (${user?.email})` 
              : 'Not authenticated'}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <p>User ID: {user?.id || 'N/A'}</p>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Task Creation Example */}
        <Card>
          <CardHeader>
            <CardTitle>Create Task</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <Input
                value={taskTitle}
                onChange={(e) => setTaskTitle(e.target.value)}
                placeholder="Task title"
              />
              <Input
                value={taskDescription}
                onChange={(e) => setTaskDescription(e.target.value)}
                placeholder="Task description (optional)"
              />
              <Button onClick={handleCreateTask} disabled={loading || !taskTitle.trim()}>
                {loading ? 'Creating...' : 'Create Task'}
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Chat Example */}
        <Card>
          <CardHeader>
            <CardTitle>Chat with AI</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <Input
                value={chatMessage}
                onChange={(e) => setChatMessage(e.target.value)}
                placeholder="Type your message..."
              />
              <Button onClick={handleSendMessage} disabled={loading || !chatMessage.trim()}>
                {loading ? 'Sending...' : 'Send Message'}
              </Button>
              
              {chatResponse && (
                <div className="mt-4 p-4 bg-gray-100 rounded-md">
                  <h4 className="font-semibold mb-2">AI Response:</h4>
                  <p>{chatResponse}</p>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default ApiExample;