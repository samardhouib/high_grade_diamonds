/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  images: {
    domains: ['localhost', 'backend'],
    unoptimized: process.env.NODE_ENV === 'development',
  },
  experimental: {
    // Enable standalone mode for Docker
    outputFileTracingRoot: undefined,
  },
}

module.exports = nextConfig
