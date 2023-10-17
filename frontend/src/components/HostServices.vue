<script setup lang="ts">
import { timeToString } from "@/utils/common";
import useApi from "@/composables/useApi";
import useAuth0 from "@/composables/useAuth0";
import { computed } from "vue";
import type { JellyMediaState } from "@/types/ApiState";

const { useApiState } = useApi();
const state = useApiState();
const { isAdmin } = useAuth0();

const jellyActive = computed(() => {
    const jelly = state.services.value?.jelly;
    if (jelly && jelly.length > 0) {
        return jelly.filter((item) => item.now_playing);
    }
    return [];
});
const lastJellyActive = computed(() => {
    const jelly = state.services.value?.jelly;
    if (jelly && jelly.length > 0) {
        return Math.min(...jelly.map((item) => item.last_activity));
    }
    return -1;
});
</script>

<template>
    <n-divider title-placement="left">Active</n-divider>
    <n-table :striped="true">
        <n-tbody>
            <n-tr v-for="(status, service) in state.services?.value" :key="service">
                <template v-if="isAdmin()">
                    <n-td>
                        <n-collapse>
                            <n-collapse-item :title="service">
                                <template #header-extra>
                                    <span :class="status ? 'active' : 'idle'">
                                        {{
                                            status
                                                ? `${
                                                      service === "jelly" &&
                                                      jellyActive.length > 0
                                                          ? jellyActive.length
                                                          : ""
                                                  } Active ${
                                                      service === "jelly" &&
                                                      lastJellyActive > 0
                                                          ? timeToString(
                                                                lastJellyActive
                                                            ) + " ago"
                                                          : ""
                                                  }`
                                                : "Idle"
                                        }}
                                    </span>
                                </template>
                                <template v-if="jellyActive.length > 0">
                                    <MediaCard
                                        v-for="(
                                            itemDetails, index
                                        ) in jellyActive as Required<JellyMediaState>[]"
                                        :key="index"
                                        :details="itemDetails"
                                    />
                                </template>
                                <template v-else-if="service === 'jelly'">
                                    <n-table v-if="status" striped>
                                        <n-tbody>
                                            <n-tr
                                                v-for="(
                                                    item, index
                                                ) in status as JellyMediaState[]"
                                                :key="index"
                                            >
                                                <n-td>{{ item.user }}</n-td>
                                                <n-td
                                                    ><span style="float: right">
                                                        Last Activity:
                                                        {{
                                                            timeToString(
                                                                item.last_activity
                                                            )
                                                        }}</span
                                                    ></n-td
                                                >
                                            </n-tr>
                                        </n-tbody>
                                    </n-table>
                                </template>
                                <pre v-else>
                                {{ JSON.stringify(status, null, 2) }}
                            </pre
                                >
                            </n-collapse-item>
                        </n-collapse>
                    </n-td>
                </template>
                <template v-else>
                    <n-td>{{ service }}</n-td>
                    <n-td>
                        <span style="float: right" :class="status ? 'active' : 'idle'">
                            {{
                                status
                                    ? `${
                                          service === "jelly" ? jellyActive.length : ""
                                      } Active`
                                    : "Idle"
                            }}
                        </span>
                    </n-td>
                </template>
            </n-tr>
        </n-tbody>
    </n-table>
</template>
