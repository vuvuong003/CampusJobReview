/** @type {import('tailwindcss').Config} */
// module.exports = {
//     content: [
//       "./src/**/*.{js,jsx,ts,tsx}",
//     ],
//     theme: {
//       extend: {
//         colors: {
//           purplegray: {
//             100: '#F1F2F7',
//             300: '#B6B1CD',
//             400: '#A4A1B8',
//             500: '#8C7ABD',
//             600: '#604E9E',
//             900: '#301896'
//           },
//           purplezinc: '#43464A'
//         }
//       },
//     },
//     plugins: [],
//   }

  module.exports = {
    purge: ['./src/**/*.{js,jsx,ts,tsx}', './public/index.html'],
    darkMode: false, // or 'media' or 'class'
    theme: {
      extend: {},
    },
    variants: {
      extend: {},
    },
    plugins: [],
  }
  
  