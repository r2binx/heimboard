import type {
    BootSchedule,
    ApiState,
    HostServices,
    VmInfo,
    FritzInfo,
    Result,
    StorageUsage,
} from "@/types/ApiState";
import axios, { type RawAxiosRequestConfig } from "axios";
import type { ToRefs } from "vue";
import { reactive, toRefs } from "vue";

const host = "https://" + import.meta.env.VITE_APP_IDLEREPORTER;

async function axiosRequest<T>(
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

    return axios.request<T>(requestConfig);
}

export function fritzInfo() {
    return axiosRequest<{ result: FritzInfo }>("GET", host + "/fritz/info");
}

export function fetchActive() {
    return axiosRequest<{ active: HostServices }>("GET", host + "/active");
}

/**
 * @returns a promise with uptime in seconds
 */
export function fetchUptime() {
    return axiosRequest<number>("GET", host + "/uptime", { timeout: 1000 });
}

export function reboot() {
    return axiosRequest<Result["result"]>("GET", host + "/reboot");
}

export function tryShutdown() {
    return axiosRequest<Result["result"]>("GET", host + "/inactive-shutdown");
}

export function shutdown() {
    return axiosRequest<Result["result"]>("GET", host + "/shutdown");
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
    return axiosRequest<BootSchedule>(
        "GET",
        "https://" + import.meta.env.VITE_APP_WAKESERVER + "/boot-schedule"
    );
}

export function fetchAllVms() {
    return axiosRequest<{ result: VmInfo[] }>("GET", host + "/vm/all");
}

/**
 * @param  {} vmName Name of the vm
 */
export function stopVm(vmName: string) {
    return axiosRequest<Result>("POST", host + "/vm/" + vmName + "/stop");
}

/**
 * @param  {} vmName Name of the vm
 */
export function startVm(vmName: string) {
    return axiosRequest<Result>("POST", host + "/vm/" + vmName + "/start");
}

/**
 * @param  {} vmName Name of the vm
 */
export function destroyVm(vmName: string) {
    return axiosRequest<Result>("PUT", host + "/vm/" + vmName, {
        data: { state: "destroy" },
    });
}

/**
 * @param  {} vmName Name of the vm
 */
export function suspendVm(vmName: string) {
    return axiosRequest<Result>("PUT", host + "/vm/" + vmName, {
        data: { state: "suspend" },
    });
}

/**
 * @param  {} vmName Name of the vm
 */
export function resumeVm(vmName: string) {
    return axiosRequest<Result>("PUT", host + "/vm/" + vmName, {
        data: { state: "resume" },
    });
}

/**
 * @param  {} vmName Name of the vm
 * @param  {} memory Amount of memory in KiB
 */
export function setVmMemory(vmName: string, memory: number) {
    return axiosRequest<Result>("PUT", host + "/vm/" + vmName, {
        data: { memory: memory },
    });
}

export function wakeOnLan() {
    return axiosRequest<Result["result"]>(
        "GET",
        "https://" + import.meta.env.VITE_APP_WAKESERVER + "/wakeup"
    );
}

export function fetchWakeAvail() {
    return axiosRequest<string>(
        "GET",
        "https://" + import.meta.env.VITE_APP_WAKESERVER + "/ping",
        { timeout: 1000 }
    );
}

export function fetchStorageUsage() {
    return axiosRequest<{ result: StorageUsage[] }>("GET", host + "/storage/usage", {
        timeout: 2000,
    });
}

function catchNetworkError(error: any, message: string) {
    if (!!error.isAxiosError && !error.response) {
        console.log(message);
        console.debug(error);
    } else {
        console.log(error);
    }
}

const state: ApiState = reactive({
    reachable: false,
    active: false,
    uptime: 0,
    services: undefined,
    vms: undefined,
    fritz: undefined,
    schedule: undefined,
    storage: undefined,
    net_reachable: false,
    refreshing: false,
});

function useApiState(): ToRefs<ApiState> & { refreshState: (token: string) => void } {
    const refreshState = async (token: string) => {
        state.refreshing = true;
        axios.interceptors.request.use((config) => {
            if (config.headers) {
                config.headers.Authorization = `Bearer ${token}`;
            }
            return config;
        });

        const [wakeAvail, uptime] = await Promise.allSettled([
            fetchWakeAvail(),
            fetchUptime(),
        ]);

        if (wakeAvail.status === "fulfilled" && wakeAvail.value.status === 200) {
            state.net_reachable = true;

            const schedres = await fetchScheduledBoot();
            if (schedres.status === 200) {
                state.schedule = schedres.data;
            }
        } else {
            state.net_reachable = false;
        }

        if (uptime.status === "fulfilled" && uptime.value.status === 200) {
            state.uptime = uptime.value.data;
            state.reachable = true;

            const [activeServices, allVMs, fritz, storage] = await Promise.all([
                fetchActive(),
                fetchAllVms(),
                fritzInfo(),
                fetchStorageUsage(),
            ]);

            state.active = activeServices.data.active ? true : false;
            state.services = activeServices.data.active;
            state.vms = allVMs.data.result;
            state.fritz = fritz.data.result;
            state.storage = storage.data.result;
        } else {
            state.reachable = false;
        }

        state.refreshing = false;
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
