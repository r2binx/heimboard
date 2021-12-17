import axios from "axios";

const host = "http://192.168.178.175:18500"

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
    return axios.get("http://192.168.178.22:15000/wakeup");
}
