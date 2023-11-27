// axios-config.js
import axios from "axios";

export const axiosAuthInstance = axios.create({
    baseURL: "http://localhost:8000/api/",
    withCredentials: true,
});

axiosAuthInstance.interceptors.response.use(
    (response) => response,
    (error) => Promise.reject(error)
);

export const axiosNonAuthInstance = axios.create({
    baseURL: "http://localhost:8000/api/",
    withCredentials: true,
});

axiosNonAuthInstance.interceptors.response.use(
    (response) => response,
    (error) => Promise.reject(error)
);
