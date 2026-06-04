/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        axon: {
          dark: '#0B1319',      // Base background
          panel: 'rgba(20, 30, 40, 0.6)', // Glassmorphism panels
          neon: '#00FF88',      // Neon green
          blue: '#00BFFF',      // Neon blue
          alert: '#FF3366',     // Red for danger
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['Orbitron', 'monospace'],
      }
    },
  },
  plugins: [],
}
