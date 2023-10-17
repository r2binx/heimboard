import { onMounted, onUnmounted } from "vue";

function useEventListener(
    target: EventTarget,
    event: string,
    callback: EventListenerOrEventListenerObject
) {
    onMounted(() => target.addEventListener(event, callback));
    onUnmounted(() => target.removeEventListener(event, callback));
}

export { useEventListener };
