// axios-config.js
import axios from "axios";

const axiosInstance = axios.create({
    baseURL: "http://localhost:8000/api/",
});

axiosInstance.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem("token");
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

axiosInstance.interceptors.response.use(
    (response) => {
        return response;
    },
    async (error) => {
        const originalRequest = error.config;
        if (error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            // Attempt to refresh token
            const refreshToken = localStorage.getItem("refresh_token");
            try {
                // Make a request to refresh the token here
                const response = await axiosInstance.post("/token/refresh/", {
                    refresh: refreshToken,
                });
                // Update token in local storage
                localStorage.setItem("token", response.data.access);
                // Update token in original request
                originalRequest.headers[
                    "Authorization"
                ] = `Bearer ${response.data.access}`;

                // Retry the original request
                return axiosInstance(originalRequest);
            } catch (refreshError) {
                // Handle refresh token failure
                localStorage.removeItem("token");
                localStorage.removeItem("refresh_token");
                window.location.href = "/login";
                return Promise.reject(refreshError);
            }
        }
        // Return any other error
        return Promise.reject(error);
    }
);

export default axiosInstance;
