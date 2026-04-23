/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  basePath: '/aida-venture-os',
  trailingSlash: true,
  images: {
    unoptimized: true,
  },
  experimental: {
    typedRoutes: false,
  },
}

module.exports = nextConfig
