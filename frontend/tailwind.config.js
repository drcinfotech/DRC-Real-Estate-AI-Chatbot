/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      fontFamily: {
        serif: ['"Instrument Serif"', "serif"],
        sans:  ["Geist", "system-ui", "sans-serif"],
        mono:  ['"JetBrains Mono"', "monospace"],
      },
      colors: {
        accent: { DEFAULT: "#34D399", dim: "#34D39922" },
      },
      animation: {
        "fade-up":    "fadeUp 0.35s ease-out both",
        "pulse-ring": "pulseRing 2s infinite",
      },
      keyframes: {
        fadeUp:    { from: { opacity: 0, transform: "translateY(6px)" }, to: { opacity: 1, transform: "translateY(0)" } },
        pulseRing: {
          "0%":   { boxShadow: "0 0 0 0 rgba(52,211,153,0.4)" },
          "70%":  { boxShadow: "0 0 0 10px rgba(52,211,153,0)" },
          "100%": { boxShadow: "0 0 0 0 rgba(52,211,153,0)" },
        },
      },
    },
  },
  plugins: [],
};
