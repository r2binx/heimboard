import axios from "axios";
import { reactive } from "vue";

const host = "https://" + import.meta.env.VITE_APP_IDLEREPORTER

export function fritzInfo() {
    return axios.get(host + "/fritz/info");
}

export function fetchActive() {
    return axios.get(host + "/active");
}

/**
 returns a promise with uptime in seconds
 */
export function fetchUptime() {
    return axios.get(host + "/uptime", { timeout: 1000 });
}

export function reboot() {
    return axios.get(host + "/reboot");
}

export function shutdown() {
    return axios.get(host + "/shutdown");
}

/**
 * @param time unix timestamp of scheduled shutdown
 */
export function scheduleBoot(time) {
    let data = { "time": time, "action": "boot" };
    return axios.post("https://" + import.meta.env.VITE_APP_WAKESERVER + "/boot-schedule", data);
}

/**
 *
 */
export function fetchScheduledBoot() {
    return axios.get("https://" + import.meta.env.VITE_APP_WAKESERVER + "/boot-schedule");
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
 */
export function suspendVm(vmName) {
    return axios.put(host + "/vm/" + vmName, { state: "suspend" });
}

/**
 * @param  {} vmName Name of the vm
 */
export function resumeVm(vmName) {
    return axios.put(host + "/vm/" + vmName, { state: "resume" });
}

/**
 * @param  {} vmName Name of the vm
 * @param  {} memory Amount of memory in KiB
 */
export function setVmMemory(vmName, memory) {
    return axios.put(host + "/vm/" + vmName, { memory: memory });
}

export function wakeOnLan() {
    return axios.get("https://" + import.meta.env.VITE_APP_WAKESERVER + "/wakeup", { timeout: 1000 });
}

export function fetchWakeAvail() {
    return axios.get("https://" + import.meta.env.VITE_APP_WAKESERVER + "/ping", { timeout: 1000 });
}

export function fetchStorageUsage() {
    return axios.get(host + "/storage/usage", { timeout: 1000 });
}

export class State {
    constructor() {
        this.reachable = false;
        this.active = false;
        this.uptime = 0;
        this.services = {};
        this.vms = [];
        this.fritz = {};
        this.schedule = {}
        this.net_reachable = false

        return reactive(this)
    }

    refreshState() {
        fetchUptime().then(res => {
            if (res.status === 200) {
                this.uptime = res.data;
                this.reachable = true

                fetchActive().then(ares => {
                    this.active = ares.data.result
                    if (this.active) {
                        this.services = ares.data.active
                    }
                });

                fetchAllVms().then(vmres => {
                    if (vmres.status === 200) {
                        this.vms = vmres.data.result;
                    }
                });

                fritzInfo().then(fritzres => {
                    if (fritzres.status === 200) {
                        this.fritz = fritzres.data.result;
                    }
                })
            }
        }).catch(err => {
            if (!!err.isAxiosError && !err.response) {
                console.log("Server unreachable")
                console.debug(err)
            } else {
                console.log(err)
            }
        })

        fetchWakeAvail().then(res => {
            if (res.status === 200) {
                this.net_reachable = true

                fetchScheduledBoot().then(schedres => {
                    if (schedres.status === 200) {
                        let schedule = schedres.data.time
                        if (schedule) {
                            this.schedule.boot = schedres.data.time
                        }
                    }
                }).catch(err => {
                    if (!!err.isAxiosError && !err.response) {
                        console.log("Network unreachable")
                        console.debug(err)
                    } else {
                        console.log(err)
                    }
                })
            }
        })
    }
}
