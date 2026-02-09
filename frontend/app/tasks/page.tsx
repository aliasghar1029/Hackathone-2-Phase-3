// [Task]: T-032
// [From]: speckit.plan §2.1

import { TaskList } from '@/components/tasks/TaskList';

export default function TasksPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 to-blue-900 p-6">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent mb-2">Your Tasks</h1>
          <p className="text-white/70">Manage your tasks in a traditional list view</p>
        </div>

        <TaskList />
      </div>
    </div>
  );
}