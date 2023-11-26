import { createRouter, createWebHistory } from "vue-router";
import LoginComponent from "@/components/LoginComponent.vue";
import SignupComponent from "@/components/SignupComponent.vue";

const routes = [
    { path: "/", component: LoginComponent },
    { path: "/login", component: LoginComponent },
    { path: "/signup", component: SignupComponent },
    { path: "/my-study-sets", component: LoginComponent },
    { path: "/public-study-sets", component: LoginComponent },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
