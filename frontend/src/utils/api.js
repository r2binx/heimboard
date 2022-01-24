import axios from "axios";
import { reactive } from "vue";

const host = "https://" + import.meta.env.VITE_APP_IDLEREPORTER

export function fritzInfo() {
    return axios.get(host + "/fritz/info");
}

export function fetchIdle() {
    return axios.get(host + "/idle");
}

/**
 returns a promise with uptime in seconds
 */
export function fetchUptime() {
    return axios.get(host + "/uptime", {timeout: 1000});
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
    let data = {"schedule": time}
    return axios.post("https://" + import.meta.env.VITE_APP_WAKESERVER + "/bootSchedule", data);
}

/**
 *
 */
export function fetchScheduledBoot() {
    return axios.get("https://" + import.meta.env.VITE_APP_WAKESERVER + "/bootSchedule");
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
    return axios.put(host + "/vm/" + vmName, {state: "destroy"});
}

/**
 * @param  {} vmName Name of the vm
 * @param  {} memory Amount of memory in KiB
 */
export function setVmMemory(vmName, memory) {
    return axios.put(host + "/vm/" + vmName, {memory: memory});
}

export function wakeOnLan() {
    return axios.get("https://" + import.meta.env.VITE_APP_WAKESERVER + "/wakeup", {timeout: 1000});
}

export function fetchWakeAvail() {
    return axios.get("https://" + import.meta.env.VITE_APP_WAKESERVER + "/ping", {timeout: 1000});
}

export class State {
    constructor() {
        this.reachable = false;
        this.idle = false;
        this.uptime = 0;
        this.services = {};
        this.vms = [];
        this.fritz = {};
        this.schedule = {}

        return reactive(this)
    }

    refreshState() {
        fetchUptime().then(res => {
            if (res.status === 200) {
                this.uptime = res.data;
                this.reachable = true;

                fetchIdle().then(idleres => {
                    this.idle = idleres.data.result
                    this.services = idleres.data.idle
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

                fetchScheduledBoot().then(schedres => {
                    if (schedres.status === 200) {
                        let schedule = schedres.data.time
                        if (schedule) {
                            // python uses seconds for timestamps
                            this.schedule.boot = schedres.data.time * 1000
                        }
                    }
                })

            } else {
                this.reachable = false;
            }
        }).catch(err => {
            console.log(err);
        });

    }
}