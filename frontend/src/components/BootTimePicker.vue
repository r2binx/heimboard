<script setup lang="ts">
import { NTimePicker } from "naive-ui";
import { useAuth0 as auth0VueClient } from "@auth0/auth0-vue";
import useAuth0 from "@/composables/useAuth0";
import useApi from "@/composables/useApi";

const { hasPermission } = useAuth0(auth0VueClient());

const { useApiState, scheduleBoot } = useApi();
const { schedule } = useApiState();

function handleBoot(value: number | null) {
    if (value !== null) {
        if (schedule.value) {
            schedule.value.time = value;
        }
        scheduleBoot(value);
    }
}
</script>

<template>
    <n-time-picker
        clearable
        :disabled="!hasPermission('admin')"
        format="HH:mm"
        :value="schedule?.time"
        placeholder="Not set"
        :minutes="15"
        style="width: 110px"
        @update:value="handleBoot"
    />
</template>
