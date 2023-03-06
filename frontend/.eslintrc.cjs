/* eslint-env node */
require("@rushstack/eslint-patch/modern-module-resolution");
const tsParser = require("@typescript-eslint/parser");

module.exports = {
    root: true,
    extends: [
        "plugin:vue/vue3-recommended",
        "eslint:recommended",
        "@vue/eslint-config-typescript",
        "@vue/eslint-config-prettier",
    ],
    parser: "vue-eslint-parser",
    parserOptions: {
        ecmaVersion: "latest",
        parser: {
            ts: tsParser,
        },
    },
};
