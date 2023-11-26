// axios-config.js
import axios from "axios";

const axiosInstance = axios.create({
    // Optional: Set common base URL, headers, etc.
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

export default axiosInstance;
