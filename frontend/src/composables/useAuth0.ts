import { auth0 } from "@/utils/auth0";
import { ref } from "vue";

const accessToken = ref<string>();

export default function useAuth0() {
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

    const hasPermission = (): boolean => {
        if (!auth0.user.value) return false;
        return (
            auth0.isAuthenticated.value &&
            auth0.user.value["https://heim.blckct.io/roles"].some((role: string) =>
                ["admin", "guest"].includes(role)
            )
        );
    };

    const isAdmin = (): boolean => {
        if (!auth0.user.value) return false;
        return (
            auth0.isAuthenticated.value &&
            auth0.user.value["https://heim.blckct.io/roles"].indexOf("admin") > -1
        );
    };

    return { accessToken, getAccessToken, hasPermission, isAdmin };
}
