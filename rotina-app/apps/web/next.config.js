/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  transpilePackages: ['@rotina/shared', '@rotina/ui'],
  output: 'standalone',
  // Evitar renderização estática de rotas que usam cookies
  experimental: {
    serverActions: {
      bodySizeLimit: '2mb',
    },
  },
};

module.exports = nextConfig;

