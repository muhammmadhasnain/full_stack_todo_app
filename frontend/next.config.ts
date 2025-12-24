import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Remove output: 'export' for Vercel deployment to allow dynamic features
  // For static export, we would use output: 'export', but Vercel works better with dynamic apps

  // Optional: Add any specific Vercel configurations here
  // For example, if you need to connect to your backend API:
  // async rewrites() {
  //   return [
  //     {
  //       source: '/api/:path*',
  //       destination: process.env.BACKEND_URL ? `${process.env.BACKEND_URL}/:path*` : 'http://localhost:8000/:path*',
  //     },
  //   ]
  // },
};

export default nextConfig;












// import type { NextConfig } from "next";

// const nextConfig: NextConfig = {
//   /* config options here */
//   output: 'export',
// };

// export default nextConfig;
