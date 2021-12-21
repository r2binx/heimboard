import axios from "axios";
import { reactive } from "vue";

import { getToken } from "./useAuth0"

const host = "https://" + import.meta.env.VITE_APP_IDLEREPORTER

axios.interceptors.request.use(async (config) => {
    const token = await getToken();
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export function fetchIdle() {
    return axios.get(host + "/idle");
}

/**
returns a promise with uptime in seconds
*/
export function fetchUptime() {
    return axios.get(host + "/uptime");
}

export function reboot() {
    return axios.get(host + "/reboot");
}

export function shutdown() {
    return axios.get(host + "/shutdown");
}

export function fetchAllVms() {
    return axios.get(host + "/vm/all");
}

/**
 * @param  {} vmName Name of the vm
 */
export function stopVm(vmName) {
    return axios.post(host + "/vm/" + vmName + "/stop");
}

/**
 * @param  {} vmName Name of the vm
 */
export function startVm(vmName) {
    return axios.post(host + "/vm/" + vmName + "/start");
}

/**
 * @param  {} vmName Name of the vm
 */
export function destroyVm(vmName) {
    return axios.put(host + "/vm/" + vmName, { state: "destroy" });
}

/**
 * @param  {} vmName Name of the vm
 * @param  {} memory Amount of memory in KiB
 */
export function setVmMemory(vmName, memory) {
    return axios.put(host + "/vm/" + vmName, { memory: memory });
}

export function wakeOnLan() {
    return axios.get("https://" + import.meta.env.VITE_APP_WAKESERVER + "/wakeup");
}

export function refreshState() {
    fetchUptime().then(res => {
        if (res.status == 200) {
            state.uptime = res.data;
            state.reachable = true;

            fetchIdle().then(idleres => {
                state.idle = idleres.data.result
                state.services = idleres.data.idle
            });

        } else {
            state.reachable = false;
        }
    }).catch(err => {
        state.reachable = false;
        console.log(err);
    });

    return state;
}

export const state = reactive({
    uptime: 0,
    reachable: false,
    idle: true,
    services: {}
});