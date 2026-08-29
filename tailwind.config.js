/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Plus Jakarta Sans"', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      colors: {
        flop: {
          cyan: '#02b5d6',   /* from flop.jpeg */
          dark: '#000000',   /* true black from flop.jpeg */
          card: '#0a0a0a',   /* very dark gray for cards */
          border: '#1a1a1a'  /* slightly lighter border */
        },
        floplight: {
          cyan: '#02b5d6',
          bg: '#ffffff',
          card: '#f4f4f5',
          border: '#e4e4e7'
        }
      }
    }
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}
