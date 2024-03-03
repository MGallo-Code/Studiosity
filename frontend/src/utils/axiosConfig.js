import axios from "axios";
import router from "@/utils/router";
import store from "@/utils/store";

export const axiosDefaultInstance = axios.create({
    baseURL: "https://studiosity.io/api/",
});

export const axiosAuthInstance = axios.create({
    baseURL: "https://studiosity.io/api/",
    withCredentials: true,
});

const refreshToken = async () => {
    try {
        await axiosAuthInstance.post("/token/refresh/", null, {
            _ignoreInterceptor: true,
        });
        return true;
    } catch (error) {
        store.dispatch("logout");
        router.push({ path: "/login" });
        return false;
    }
};

function applyResponseInterceptor(instance) {
    instance.interceptors.response.use(
        async (response) => response,
        async (error) => {
            const originalRequest = error.config;

            // Handling 401 errors
            // Avoid intercepting if _ignoreInterceptor is set
            if (
                error.response &&
                error.response.status === 401 &&
                !error.config._ignoreInterceptor
            ) {
                originalRequest._ignoreInterceptor = true;
                const tokenRefreshed = await refreshToken();
                if (tokenRefreshed) {
                    console.log("Token refreshed!");
                    return axiosAuthInstance(originalRequest);
                } else {
                    // Resolve to suppress further errors, if token wasn't refreshed it was handled.
                    return Promise.resolve("Session ended");
                }
            }

            // For other types of errors, reject the promise
            return Promise.reject(error);
        }
    );
}

applyResponseInterceptor(axiosDefaultInstance);
applyResponseInterceptor(axiosAuthInstance)