// Docs: https://tailwindcss.com/docs/configuration

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    'src/web/templates/**/*.html',
    'src/templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        'very-light-yellow-green': '#e8e8e7',
        'cyan-shade': '#61b0b2',
        'green-cyan-shade': '#79b18d',
        'green-shade': '#92b268',
        'yellow-green-shade': '#abb444',
      }
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('@tailwindcss/forms'),
    require('@tailwindcss/aspect-ratio'),
    require('@tailwindcss/container-queries'),
  ],
}
