'use client';

import React, { useState } from 'react';
import { TaskFilter } from '@/types/task';

interface TaskFilterComponentProps {
  onFilterChange: (filters: TaskFilter) => void;
}

const TaskFilterComponent: React.FC<TaskFilterComponentProps> = ({ onFilterChange }) => {
  const [status, setStatus] = useState<string>('');
  const [priority, setPriority] = useState<string>('');
  const [tags, setTags] = useState<string>('');
  const [hasRecurrence, setHasRecurrence] = useState<string>('');
  const [dueDateStart, setDueDateStart] = useState<string>('');
  const [dueDateEnd, setDueDateEnd] = useState<string>('');
  const [completed, setCompleted] = useState<string>('');
  const [search, setSearch] = useState<string>('');

  const handleApplyFilters = () => {
    const filters: TaskFilter = {};

    if (status) filters.status = status as any;
    if (priority) filters.priority = priority as any;
    if (tags) filters.tags = tags;  // Add tags filter
    if (hasRecurrence !== '') {
      filters.has_recurrence = hasRecurrence === 'true';  // Add recurrence filter
    }
    if (dueDateStart) filters.due_date_start = dueDateStart;
    if (dueDateEnd) filters.due_date_end = dueDateEnd;
    if (completed !== '') filters.completed = completed === 'true';
    if (search) filters.search = search;

    onFilterChange(filters);
  };

  const handleClearFilters = () => {
    setStatus('');
    setPriority('');
    setTags('');
    setHasRecurrence('');
    setDueDateStart('');
    setDueDateEnd('');
    setCompleted('');
    setSearch('');

    onFilterChange({});
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow mb-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">Filter Tasks</h3>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
          <select
            value={status}
            onChange={(e) => setStatus(e.target.value)}
            className="w-full text-black p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Statuses</option>
            <option value="pending">Pending</option>
            <option value="in-progress">In Progress</option>
            <option value="completed">Completed</option>
            <option value="cancelled">Cancelled</option>
            <option value="on_hold">On Hold</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Priority</label>
          <select
            value={priority}
            onChange={(e) => setPriority(e.target.value)}
            className="w-full text-black p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Priorities</option>
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Completed</label>
          <select
            value={completed}
            onChange={(e) => setCompleted(e.target.value)}
            className="w-full text-black p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All</option>
            <option value="true">Yes</option>
            <option value="false">No</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Due Date Start</label>
          <input
            type="date"
            value={dueDateStart}
            onChange={(e) => setDueDateStart(e.target.value)}
            className="w-full text-black p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Due Date End</label>
          <input
            type="date"
            value={dueDateEnd}
            onChange={(e) => setDueDateEnd(e.target.value)}
            className="w-full text-black p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Tags</label>
          <input
            type="text"
            value={tags}
            onChange={(e) => setTags(e.target.value)}
            placeholder="Enter tags (comma-separated)"
            className="w-full text-black p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Has Recurrence</label>
          <select
            value={hasRecurrence}
            onChange={(e) => setHasRecurrence(e.target.value)}
            className="w-full text-black p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All</option>
            <option value="true">Yes</option>
            <option value="false">No</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Search</label>
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search tasks..."
            className="w-full text-black p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      <div className="flex flex-col sm:flex-row sm:space-x-2 space-y-2 sm:space-y-0 mt-4">
        <button
          onClick={handleApplyFilters}
          className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 flex-1"
        >
          Apply Filters
        </button>
        <button
          onClick={handleClearFilters}
          className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 flex-1"
        >
          Clear Filters
        </button>
      </div>
    </div>
  );
};

export default TaskFilterComponent;