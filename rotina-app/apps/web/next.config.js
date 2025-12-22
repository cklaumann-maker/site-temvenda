/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  transpilePackages: ['@rotina/shared', '@rotina/ui'],
  experimental: {
    serverActions: true,
  },
};

module.exports = nextConfig;

