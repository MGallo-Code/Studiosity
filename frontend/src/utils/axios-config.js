import axios from "axios";
import router from "@/utils/router";

export const axiosDefaultInstance = axios.create({
    baseURL: "http://localhost:8000/api/",
});

export const axiosAuthInstance = axios.create({
    baseURL: "http://localhost:8000/api/",
    withCredentials: true,
});

const refreshToken = async () => {
    try {
        await axiosAuthInstance.post("/token/refresh/", null, {
            _ignoreInterceptor: true,
        });
        return true;
    } catch (error) {
        if (error.response && error.response.data.code === "token_not_valid") {
            router.push({ path: "/login" });
        }
        return false;
    }
};

axiosAuthInstance.interceptors.response.use(
    async (response) => response,
    async (error) => {
        const originalRequest = error.config;

        // Handling 401 errors
        if (error.response && error.response.status === 401) {
            // Avoid intercepting for token refresh or if a retry has already been attempted
            if (
                !originalRequest._retry &&
                !originalRequest._ignoreInterceptor
            ) {
                originalRequest._retry = true;
                const tokenRefreshed = await refreshToken();
                if (tokenRefreshed) {
                    return axiosAuthInstance(originalRequest);
                } else {
                    // Resolve to suppress further errors
                    return Promise.resolve();
                }
            }
        }

        // For other types of errors, reject the promise
        return Promise.reject(error);
    }
);
