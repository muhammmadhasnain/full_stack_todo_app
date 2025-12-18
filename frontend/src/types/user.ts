// TypeScript User interface with UUID string ID and ISO datetime format
export interface User {
  id: string;  // UUID string
  email: string;
  name: string;
  createdAt: string; // ISO date string
  updatedAt: string; // ISO date string
  is_active?: boolean;
}

export interface UserProfile extends User {
  // Extended user profile properties if needed
}

export interface UserCreate {
  name: string;
  email: string;
  password: string;
}

export interface UserLogin {
  email: string;
  password: string;
}

export interface UserUpdate {
  name?: string;
  email?: string;
  password?: string;
}