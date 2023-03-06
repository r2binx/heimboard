import type { useAuth0 as auth0VueClient } from "@auth0/auth0-vue";
import { ref } from "vue";

const accessToken = ref<string>();

export default function useAuth0(auth0: ReturnType<typeof auth0VueClient>) {
    const getAccessToken = async () => {
        const refreshToken = async () =>
            (accessToken.value = await auth0.getAccessTokenSilently());

        if (!accessToken.value && auth0.isAuthenticated.value) {
            await refreshToken();
        } else if (!auth0.isAuthenticated.value) {
            await auth0.loginWithRedirect();
            await refreshToken();
        }

        return accessToken.value!;
    };

    const hasPermission = (permissions: string) => {
        return (
            auth0.isAuthenticated.value &&
            auth0.user.value["https://heim.blckct.io/permissions"].indexOf(permissions) >
                -1
        );
    };

    return { accessToken, getAccessToken, hasPermission };
}
