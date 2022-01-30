<script setup>
import { NTimePicker } from 'naive-ui';
import { scheduleBoot, } from "@/utils/api"
import { inject } from "vue";

const state = inject('state');
const auth = inject('auth');
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
        :disabled="!auth.hasPermission('admin')"
        format="HH:mm"
        :value="scheduledBoot"
        placeholder="Not set"
        :minutes="15"
        style="width: 110px"
        @update:value="handleBoot"
    />
</template>
