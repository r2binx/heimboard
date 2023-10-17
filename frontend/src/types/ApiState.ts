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

interface StorageUsage {
    name: string;
    usage: {
        total: number;
        used: number;
        free: number;
        percent: number;
    };
}

type VmInfo = {
    name: string;
    UUID: string;
    state: keyof typeof VMState;
    mem_modifiable: boolean;
    current_memory: number;
    max_memory: number;
};

type HostServices = {
    jelly?: JellyMediaState[];
    plex?: boolean;
    kvm?: boolean;
    nzb?: boolean;
};

interface Result {
    result: {
        success: boolean;
        message: string;
    };
}

type ApiState = {
    active: boolean;
    fritz: FritzInfo | undefined;
    net_reachable: boolean;
    reachable: boolean;
    refreshing: boolean;
    schedule: BootSchedule | undefined;
    services: HostServices | undefined;
    storage: StorageUsage[] | undefined;
    uptime: number;
    vms: VmInfo[] | undefined;
};

interface JellyNowPlayingItem {
    title: string;
    paused: boolean;
    position: number;
    duration: number;
    play_method: string;
}

interface JellyMediaState {
    user: string;
    client: string;
    device: string;
    last_activity: number;
    now_playing?: JellyNowPlayingItem;
}

export type {
    ApiState,
    Result,
    StorageUsage,
    HostServices,
    BootSchedule,
    FritzInfo,
    VmInfo,
    JellyMediaState,
    JellyNowPlayingItem,
};
