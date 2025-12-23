import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'export',

  // Remove manual webpack alias as Next.js handles @/* paths automatically
  // when configured in tsconfig.json
  // webpack: (config) => {
  //   config.resolve.alias['@'] = path.resolve(__dirname, 'src');
  //   return config;
  // },

  turbopack: {}, // Ye line add karo, empty object Turbopack ko satisfy karega
};

export default nextConfig;












// import type { NextConfig } from "next";

// const nextConfig: NextConfig = {
//   /* config options here */
//   output: 'export',
// };

// export default nextConfig;
