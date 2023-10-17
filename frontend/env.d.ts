/// <reference types="vite/client" />
/// <reference types="vue/macros-global" />
/// <reference types="vite-plugin-pwa/vue" />
/// <reference types="vite-plugin-pwa/info" />
interface ImportMetaEnv {
    readonly VITE_APP_IDLEREPORTER: string;
    readonly VITE_APP_WAKESERVER: string;
    readonly VITE_AUTH0_DOMAIN: string;
    readonly VITE_AUTH0_CLIENT_ID: string;
    readonly VITE_AUTH0_AUDIENCE: string;
}

interface ImportMeta {
    readonly env: ImportMetaEnv;
}
