import { createApp } from "vue";
import App from "./App.vue";
import createAuth0 from "@/utils/auth0";
import { createHead } from "@vueuse/head";

const head = createHead();

createApp(App).use(createAuth0).use(head).mount("#app");
