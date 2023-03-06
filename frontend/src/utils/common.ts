export function progressColor(value: number, alpha = "FF") {
    if (value < 25) {
        return "#87D4F9" + alpha;
    } else if (value >= 25 && value < 40) {
        return "#61DBC3" + alpha;
    } else if (value >= 40 && value < 70) {
        return "#95DA74" + alpha;
    } else if (value >= 70 && value < 90) {
        return "#FAD375" + alpha;
    } else {
        return "#D9534F" + alpha;
    }
}

export function timeToString(time: number) {
    if (time < 120) {
        return time + "s";
    } else if (time < 3600) {
        return Math.floor(time / 60) + "m " + (time % 60) + "s";
    } else if (time < 86400) {
        return (
            Math.floor(time / 3600) +
            "h " +
            Math.floor((time % 3600) / 60) +
            "m " +
            (time % 60) +
            "s"
        );
    } else {
        return (
            Math.floor(time / 86400) +
            "d " +
            Math.floor((time % 86400) / 3600) +
            "h " +
            Math.floor((time % 3600) / 60) +
            "m " +
            (time % 60) +
            "s"
        );
    }
}

export function readableTime(timestamp: string) {
    const time = new Date(timestamp);
    return ("0" + time.getHours()).slice(-2) + ":" + ("0" + time.getMinutes()).slice(-2);
}

export function formatBytes(bytes: number, decimals = 2) {
    if (bytes === 0) return "0 Bytes";

    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];

    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + sizes[i];
}
