/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  
  // Environment variables
  env: {
    NEXT_PUBLIC_FLASK_URL: process.env.NEXT_PUBLIC_FLASK_URL || 'http://localhost:8084',
  },

  // API proxy configuration for development
  async rewrites() {
    return [
      {
        source: '/api/v0/:path*',
        destination: `${process.env.NEXT_PUBLIC_FLASK_URL || 'http://localhost:8084'}/api/v0/:path*`,
      },
    ];
  },

  // Build configuration
  output: 'standalone',
  
  // Webpack configuration for Plotly
  webpack: (config, { isServer }) => {
    if (!isServer) {
      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false,
        net: false,
        tls: false,
      };
    }
    return config;
  },
};

module.exports = nextConfig;
