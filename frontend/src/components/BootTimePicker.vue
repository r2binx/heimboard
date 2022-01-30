<script setup>
import { NTimePicker } from "naive-ui";
import { scheduleBoot, } from "@/utils/api"
import { inject } from "vue";

const state = inject('state');

let scheduledBoot = $ref(state.schedule.boot)

function handleBoot(value) {
    scheduledBoot = value
    state.schedule.boot = scheduledBoot
    scheduleBoot(scheduledBoot)
}

</script>
<template>
    <n-time-picker
        clearable
        format="HH:mm"
        :value="scheduledBoot"
        placeholder="No time set"
        size="large"
        :minutes="15"
        style="width: max-content;"
        @update:value="handleBoot"
    />
</template>
<style>
</style>