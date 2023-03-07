import type { ApiState } from "@/types/ApiState";
import axios, { type RawAxiosRequestConfig } from "axios";
import { reactive, toRefs } from "vue";

const host = "https://" + import.meta.env.VITE_APP_IDLEREPORTER;

async function axiosRequest(
    method: "GET" | "POST" | string,
    url: string,
    options?: RawAxiosRequestConfig
) {
    let requestConfig = {
        method,
        url,
    } as RawAxiosRequestConfig;

    if (options) {
        requestConfig = { ...requestConfig, ...options };
    }

    return axios.request(requestConfig);
}

export function fritzInfo() {
    return axiosRequest("GET", host + "/fritz/info");
}

export function fetchActive() {
    return axiosRequest("GET", host + "/active");
}

/**
 * @returns a promise with uptime in seconds
 */
export function fetchUptime() {
    return axiosRequest("GET", host + "/uptime", { timeout: 1000 });
}

export function reboot() {
    return axiosRequest("GET", host + "/reboot");
}

export function tryShutdown() {
    return axiosRequest("GET", host + "/inactive-shutdown");
}

export function shutdown() {
    return axiosRequest("GET", host + "/shutdown");
}

/**
 * @param time unix timestamp of scheduled shutdown
 */
export function scheduleBoot(time: number) {
    return axiosRequest(
        "POST",
        "https://" + import.meta.env.VITE_APP_WAKESERVER + "/boot-schedule",
        { data: { time: time, action: "boot" } }
    );
}

export function fetchScheduledBoot() {
    return axiosRequest(
        "GET",
        "https://" + import.meta.env.VITE_APP_WAKESERVER + "/boot-schedule"
    );
}

export function fetchAllVms() {
    return axiosRequest("GET", host + "/vm/all");
}

/**
 * @param  {} vmName Name of the vm
 */
export function stopVm(vmName: string) {
    return axiosRequest("POST", host + "/vm/" + vmName + "/stop");
}

/**
 * @param  {} vmName Name of the vm
 */
export function startVm(vmName: string) {
    return axiosRequest("POST", host + "/vm/" + vmName + "/start");
}

/**
 * @param  {} vmName Name of the vm
 */
export function destroyVm(vmName: string) {
    return axiosRequest("PUT", host + "/vm/" + vmName, {
        data: { state: "destroy" },
    });
}

/**
 * @param  {} vmName Name of the vm
 */
export function suspendVm(vmName: string) {
    return axiosRequest("PUT", host + "/vm/" + vmName, {
        data: { state: "suspend" },
    });
}

/**
 * @param  {} vmName Name of the vm
 */
export function resumeVm(vmName: string) {
    return axiosRequest("PUT", host + "/vm/" + vmName, {
        data: { state: "resume" },
    });
}

/**
 * @param  {} vmName Name of the vm
 * @param  {} memory Amount of memory in KiB
 */
export function setVmMemory(vmName: string, memory: number) {
    return axiosRequest("PUT", host + "/vm/" + vmName, {
        data: { memory: memory },
    });
}

export function wakeOnLan() {
    return axiosRequest(
        "GET",
        "https://" + import.meta.env.VITE_APP_WAKESERVER + "/wakeup"
    );
}

export function fetchWakeAvail() {
    return axiosRequest(
        "GET",
        "https://" + import.meta.env.VITE_APP_WAKESERVER + "/ping",
        { timeout: 1000 }
    );
}

export function fetchStorageUsage() {
    return axios.get(host + "/storage/usage", { timeout: 1000 });
}

function catchNetworkError(error: any, message: string) {
    if (!!error.isAxiosError && !error.response) {
        console.log(message);
        console.debug(error);
    } else {
        console.log(error);
    }
}

const state: Omit<ApiState, "refreshState"> = reactive({
    reachable: false,
    active: false,
    uptime: 0,
    services: undefined,
    vms: undefined,
    fritz: undefined,
    schedule: undefined,
    net_reachable: false,
    refreshing: false,
});

function useApiState() {
    const refreshState = (token: string) => {
        state.refreshing = true;
        axios.interceptors.request.use((config) => {
            if (config.headers) {
                config.headers.Authorization = `Bearer ${token}`;
            }
            return config;
        });
        fetchUptime()
            .then(async (res) => {
                if (res.status === 200) {
                    state.uptime = res.data;
                    state.reachable = true;

                    const [activeServices, allVMs, fritz] = await Promise.all([
                        fetchActive(),
                        fetchAllVms(),
                        fritzInfo(),
                    ]);

                    state.active = activeServices.data.result;
                    state.services = activeServices.data.active;
                    state.vms = allVMs.data.result;
                    state.fritz = fritz.data.result;
                } else {
                    state.reachable = false;
                }
            })
            .catch((err) => {
                catchNetworkError(err, "Server unreachable");
                state.reachable = false;
            })
            .finally(() => {
                state.refreshing = false;
            });

        fetchWakeAvail()
            .then((res) => {
                if (res.status === 200) {
                    state.net_reachable = true;

                    fetchScheduledBoot()
                        .then((schedres) => {
                            if (schedres.status === 200) {
                                state.schedule = schedres.data;
                            }
                        })
                        .catch((err) => {
                            catchNetworkError(err, "Network unreachable");
                            state.net_reachable = false;
                        });
                }
            })
            .catch((err) => {
                catchNetworkError(err, "Network unreachable");
                state.net_reachable = false;
            });
    };

    return {
        ...toRefs(state),
        refreshState,
    };
}

export default function useApi() {
    return {
        useApiState,
        fetchStorageUsage,
        reboot,
        shutdown,
        tryShutdown,
        scheduleBoot,
        startVm,
        stopVm,
        destroyVm,
        suspendVm,
        resumeVm,
        setVmMemory,
        wakeOnLan,
    };
}
