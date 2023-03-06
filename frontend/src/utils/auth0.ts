import { createAuth0, type Auth0VueClientOptions } from "@auth0/auth0-vue";

const config: Auth0VueClientOptions = {
    domain: import.meta.env.VITE_AUTH0_DOMAIN,
    clientId: import.meta.env.VITE_AUTH0_CLIENT_ID,
    cacheLocation: "localstorage",
    useRefreshTokens: true,
    authorizationParams: {
        scope: "openid profile offline_access",
        audience: import.meta.env.VITE_AUTH0_AUDIENCE,
        redirect_uri: window.location.origin,
    },
};

export default createAuth0(config);
