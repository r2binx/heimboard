<script setup lang="ts">
import { NButton, useMessage, useNotification } from "naive-ui";
import { useRegisterSW } from "virtual:pwa-register/vue";
import { h } from "vue";

const notification = useNotification();
const message = useMessage();
const { updateServiceWorker } = useRegisterSW({
    onNeedRefresh: () => updateNotification(),
    onOfflineReady: () => message.success("Install successful"),
    onRegisterError: (err) => console.log(err),
    onRegisteredSW: (swUrl, reg) => {
        console.log("Registered service worker:", swUrl);
        console.log("Registration:", reg);
    },
});
const updateNotification = () => {
    const n = notification.info({
        title: "Update available",
        content: "A new version is available, click to reload",
        action: () =>
            h(
                NButton,
                {
                    type: "primary",
                    onClick: () => {
                        updateServiceWorker();
                        n.destroy();
                    },
                },
                { default: () => "Reload" }
            ),
    });
};
</script>
<template>
    <slot />
</template>
