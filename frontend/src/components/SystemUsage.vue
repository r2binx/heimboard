<script setup lang="ts">
import ProgressCircle from "@/components/ProgressCircle.vue";
import { useWebSocket } from "@vueuse/core";
import { NDivider, NSpace } from "naive-ui";
import { ref } from "vue";
import useAuth0 from "@/composables/useAuth0";

const { getAccessToken } = useAuth0();
const usage = ref<Record<"cpu" | "memory", number>>({ cpu: 0, memory: 0 });

getAccessToken().then((token) => {
    useWebSocket(
        "wss://" + import.meta.env.VITE_APP_IDLEREPORTER + "/usage?rate=1&token=" + token,
        {
            autoReconnect: true,
            onConnected: () =>
                console.log("Successfully connected to the system websocket server..."),
            onMessage: (ws, event) => {
                let data = JSON.parse(event.data);
                usage.value.cpu = data["cpu"];
                usage.value.memory = data["memory"]["used"];
            },
        }
    );
});
</script>

<template>
    <n-divider title-placement="left">SYSTEM</n-divider>
    <n-space justify="space-around">
        <progress-circle
            v-for="(value, key) in usage"
            :key="key"
            :percentage="value"
            :title="key"
        >
            <span style="font-size: large">{{ ~~value }}%</span>
        </progress-circle>
    </n-space>
</template>
