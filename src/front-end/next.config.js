const { PHASE_DEVELOPMENT_SERVER } = require('next/constants')

module.exports = async (phase, { defaultConfig }) => {
  /**
   * @type {import('next').NextConfig}
   */

  if (phase === PHASE_DEVELOPMENT_SERVER) return {}

  const nextConfig = {
    reactStrictMode: true,
    output: 'export',
    distDir: '../html',
  }

  return nextConfig
}
