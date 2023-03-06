<script setup lang="ts">
import { useAuth0 as auth0VueClient } from "@auth0/auth0-vue";
import ProgressCircle from "@/components/ProgressCircle.vue";
import { useWindowWidth } from "@/composables/useWindowWidth";
import { useWebSocket } from "@vueuse/core";
import { NDivider, NSpace } from "naive-ui";
import { computed, ref } from "vue";
import useApi from "@/composables/useApi";
import useAuth0 from "@/composables/useAuth0";

const { getAccessToken } = useAuth0(auth0VueClient());
const { useApiState } = useApi();
const state = useApiState();

const { windowWidth } = useWindowWidth();

type Usage = Record<"in" | "out", { value: number; pct: number }>;

let bandwidth = computed(() => {
    let fritz = state.fritz.value;
    if (!fritz) return { in: 0, out: 0 };

    return { in: ~~(fritz.net.down / 1e6), out: ~~(fritz.net.up / 1e6) };
});

const rateInPct = (rate: number, type: "in" | "out") => {
    return (rate / bandwidth.value[type]) * 100;
};

const usage = ref<Usage>({ in: { value: 0, pct: 0 }, out: { value: 0, pct: 0 } });

getAccessToken().then((token) => {
    useWebSocket(
        "wss://" + import.meta.env.VITE_APP_IDLEREPORTER + "/net?rate=1&token=" + token,
        {
            autoReconnect: true,
            onConnected: () =>
                console.log("Successfully connected to the fritz websocket server..."),
            onMessage: (ws, event) => {
                let data = JSON.parse(event.data);
                for (let type of Object.keys(data) as ("in" | "out")[]) {
                    const mbits = ~~(data[type] / 125000);
                    usage.value[type].value = mbits;
                    usage.value[type].pct = rateInPct(mbits, type);
                }
            },
        }
    );
});
</script>

<template>
    <n-divider title-placement="left">Network</n-divider>
    <n-space justify="space-around">
        <progress-circle
            v-for="(bw, key) in usage"
            :key="key"
            :percentage="bw.pct"
            :title="key"
        >
            <div :style="{ fontSize: windowWidth <= 420 ? 'medium' : 'large' }">
                {{ bw.value }}<span style="font-size: small">Mbit/s</span>
            </div>
        </progress-circle>
    </n-space>
</template>
