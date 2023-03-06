<script setup lang="ts">
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup
import RefreshOutlined from "@/components/icons/RefreshOutlined.vue";
import { useAuth0 as auth0VueClient } from "@auth0/auth0-vue";
import {
    darkTheme as naiveDarkTheme,
    NButton,
    NCard,
    NConfigProvider,
    NGlobalStyle,
    NLoadingBarProvider,
    NMessageProvider,
    NNotificationProvider,
    NSpace,
    NSpin,
    useOsTheme,
    type GlobalThemeOverrides,
} from "naive-ui";
import type { BuiltInGlobalTheme } from "naive-ui/es/themes/interface";
import { computed, defineAsyncComponent, onUnmounted, watch } from "vue";
import { $, $ref } from "vue/macros";
import ReloadPrompt from "@/components/ReloadPrompt.vue";
import useApi from "@/composables/useApi";
import useAuth0 from "./composables/useAuth0";
import { useHead } from "@vueuse/head";

const osThemeRef = $(useOsTheme());
let theme: BuiltInGlobalTheme | null = $ref(
    osThemeRef === "dark" ? naiveDarkTheme : null
);

let activeShade = $ref(osThemeRef === "dark" ? "#63e2b7" : "#18a058");
let idleShade = $ref(osThemeRef === "dark" ? "#e88080" : "#d03050");
let fontColor = $ref(osThemeRef === "dark" ? "#e8e8e8" : "#1f2225");

useHead({
    title: "HEIMBOARD",
    meta: [
        { name: "description", content: "Dashboard for the blckct.io server" },
        {
            name: "theme-color",
            content: computed(() => (osThemeRef === "dark" ? "#18181C" : "#FFFFFF")),
        },
    ],
});

const { isAuthenticated, isLoading, loginWithRedirect, logout } = auth0VueClient();

const auth0Logout = () => {
    logout({
        logoutParams: {
            returnTo: window.location.origin,
        },
    });
};

const { useApiState } = useApi();
const state = useApiState();

const { accessToken, getAccessToken } = useAuth0(auth0VueClient());

const refreshState = () => {
    if (!accessToken.value) {
        getAccessToken().then((token) => {
            state.refreshState(token);
        });
    } else {
        state.refreshState(accessToken.value);
    }
};

watch(
    () => isAuthenticated.value,
    () => refreshState()
);

const keepAlive = () => {
    if (document.hasFocus() && isAuthenticated.value) {
        refreshState();
    }
};

const intervalFocusHandler = setInterval(keepAlive, 30000);

const MainPanel = defineAsyncComponent(() => import("@/components/MainPanel.vue"));

onUnmounted(() => clearInterval(intervalFocusHandler));

const darkThemeOverrides: GlobalThemeOverrides = {};
const lightThemeOverrides: GlobalThemeOverrides = {};

function darkTheme() {
    theme = naiveDarkTheme;
    activeShade = "#63e2b7";
    idleShade = "#e88080";
    fontColor = "#e8e8e8";
}
function defaultTheme() {
    theme = null;
    activeShade = "#18a058";
    idleShade = "#d03050";
    fontColor = "#1f2225";
}
</script>

<template>
    <n-config-provider
        class="container"
        :theme="theme"
        :theme-overrides="theme === null ? lightThemeOverrides : darkThemeOverrides"
    >
        <n-message-provider>
            <n-notification-provider placement="bottom-right">
                <ReloadPrompt>
                    <div class="center">
                        <n-card
                            class="main"
                            :bordered="false"
                            title="HEIMBOARD"
                            size="huge"
                            header-style="font-size: xx-large;"
                        >
                            <template #header-extra>
                                <n-button
                                    v-if="isAuthenticated"
                                    id="refresh-button"
                                    :loading="state.refreshing.value"
                                    style="margin-right: 10px"
                                    size="large"
                                    circle
                                    @click="refreshState"
                                >
                                    <template #icon>
                                        <RefreshOutlined />
                                    </template>
                                </n-button>
                                <n-button
                                    v-if="theme == null || theme.name === 'light'"
                                    class="theme-toggle"
                                    size="large"
                                    circle
                                    @click="darkTheme"
                                    >🌚
                                </n-button>
                                <n-button
                                    v-else
                                    class="theme-toggle"
                                    size="large"
                                    circle
                                    @click="defaultTheme"
                                    >🌞
                                </n-button>
                            </template>
                            <div v-if="!isLoading">
                                <template v-if="isAuthenticated">
                                    <n-loading-bar-provider>
                                        <Suspense>
                                            <MainPanel />
                                        </Suspense>
                                    </n-loading-bar-provider>
                                </template>
                                <div v-else>
                                    <n-button
                                        size="large"
                                        type="primary"
                                        @click="loginWithRedirect()"
                                        >Login</n-button
                                    >
                                </div>
                            </div>
                            <n-space v-else vertical justify="center">
                                <n-spin size="large" />
                                <p>Loading...</p>
                            </n-space>
                            <template v-if="isAuthenticated" #action>
                                <n-button
                                    size="small"
                                    style="float: right"
                                    @click="auth0Logout()"
                                    >Logout
                                </n-button>
                            </template>
                        </n-card>
                    </div>
                    <n-global-style />
                </ReloadPrompt>
            </n-notification-provider>
        </n-message-provider>
    </n-config-provider>
</template>

<style>
.idle {
    color: v-bind(idleShade);
}
.active {
    color: v-bind(activeShade);
}

@media only screen and (min-width: 721px) {
    .container {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-top: 5ex;
        flex-direction: row;
        padding: 5rem;
    }

    .center {
        min-width: 53em;
    }
}

@media (max-width: 720px) {
    .main > .n-card-header,
    .main > .n-card__content,
    .main > .n-card__action {
        padding: 1.5ex;
    }

    #refresh-button {
        margin-right: 0px !important;
    }

    .theme-toggle {
        display: none;
    }

    .container {
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0;
        flex-direction: row;
    }

    .center {
        width: 100%;
    }
}

#app {
    font-family: "Fira Code", monospace;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
}

* {
    text-transform: uppercase;
    font-weight: 600;
}

@font-face {
    font-family: "Fira Code";
    font-style: normal;
    font-weight: 600;
    font-display: swap;
    src: local(""), url("/fira-code-600.woff2") format("woff2");
}
</style>
