import createAuth0Client from '@auth0/auth0-spa-js';
import { ref } from 'vue';
import axios from "axios";

const config = {
    domain: import.meta.env.VITE_AUTH0_DOMAIN,
    client_id: import.meta.env.VITE_AUTH0_CLIENT_ID,
    audience: import.meta.env.VITE_AUTH0_AUDIENCE,
};

export class Auth {
    constructor() {
        this.loading = ref(true);
        this.isAuthenticated = ref(false);
        this.user = ref(null);
        let auth0Resolver;
        this.auth0Promise = new Promise(resolve => auth0Resolver = resolve);
        createAuth0Client({
            domain: config.domain,
            client_id: config.client_id,
            cacheLocation: 'localstorage',
            redirect_uri: window.location.origin
        }).then(async auth => {
            auth0Resolver(auth);
            await this.handleStateChange();
        });

        axios.interceptors.request.use(async (config) => {
            const token = await this.getToken();
            if (token) {
                config.headers.Authorization = `Bearer ${token}`;
            }
            return config;
        });
    }

    async handleStateChange() {
        const auth0 = await this.auth0Promise;
        const user = await auth0.getUser({
            audience: config.audience
        });
        this.isAuthenticated.value = !!(user);
        this.user.value = user;
        this.loading.value = false;
    }

    async login() {
        await (await this.auth0Promise).loginWithPopup({
            scope: 'openid profile',
            audience: config.audience
        });
        await this.handleStateChange();
    }

    async logout() {
        await (await this.auth0Promise).logout({
            returnTo: window.location.origin,
        });
        this.isAuthenticated.value = false;
        this.user.value = null;
    }

    async getToken() {
        return await (await this.auth0Promise).getTokenSilently({
            audience: config.audience
        });
    }

    hasPermission(permissions) {
        return this.isAuthenticated.value && this.user.value["https://heim.blckct.io/permissions"].indexOf(permissions) > -1;
    }
}
