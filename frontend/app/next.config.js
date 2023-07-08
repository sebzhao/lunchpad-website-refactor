/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/v1/:path*',
        destination: 'http://127.0.0.1:4000/v1/:path*'
      }
    ]
  },

  webpack: (
    config, { buildId, dev, isServer, defaultLoaders, nextRuntime, webpack }
  ) => {
    // Important: return the modified config
    config.watchOptions = {
      ignored: ['**/node_modules', '**/.next']
    }

    return config
  }
}

module.exports = nextConfig
