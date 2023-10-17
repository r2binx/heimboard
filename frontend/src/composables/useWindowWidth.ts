import { ref } from "vue";
import { useEventListener } from "./useEventListener";

function useWindowWidth() {
    const windowWidth = ref(window.innerWidth);

    useEventListener(window, "resize", () => (windowWidth.value = window.innerWidth));

    return { windowWidth };
}

export { useWindowWidth };
