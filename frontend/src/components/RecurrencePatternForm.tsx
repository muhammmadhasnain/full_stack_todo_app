'use client';

import React, { useState } from 'react';
import { RecurrencePattern } from '@/types/task';

interface RecurrencePatternFormProps {
  recurrencePattern: RecurrencePattern | undefined;
  onPatternChange: (pattern: RecurrencePattern | undefined) => void;
}

const RecurrencePatternForm: React.FC<RecurrencePatternFormProps> = ({
  recurrencePattern,
  onPatternChange
}) => {
  const [isOpen, setIsOpen] = useState(!!recurrencePattern);
  const [type, setType] = useState<'daily' | 'weekly' | 'monthly' | 'yearly'>(recurrencePattern?.type || 'daily');
  const [interval, setInterval] = useState<number>(recurrencePattern?.interval || 1);
  const [endDate, setEndDate] = useState<string>(recurrencePattern?.end_date || '');
  const [occurrences, setOccurrences] = useState<number | undefined>(recurrencePattern?.occurrences);
  const [daysOfWeek, setDaysOfWeek] = useState<number[]>(recurrencePattern?.days_of_week || []);
  const [daysOfMonth, setDaysOfMonth] = useState<number[]>(recurrencePattern?.days_of_month || []);

  const handleToggle = () => {
    if (isOpen) {
      // Clear the pattern
      onPatternChange(undefined);
    } else {
      // Initialize with default values
      onPatternChange({
        type: 'daily',
        interval: 1,
      });
    }
    setIsOpen(!isOpen);
  };

  const handleTypeChange = (newType: 'daily' | 'weekly' | 'monthly' | 'yearly') => {
    setType(newType);
    updatePattern({ type: newType });
  };

  const updatePattern = (updates: Partial<RecurrencePattern>) => {
    const newPattern: RecurrencePattern = {
      type,
      interval,
      end_date: endDate || undefined,
      occurrences: occurrences || undefined,
      days_of_week: daysOfWeek.length > 0 ? daysOfWeek : undefined,
      days_of_month: daysOfMonth.length > 0 ? daysOfMonth : undefined,
      ...updates,
    };
    onPatternChange(newPattern);
  };

  const handleDaysOfWeekToggle = (day: number) => {
    const newDays = daysOfWeek.includes(day)
      ? daysOfWeek.filter(d => d !== day)
      : [...daysOfWeek, day];

    setDaysOfWeek(newDays);
    updatePattern({ days_of_week: newDays.length > 0 ? newDays : undefined });
  };

  const handleDaysOfMonthToggle = (day: number) => {
    const newDays = daysOfMonth.includes(day)
      ? daysOfMonth.filter(d => d !== day)
      : [...daysOfMonth, day];

    setDaysOfMonth(newDays);
    updatePattern({ days_of_month: newDays.length > 0 ? newDays : undefined });
  };

  const weekDays = [
    { name: 'Sun', value: 0 },
    { name: 'Mon', value: 1 },
    { name: 'Tue', value: 2 },
    { name: 'Wed', value: 3 },
    { name: 'Thu', value: 4 },
    { name: 'Fri', value: 5 },
    { name: 'Sat', value: 6 },
  ];

  const monthDays = Array.from({ length: 31 }, (_, i) => i + 1);

  return (
    <div className="border rounded-lg p-4 bg-gray-50">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-medium text-gray-800">Recurrence Pattern</h3>
        <label className="relative inline-flex items-center cursor-pointer">
          <input
            type="checkbox"
            checked={isOpen}
            onChange={handleToggle}
            className="sr-only peer"
          />
          <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
        </label>
      </div>

      {isOpen && (
        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Pattern Type</label>
              <select
                value={type}
                onChange={(e) => handleTypeChange(e.target.value as any)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="daily">Daily</option>
                <option value="weekly">Weekly</option>
                <option value="monthly">Monthly</option>
                <option value="yearly">Yearly</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Interval</label>
              <input
                type="number"
                min="1"
                value={interval}
                onChange={(e) => {
                  const val = parseInt(e.target.value);
                  setInterval(val);
                  updatePattern({ interval: val });
                }}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>

          {(type === 'weekly' || type === 'monthly') && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                {type === 'weekly' ? 'Days of Week' : 'Days of Month'}
              </label>
              <div className="flex flex-wrap gap-2">
                {type === 'weekly'
                  ? weekDays.map(day => (
                      <button
                        key={day.value}
                        type="button"
                        onClick={() => handleDaysOfWeekToggle(day.value)}
                        className={`px-3 py-1 rounded-md text-sm ${
                          daysOfWeek.includes(day.value)
                            ? 'bg-blue-500 text-white'
                            : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                        }`}
                      >
                        {day.name}
                      </button>
                    ))
                  : monthDays.map(day => (
                      <button
                        key={day}
                        type="button"
                        onClick={() => handleDaysOfMonthToggle(day)}
                        className={`px-2 py-1 rounded-md text-sm ${
                          daysOfMonth.includes(day)
                            ? 'bg-blue-500 text-white'
                            : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                        }`}
                      >
                        {day}
                      </button>
                    ))}
              </div>
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">End Date (optional)</label>
              <input
                type="date"
                value={endDate}
                onChange={(e) => {
                  setEndDate(e.target.value);
                  updatePattern({ end_date: e.target.value || undefined });
                }}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Number of Occurrences (optional)</label>
              <input
                type="number"
                min="1"
                value={occurrences || ''}
                onChange={(e) => {
                  const val = e.target.value ? parseInt(e.target.value) : undefined;
                  setOccurrences(val);
                  updatePattern({ occurrences: val || undefined });
                }}
                placeholder="Leave empty for no limit"
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default RecurrencePatternForm;