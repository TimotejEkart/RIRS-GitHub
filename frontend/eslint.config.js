import js from "@eslint/js";
import globals from "globals";

export default [
  { ignores: ["static/js/body-muscles/**", "node_modules/**"] },
  js.configs.recommended,
  {
    files: ["static/js/**/*.js"],
    languageOptions: {
      sourceType: "script",
      globals: { ...globals.browser },
    },
  },
];
