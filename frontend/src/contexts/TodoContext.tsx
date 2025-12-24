// frontend/src/contexts/TodoContext.tsx

'use client';

import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { Todo, CreateTodoData, UpdateTodoData, TodoFilters } from '@/types/todo';
import { todoService } from '@/lib/api';

type TodoState = {
  todos: Todo[];
  loading: boolean;
  error: string | null;
  filters: TodoFilters;
};

type TodoAction =
  | { type: 'FETCH_TODOS_START' }
  | { type: 'FETCH_TODOS_SUCCESS'; payload: Todo[] }
  | { type: 'FETCH_TODOS_ERROR'; payload: string }
  | { type: 'ADD_TODO'; payload: Todo }
  | { type: 'UPDATE_TODO'; payload: Todo }
  | { type: 'DELETE_TODO'; payload: string }
  | { type: 'TOGGLE_TODO'; payload: Todo }
  | { type: 'SET_FILTERS'; payload: TodoFilters };

const initialState: TodoState = {
  todos: [],
  loading: false,
  error: null,
  filters: { status: 'all' },
};

const TodoContext = createContext<{
  state: TodoState;
  addTodo: (data: CreateTodoData) => Promise<void>;
  updateTodo: (id: string, data: UpdateTodoData) => Promise<void>;
  deleteTodo: (id: string) => Promise<void>;
  toggleTodo: (id: string) => Promise<void>;
  setFilters: (filters: TodoFilters) => void;
  loadTodos: () => Promise<void>;
} | undefined>(undefined);

const todoReducer = (state: TodoState, action: TodoAction): TodoState => {
  switch (action.type) {
    case 'FETCH_TODOS_START':
      return { ...state, loading: true, error: null };
    case 'FETCH_TODOS_SUCCESS':
      return { ...state, loading: false, todos: action.payload };
    case 'FETCH_TODOS_ERROR':
      return { ...state, loading: false, error: action.payload };
    case 'ADD_TODO':
      return { ...state, todos: [action.payload, ...state.todos] };
    case 'UPDATE_TODO':
      return {
        ...state,
        todos: state.todos.map(todo =>
          todo.id === action.payload.id ? action.payload : todo
        ),
      };
    case 'DELETE_TODO':
      return {
        ...state,
        todos: state.todos.filter(todo => todo.id !== action.payload),
      };
    case 'TOGGLE_TODO':
      return {
        ...state,
        todos: state.todos.map(todo =>
          todo.id === action.payload.id ? action.payload : todo
        ),
      };
    case 'SET_FILTERS':
      return { ...state, filters: action.payload };
    default:
      return state;
  }
};

export const TodoProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(todoReducer, initialState);

  const loadTodos = async () => {
    try {
      dispatch({ type: 'FETCH_TODOS_START' });
      const todos = await todoService.getTodos(state.filters);
      dispatch({ type: 'FETCH_TODOS_SUCCESS', payload: todos });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to load todos';
      dispatch({ type: 'FETCH_TODOS_ERROR', payload: errorMessage });
    }
  };

  const addTodo = async (data: CreateTodoData) => {
    try {
      const newTodo = await todoService.createTodo(data);
      dispatch({ type: 'ADD_TODO', payload: newTodo });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to add todo';
      dispatch({ type: 'FETCH_TODOS_ERROR', payload: errorMessage });
    }
  };

  const updateTodo = async (id: string, data: UpdateTodoData) => {
    try {
      const updatedTodo = await todoService.updateTodo(id, data);
      dispatch({ type: 'UPDATE_TODO', payload: updatedTodo });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to update todo';
      dispatch({ type: 'FETCH_TODOS_ERROR', payload: errorMessage });
    }
  };

  const deleteTodo = async (id: string) => {
    try {
      await todoService.deleteTodo(id);
      dispatch({ type: 'DELETE_TODO', payload: id });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to delete todo';
      dispatch({ type: 'FETCH_TODOS_ERROR', payload: errorMessage });
    }
  };

  const toggleTodo = async (id: string) => {
    try {
      const toggledTodo = await todoService.toggleTodoCompletion(id);
      dispatch({ type: 'TOGGLE_TODO', payload: toggledTodo });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to toggle todo';
      dispatch({ type: 'FETCH_TODOS_ERROR', payload: errorMessage });
    }
  };

  const setFilters = (filters: TodoFilters) => {
    dispatch({ type: 'SET_FILTERS', payload: filters });
  };

  useEffect(() => {
    loadTodos();
  }, [state.filters]);

  return (
    <TodoContext.Provider
      value={{
        state,
        addTodo,
        updateTodo,
        deleteTodo,
        toggleTodo,
        setFilters,
        loadTodos,
      }}
    >
      {children}
    </TodoContext.Provider>
  );
};

export const useTodo = () => {
  const context = useContext(TodoContext);
  if (context === undefined) {
    throw new Error('useTodo must be used within a TodoProvider');
  }
  return context;
};