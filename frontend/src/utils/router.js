import { createRouter, createWebHistory } from "vue-router";
import HomeComponent from "@/components/HomeComponent.vue";
import LoginComponent from "@/components/LoginComponent.vue";
import SignupComponent from "@/components/SignupComponent.vue";
import MySetsComponent from "@/components/MySetsComponent.vue";
import PublicSetsComponent from "@/components/PublicSetsComponent.vue";

const routes = [
    { path: "/", component: HomeComponent },
    { path: "/login", component: LoginComponent },
    { path: "/signup", component: SignupComponent },
    { path: "/my-study-sets", component: MySetsComponent },
    { path: "/public-study-sets", component: PublicSetsComponent },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
