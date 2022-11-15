/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      fontFamily: {
        pokemon: ["Pokemon Solid", "sans-serif"]
      }
    },
  },
  plugins: [],
}
