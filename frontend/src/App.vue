<script setup>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup
import { ref } from "vue";
import { NConfigProvider, NMessageProvider, useOsTheme, darkTheme, NButton, NCard, NGlobalStyle, NIcon, NLoadingBarProvider } from "naive-ui";
import { PowerOff } from "@vicons/fa";
import Status from "./components/Status.vue";
import Usage from "./components/Usage.vue";
import Services from "./components/Services.vue";
import KVM from "./components/KVM.vue";
import { fetchUptime, wakeOnLan, state } from "./utils/api.js";
import { useAuth0, AuthState } from "./utils/useAuth0";
const { login, logout, initAuth } = useAuth0(AuthState);

initAuth();

const osThemeRef = useOsTheme();
const theme = ref(osThemeRef.value === 'dark' ? darkTheme : null);
const activeShade = ref(osThemeRef.value === 'dark' ? "#63e2b7" : "#18a058");
const idleShade = ref(osThemeRef.value === 'dark' ? "#e88080" : "#d03050");

fetchUptime().then(res => {
  if (res.status == 200) {
    state.uptime = res.data;
    state.reachable = true;
  } else {
    state.reachable = false;
  }
}).catch(err => {
  state.reachable = false;
  console.log(err);
});

function handleWakeUp() {
  wakeOnLan().then(res => {
    if (res.data.success) {
      console.success("Woke up!");
    } else {
      console.error(res.data.message);
    }
  }).catch(
    err => {
      console.error("Failed to wake up!");
      console.log(err);
    }
  );
}

function changeTheme(newTheme) {
  theme.value = newTheme;
  activeShade.value = newTheme === darkTheme ? "#63e2b7" : "#18a058";
  idleShade.value = newTheme === darkTheme ? "#e88080" : "#d03050";
}

</script>

<template>
  <n-config-provider class="container" :theme="theme">
    <div class="center">
      <n-card :bordered="false" title="HEIMBOARD" size="huge" header-style="font-size: xx-large;">
        <template #header-extra>
          <n-button
            class="theme-toggle"
            size="large"
            circle
            v-if="theme == null || theme == 'light'"
            @click="changeTheme(darkTheme)"
          >🌚</n-button>
          <n-button class="theme-toggle" size="large" circle v-else @click="changeTheme(null)">🌞</n-button>
        </template>
        <div v-if="!AuthState.loading">
          <div v-if="!AuthState.isAuthenticated">
            <n-button size="large" type="primary" @click="login()">LOGIN</n-button>
          </div>

          <div v-else>
            <div v-if="state.reachable">
              <n-message-provider>
                <Status />
              </n-message-provider>
              <Usage />
              <Services />
              <n-message-provider v-if="AuthState.user.email == 'robin@blckct.io'">
                <n-loading-bar-provider>
                  <KVM />
                </n-loading-bar-provider>
              </n-message-provider>
            </div>
            <div v-else>
              <n-button @click="handleWakeUp" style="font-size: 72px;" circle :bordered="false">
                <n-icon>
                  <PowerOff />
                </n-icon>
              </n-button>
              <p style="font-size: large;">WAKE UP</p>
            </div>
          </div>
        </div>

        <div v-else>Loading ...</div>
        <template v-if="AuthState.isAuthenticated" #action>
          <n-button size="small" style="float: right;" @click="logout()">LOGOUT</n-button>
        </template>
      </n-card>
    </div>
    <n-global-style />
  </n-config-provider>
</template>

<style>
.theme-toggle {
  position: absolute;
  top: 8px;
  right: 16px;
}

.idle {
  color: v-bind(idleShade);
}

.active {
  color: v-bind(activeShade);
}

@media only screen and (min-width: 593px) {
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

@media (max-width: 592px) {
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
  font-weight: 600;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
}
</style>