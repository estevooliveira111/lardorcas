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
      backgroundImage: {
        'custom-image': "url('https://static.wixstatic.com/media/d43a50_46caa963d7274e8e8efcf5b9ca74f0cc~mv2.png/v1/fill/w_920,h_749,al_c,q_90,enc_avif,quality_auto/d43a50_46caa963d7274e8e8efcf5b9ca74f0cc~mv2.png')",
      }
    }
  }
}
