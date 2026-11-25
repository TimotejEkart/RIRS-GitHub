import js from "@eslint/js";
import globals from "globals";

export default [
  { ignores: ["static/js/body-muscles/**", "node_modules/**", "coverage/**"] },
  js.configs.recommended,
  {
    files: ["static/js/**/*.js"],
    languageOptions: { sourceType: "script", globals: { ...globals.browser } },
  },
  {
    files: ["tests/**/*.js"],
    languageOptions: { globals: { ...globals.browser } },
  },
];
