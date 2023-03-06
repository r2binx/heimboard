interface BootSchedule {
    time: number;
    action: "boot" | string;
}

interface FritzInfo {
    net: {
        up: number;
        down: number;
    };
    ip: {
        v4: string;
        v6: string;
    };
}

enum VMState {
    no_state,
    running,
    blocked,
    paused,
    shutdown,
    shutoff,
    crashed,
    suspended,
}

type VmInfo = {
    name: string;
    UUID: string;
    state: keyof typeof VMState;
    mem_modifiable: boolean;
    current_memory: number;
    max_memory: number;
};

type ApiState = {
    reachable: boolean;
    active: boolean;
    uptime: number;
    services: Record<"jelly" | "plex" | "kvm" | "nzb", boolean> | undefined;
    vms: VmInfo[] | undefined;
    fritz: FritzInfo | undefined;
    schedule: BootSchedule | undefined;
    net_reachable: boolean;
    refreshing: boolean;
    refreshState: (token: string) => void;
};

export type { ApiState, BootSchedule, FritzInfo, VmInfo };
