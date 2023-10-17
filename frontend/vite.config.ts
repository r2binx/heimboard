import vue from "@vitejs/plugin-vue";
import { fileURLToPath, URL } from "node:url";
import { defineConfig } from "vite";
import Components from "unplugin-vue-components/vite";
import { NaiveUiResolver } from "unplugin-vue-components/resolvers";
import Checker from "vite-plugin-checker";
import VueDevTools from "vite-plugin-vue-devtools";
import Inspect from "vite-plugin-inspect";
import { VitePWA } from "vite-plugin-pwa";

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [
        VueDevTools(),
        vue(),
        VitePWA({
            base: "/",
            registerType: "prompt",
            srcDir: "src",
            includeAssets: [
                "favicon.svg",
                "favicon.ico",
                "robots.txt",
                "apple-touch-icon.png",
                "fira-code-600.woff2",
            ],
            manifest: {
                name: "HEIMBOARD",
                short_name: "HEIM",
                theme_color: "#ffffff",
                description: "Dashboard for the blckct.io server",
                display: "standalone",
                start_url: "/",
                icons: [
                    {
                        src: "pwa-192x192.png",
                        sizes: "192x192",
                        type: "image/png",
                    },
                    {
                        src: "pwa-512x512.png",
                        sizes: "512x512",
                        type: "image/png",
                    },
                    {
                        src: "pwa-512x512.png",
                        sizes: "512x512",
                        type: "image/png",
                        purpose: "any maskable",
                    },
                ],
            },
        }),
        Components({
            dts: true,
            resolvers: [NaiveUiResolver()],
        }),
        Inspect(),
        Checker({
            vueTsc: true,
        }),
    ],
    build: {
        sourcemap: true,
        minify: true,
        emptyOutDir: true,
        manifest: true,
        rollupOptions: {
            output: {
                manualChunks: {
                    axios: ["axios"],
                },
            },
        },
    },
    optimizeDeps: {
        entries: ["./src/main.ts"],
        include: ["vue", "@vueuse/core", "axios", "naive-ui"],
    },
    resolve: {
        alias: {
            "@": fileURLToPath(new URL("./src", import.meta.url)),
        },
    },
});
