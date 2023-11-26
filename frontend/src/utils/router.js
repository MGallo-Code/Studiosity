import { createRouter, createWebHistory } from "vue-router";
import HomeComponent from "@/components/HomeComponent.vue";
import LoginComponent from "@/components/LoginComponent.vue";
import SignupComponent from "@/components/SignupComponent.vue";
import MySetsComponent from "@/components/MySetsComponent.vue";
import PublicSetsComponent from "@/components/PublicSetsComponent.vue";
import SetDetailComponent from "@/components/SetDetailComponent.vue";

const routes = [
    { path: "/", component: HomeComponent },
    { path: "/login", component: LoginComponent },
    { path: "/signup", component: SignupComponent },
    { path: "/my-study-sets/:page?", component: MySetsComponent },
    { path: "/public-study-sets/:page?", component: PublicSetsComponent },
    { path: "/study-set/:id", component: SetDetailComponent },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
