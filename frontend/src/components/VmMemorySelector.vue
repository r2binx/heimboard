<script setup lang="ts">
import useApi from "@/composables/useApi";
import type { VmInfo } from "@/types/ApiState";
import { NSlider, NSelect, useMessage } from "naive-ui";

defineProps<{ vm: VmInfo; type: "slider" | "dropdown" }>();

const { setVmMemory, useApiState } = useApi();
const state = useApiState();
const message = useMessage();

function handleMemoryEdit(name: string, value: number) {
    setVmMemory(name, value * 1024 * 1024)
        .then((res) => {
            if (res.data.result.success && state.vms.value) {
                let index = state.vms.value.findIndex((vm) => vm.name === name);
                state.vms.value[index].current_memory = value * 1024 * 1024;
                message.success(
                    "Successfully set memory of " + name + " to " + value + "GB"
                );
            } else {
                message.error(res.data.result.message);
            }
        })
        .catch((err) => {
            message.error("Failed to set memory of " + name);
            console.log(err);
        });
}

function vmMemoryOptions(max_memory: number) {
    let options = [];
    for (let i = 1; i <= max_memory; i++) {
        options.push({
            value: i,
            label: i + "GB",
        });
    }
    return options;
}

function vmMemoryMarks(max_memory: number) {
    let options: Record<number, string> = {};
    for (let i = 1; i <= max_memory; i++) {
        if (i % 4 == 0) options[i] = i + "GB";
    }
    return options;
}
</script>

<template>
    <n-select
        v-if="type === 'dropdown'"
        style="width: 100px; min-width: 30%; max-width: 80%"
        :value="vm.current_memory / 1024 / 1024"
        :options="vmMemoryOptions(vm.max_memory / 1024 / 1024)"
        @update:value="($event) => handleMemoryEdit(vm.name, $event)"
    />
    <n-slider
        v-else-if="type === 'slider'"
        style="width: 90%; margin: 8px auto 42px"
        step="mark"
        :max="vm.max_memory / 1024 / 1024"
        :format-tooltip="(value) => `${value}GB`"
        :marks="vmMemoryMarks(vm.max_memory / 1024 / 1024)"
        :value="vm.current_memory / 1024 / 1024"
        @update:value="($event) => handleMemoryEdit(vm.name, $event)"
    />
</template>
