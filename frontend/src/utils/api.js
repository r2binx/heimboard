import axios from "axios";
import { ref } from "vue";

const host = "https://" + import.meta.env.VITE_APP_IDLEREPORTER


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

export class State {
    constructor() {
        this.reachable = ref(false);
        this.idle = ref(false)
        this.uptime = ref(0);
        this.services = ref({});
        this.vms = ref([]);
    }

    refreshState() {
        fetchUptime().then(res => {
            if (res.status == 200) {
                this.uptime.value = res.data;
                this.reachable.value = true;

                fetchIdle().then(idleres => {
                    this.idle.value = idleres.data.result
                    this.services.value = idleres.data.idle
                });

                fetchAllVms().then(vmres => {
                    if (vmres.status == 200) {
                        this.vms.value = vmres.data.result;
                    }
                });

            } else {
                this.reachable.value = false;
            }
        }).catch(err => {
            console.log(err);
        });

    }
}