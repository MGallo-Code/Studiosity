import { createRouter, createWebHistory } from "vue-router";
import HomeComponent from "@/components/HomeComponent.vue";
import LoginComponent from "@/components/LoginComponent.vue";
import SignupComponent from "@/components/SignupComponent.vue";
import MyStudySetsComponent from "@/components/MyStudySetsComponent.vue";

const routes = [
    { path: "/", component: HomeComponent },
    { path: "/login", component: LoginComponent },
    { path: "/signup", component: SignupComponent },
    { path: "/my-study-sets", component: MyStudySetsComponent },
    { path: "/public-study-sets", component: LoginComponent },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
