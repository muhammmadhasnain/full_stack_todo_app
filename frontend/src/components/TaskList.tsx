'use client';

import React, { useState, useEffect } from 'react';
import { useTask } from '@/contexts/task';
import { useAuth } from '@/contexts/auth';
import { useToast } from '@/contexts/toast';
import { Task, TaskFilter } from '@/types/task';
import TaskFilterComponent from '@/components/TaskFilterComponent';
import Pagination from '@/components/Pagination';
import { format } from 'date-fns';
import TaskItem from '@/components/TaskItem'; // Import the TaskItem component

const TaskList: React.FC = () => {
  const { tasks, loading, error, fetchTasks } = useTask();
  const { user } = useAuth();
  const { showToast } = useToast();
  const [filters, setFilters] = useState<TaskFilter>({});
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(10);
  const [filteredTasks, setFilteredTasks] = useState<Task[]>([]); // initial empty array

  // Apply filters and pagination whenever tasks or filters change
  useEffect(() => {
    const result = Array.isArray(tasks) ? [...tasks] : []; // safe array check

    let filtered = result;

    // Apply filters
    if (filters.status) {
      filtered = filtered.filter(task => task.status === filters.status);
    }
    if (filters.priority) {
      filtered = filtered.filter(task => task.priority === filters.priority);
    }
    if (filters.completed !== undefined && filters.completed !== null) {
      filtered = filtered.filter(task => task.completed === filters.completed);
    }
    if (filters.search) {
      const searchTerm = filters.search.toLowerCase();
      filtered = filtered.filter(task =>
        task.title.toLowerCase().includes(searchTerm) ||
        (task.description && task.description.toLowerCase().includes(searchTerm))
      );
    }
    if (filters.due_date_start) {
      const startDate = new Date(filters.due_date_start);
      filtered = filtered.filter(task => task.dueDate && new Date(task.dueDate) >= startDate);
    }
    if (filters.due_date_end) {
      const endDate = new Date(filters.due_date_end);
      filtered = filtered.filter(task => task.dueDate && new Date(task.dueDate) <= endDate);
    }

    setFilteredTasks(filtered);
    setCurrentPage(1);
  }, [tasks, filters]);

  const handleFilterChange = (newFilters: TaskFilter) => setFilters(newFilters);
  const handlePageChange = (page: number) => setCurrentPage(page);

  const totalPages = Math.ceil(filteredTasks.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const paginatedTasks = filteredTasks.slice(startIndex, startIndex + itemsPerPage);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[200px]">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    showToast(error, 'error');
  }

  return (
    <div>
      <TaskFilterComponent onFilterChange={handleFilterChange} />

      <div className="space-y-3">
        {/* Render TaskItem components for each task */}
        {paginatedTasks.length > 0 ? (
          paginatedTasks.map(task => (
            <TaskItem key={task.id} task={task} />
          ))
        ) : (
          <div className="text-center py-6 text-gray-500">
            No tasks found matching your filters.
          </div>
        )}
      </div>

      {filteredTasks.length > 0 && (
        <Pagination
          currentPage={currentPage}
          totalPages={totalPages}
          onPageChange={handlePageChange}
          totalItems={filteredTasks.length}
          itemsPerPage={itemsPerPage}
        />
      )}
    </div>
  );
};

export default TaskList;
