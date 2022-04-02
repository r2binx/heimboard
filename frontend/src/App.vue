<script setup>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup
import RefreshOutlined from "@/assets/RefreshOutlined.svg"
import { onBeforeUnmount, onMounted, onUnmounted, provide, watch } from "vue"
// import doesn't work with vite dev server
// import { $ref } from 'vue/macros'
import {
	darkTheme,
	NButton,
	NCard,
	NConfigProvider,
	NGlobalStyle,
	NIcon,
	NSpace,
	NSpin,
	useOsTheme,
} from "naive-ui"
import Panel from "@/components/Panel.vue"
import { Auth } from "@/utils/useAuth0.js"
import { State } from "@/utils/api.js"
import { registerSW } from "virtual:pwa-register"

let windowWidth = $ref(window.innerWidth)
const onWidthChange = () => (windowWidth = window.innerWidth)
onMounted(() => window.addEventListener("resize", onWidthChange))
onUnmounted(() => window.removeEventListener("resize", onWidthChange))
provide("windowWidth", $$(windowWidth))

const osThemeRef = $(useOsTheme())
let theme = $ref(osThemeRef === "dark" ? darkTheme : null)
let activeShade = $ref(osThemeRef === "dark" ? "#63e2b7" : "#18a058")
let idleShade = $ref(osThemeRef === "dark" ? "#e88080" : "#d03050")

let fontColor = $ref(osThemeRef === "dark" ? "#e8e8e8" : "#1f2225")
provide("fontColor", fontColor)

const auth = new Auth()
provide("auth", auth)

const state = new State()
provide("state", state)

watch(
	() => auth.isAuthenticated.value,
	() => state.refreshState()
)

const keepAlive = () => {
	if (document.hasFocus() && auth.isAuthenticated.value) {
		state.refreshState()
	}
}

const intervalFocusHandler = setInterval(keepAlive, 30000)

onBeforeUnmount(() => clearInterval(intervalFocusHandler))

onMounted(async () => {
	registerSW({
		immediate: true,
		onNeedRefresh: () => console.log("The PWA will update automagically"),
	})
})

function changeTheme(newTheme) {
	theme = newTheme
	activeShade = newTheme === darkTheme ? "#63e2b7" : "#18a058"
	idleShade = newTheme === darkTheme ? "#e88080" : "#d03050"
	fontColor = newTheme === darkTheme ? "#e8e8e8" : "#1f2225"
}
</script>

<template>
	<n-config-provider class="container" :theme="theme">
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
						v-if="auth.isAuthenticated.value"
						id="refresh-button"
						:loading="state.refreshing"
						style="margin-right: 10px"
						size="large"
						circle
						@click="state.refreshState()"
					>
						<template #icon>
							<n-icon>
								<RefreshOutlined />
							</n-icon>
						</template>
					</n-button>
					<n-button
						v-if="theme == null || theme === 'light'"
						class="theme-toggle"
						size="large"
						circle
						@click="changeTheme(darkTheme)"
						>🌚
					</n-button>
					<n-button
						v-else
						class="theme-toggle"
						size="large"
						circle
						@click="changeTheme(null)"
						>🌞
					</n-button>
				</template>
				<div v-if="!auth.loading.value">
					<Panel v-if="auth.isAuthenticated.value" />
					<div v-else>
						<n-button size="large" type="primary" @click="auth.login()">Login</n-button>
					</div>
				</div>
				<n-space v-else vertical justify="center">
					<n-spin size="large" />
					<p>Loading...</p>
				</n-space>
				<template v-if="auth.isAuthenticated.value" #action>
					<n-button size="small" style="float: right" @click="auth.logout()"
						>Logout
					</n-button>
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
		align-items: center;
		justify-content: center;
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
	src: local(""), url("@/assets/fira-code-600.woff2") format("woff2");
}
</style>
