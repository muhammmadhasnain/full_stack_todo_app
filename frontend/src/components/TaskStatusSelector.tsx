'use client';

import React from 'react';

interface TaskStatusSelectorProps {
  currentStatus: string;
  onStatusChange: (status: string) => void;
  disabled?: boolean;
}

const TaskStatusSelector: React.FC<TaskStatusSelectorProps> = ({
  currentStatus,
  onStatusChange,
  disabled = false
}) => {
  const statusOptions = [
    { value: 'pending', label: 'Pending', color: 'bg-yellow-100 text-yellow-800' },
    { value: 'in-progress', label: 'In Progress', color: 'bg-blue-100 text-blue-800' },
    { value: 'completed', label: 'Completed', color: 'bg-green-100 text-green-800' },
    { value: 'cancelled', label: 'Cancelled', color: 'bg-red-100 text-red-800' },
    { value: 'on_hold', label: 'On Hold', color: 'bg-gray-100 text-gray-800' },
  ];

  const currentStatusOption = statusOptions.find(option => option.value === currentStatus) || statusOptions[0];

  return (
    <select
      value={currentStatus}
      onChange={(e) => onStatusChange(e.target.value)}
      disabled={disabled}
      className={`px-3 py-1 rounded-full text-sm font-medium ${currentStatusOption.color} ${disabled ? 'opacity-50 cursor-not-allowed' : 'hover:opacity-90 cursor-pointer'}`}
    >
      {statusOptions.map((option) => (
        <option key={option.value} value={option.value}>
          {option.label}
        </option>
      ))}
    </select>
  );
};

export default TaskStatusSelector;