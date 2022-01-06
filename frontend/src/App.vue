<script setup>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup
import RefreshOutlined from "./assets/RefreshOutlined.svg"
import { provide, ref, watch } from "vue";
import {
  NConfigProvider,
  useOsTheme,
  darkTheme,
  NButton,
  NCard,
  NGlobalStyle,
  NSpin,
  NSpace,
  NIcon,
} from "naive-ui";
import Panel from "./components/Panel.vue";
import { Auth } from "./utils/useAuth0.js";
import { State } from "./utils/api";

const auth = new Auth();
provide("auth", auth);

const state = new State();
provide("state", state);

watch(() => auth.isAuthenticated.value, () => {
  state.refreshState();
});

const osThemeRef = useOsTheme();
const theme = ref(osThemeRef.value === "dark" ? darkTheme : null);
const activeShade = ref(osThemeRef.value === "dark" ? "#63e2b7" : "#18a058");
const idleShade = ref(osThemeRef.value === "dark" ? "#e88080" : "#d03050");
const fontColor = ref(osThemeRef.value === "dark" ? "#e8e8e8" : "#1f2225");

function changeTheme(newTheme) {
  theme.value = newTheme;
  activeShade.value = newTheme === darkTheme ? "#63e2b7" : "#18a058";
  idleShade.value = newTheme === darkTheme ? "#e88080" : "#d03050";
  fontColor.value = newTheme === darkTheme ? "#e8e8e8" : "#1f2225";
}

</script>

<template>
  <n-config-provider class="container" :theme="theme">
    <div class="center">
      <n-card :bordered="false" title="HEIMBOARD" size="huge" header-style="font-size: xx-large;">
        <template #header-extra>
          <n-button
            id="refresh-button"
            style="margin-right: 10px"
            size="large"
            circle
            v-if="auth.isAuthenticated.value"
            @click="state.refreshState()"
          >
            <template #icon>
              <n-icon>
                <RefreshOutlined />
              </n-icon>
            </template>
          </n-button>
          <n-button
            class="theme-toggle"
            size="large"
            circle
            v-if="theme == null || theme == 'light'"
            @click="changeTheme(darkTheme)"
          >🌚</n-button>
          <n-button class="theme-toggle" size="large" circle v-else @click="changeTheme(null)">🌞</n-button>
        </template>

        <div v-if="!auth.loading.value">
          <Panel v-if="auth.isAuthenticated.value" />
          <div v-else>
            <n-button size="large" type="primary" @click="auth.login()">Login</n-button>
          </div>
        </div>
        <n-space vertical justify="center" v-else>
          <n-spin size="large" />
          <p>Loading...</p>
        </n-space>
        <template v-if="auth.isAuthenticated.value" #action>
          <n-button size="small" style="float: right" @click="auth.logout()">Logout</n-button>
        </template>
      </n-card>
    </div>
    <n-global-style />
  </n-config-provider>
</template>

<style>
n-icon {
  fill: v-bind(fontColor);
}

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
    align-items: center;
    justify-content: center;
    width: 800px;
    min-width: 30%;
    max-width: 60%;
  }
}

@media (max-width: 720px) {
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
    margin-top: 2ex;
    flex-direction: row;
  }

  .center {
    align-items: center;
    justify-content: center;
    width: 90%;
  }
}

#app {
  /* font-family: Avenir, Helvetica, Arial, sans-serif; */
  font-family: "Fira Code", monospace;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
}
* {
  text-transform: uppercase;
  font-weight: 600;
}
</style>
