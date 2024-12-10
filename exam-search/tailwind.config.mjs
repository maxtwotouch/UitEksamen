/** @type {import('tailwindcss').Config} */
import daisyui from "daisyui";

export default {
  content: [
    "./index.html",
    "./src/**/*.{ts,tsx}", // ensure it scans your TS/TSX files
  ],
  theme: {
    extend: {},
  },
  plugins: [daisyui], // Add daisyui plugin here
};
