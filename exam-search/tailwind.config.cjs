/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{ts,tsx}", // ensure it scans your TS/TSX files
  ],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")], // Add daisyui plugin here
}
