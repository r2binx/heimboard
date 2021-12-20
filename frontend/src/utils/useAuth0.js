import createAuth0Client from '@auth0/auth0-spa-js';
import { reactive } from 'vue';

let auth0Resolver;
const auth0Promise = new Promise(resolve => auth0Resolver = resolve);

export const AuthState = reactive({
    user: null,
    loading: false,
    isAuthenticated: false,
});

const config = {
    domain: import.meta.env.VITE_AUTH0_DOMAIN,
    client_id: import.meta.env.VITE_AUTH0_CLIENT_ID,
    audience: import.meta.env.VITE_AUTH0_AUDIENCE,
};

async function handleStateChange() {
    const auth0 = (await auth0Promise);
    AuthState.user = await auth0.getUser({ audience: config.audience });
    AuthState.isAuthenticated = !!(AuthState.user);
    AuthState.loading = false;
}

export async function initAuth() {
    AuthState.loading = true;
    createAuth0Client({
        domain: config.domain,
        client_id: config.client_id,
        cacheLocation: 'localstorage',
        redirect_uri: window.location.origin
    }).then(async auth => {
        auth0Resolver(auth);
        await handleStateChange();
    });
}

export async function login() {
    await (await auth0Promise).loginWithPopup({
        scope: 'openid profile',
        audience: config.audience
    });
    await handleStateChange();
}

export async function logout() {
    await (await auth0Promise).logout({
        returnTo: window.location.origin,
    });
}

export async function getToken() {
    return await (await auth0Promise).getTokenSilently({ audience: config.audience });
}
