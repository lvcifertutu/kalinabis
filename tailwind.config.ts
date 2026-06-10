import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        'serif-display': ['EB Garamond', 'Georgia', 'serif'],
        'serif-body': ['Crimson Text', 'Georgia', 'serif'],
      },
      colors: {
        'black-deep': '#0A0E27',
        'lilith-primary': '#CC0000',
        'lilith-secondary': '#4B0082',
        'lilith-accent': '#FF1493',
        'artemisa-primary': '#E8E8E8',
        'artemisa-secondary': '#87CEEB',
        'afrodita-primary': '#FFD700',
        'afrodita-secondary': '#FF69B4',
        'isis-primary': '#00CED1',
        'isis-secondary': '#FFD700',
      },
    },
  },
  plugins: [],
}
export default config
