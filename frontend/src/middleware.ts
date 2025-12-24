import { NextRequest, NextResponse } from 'next/server';

export function middleware(request: NextRequest) {
  // Add your middleware logic here
  // For now, just allow all requests to pass through
  return NextResponse.next();
}

// Define which paths the middleware should run for
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};