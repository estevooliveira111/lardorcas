/** @type {import('tailwindcss').Config} */

export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
    "./node_modules/flowbite/**/*.js"
  ],
  plugins: [require("@tailwindcss/typography"), require('flowbite/plugin'), require('tailwindcss-primeui')],
  darkTheme: false,
  darkMode: "false",
  themeRoot: ":root",

  theme: {
    extend: {
      colors: {
        primary: '#0baab2',
        secundary: '#07569E'
      },
    },
  },
}
