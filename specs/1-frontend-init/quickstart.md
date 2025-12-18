# Quickstart: Frontend Development

## Prerequisites

- Node.js 18+ installed
- npm or yarn package manager

## Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser to see the result.

## Development Commands

- `npm run dev` - Start development server with hot reloading
- `npm run build` - Build the application for production
- `npm run start` - Start the production server
- `npm run lint` - Run ESLint to check for code issues

## Project Structure

- `app/` - Next.js 16+ App Router pages and layouts
- `components/` - Reusable React components
- `lib/` - Utility functions and shared code
- `public/` - Static assets
- `styles/` - Global styles (if needed beyond Tailwind)

## Next Steps

After initialization, you can:
- Create new pages in the `app/` directory following App Router conventions
- Add components to the `components/` directory
- Configure additional Tailwind CSS settings in `tailwind.config.ts`
- Set up API routes for backend communication