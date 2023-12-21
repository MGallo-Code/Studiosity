import { createRouter, createWebHistory } from "vue-router";
import store from "@/utils/store";
import HomeComponent from "@/components/HomeComponent.vue";
import LoginComponent from "@/components/LoginComponent.vue";
import SignupComponent from "@/components/SignupComponent.vue";
import MySetDetailComponent from "@/components/MySetDetailComponent.vue";
import MySetsComponent from "@/components/MySetsComponent.vue";
import PublicSetsComponent from "@/components/PublicSetsComponent.vue";
import SetDetailComponent from "@/components/SetDetailComponent.vue";
import MyProfileComponent from "@/components/MyProfileComponent.vue";

const routes = [
    { path: "/", component: HomeComponent },
    { path: "/login", component: LoginComponent },
    { path: "/signup", component: SignupComponent },
    {
        path: "/my-study-sets/:page?",
        component: MySetsComponent,
        meta: { requiresAuth: true },
    },
    {
        path: "/my-study-set/:id/:page?",
        component: MySetDetailComponent,
        meta: { requiresAuth: true },
    },
    { path: "/public-study-sets/:page?", component: PublicSetsComponent },
    { path: "/study-set/:id", component: SetDetailComponent },
    {
        path: "/my-profile",
        component: MyProfileComponent,
        meta: { requiresAuth: true },
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach((to, from, next) => {
    if (
        to.matched.some((record) => record.meta.requiresAuth) &&
        !store.state.isAuthenticated
    ) {
        next({ path: "/login", query: { redirect: to.fullPath } });
    } else {
        next();
    }
});

export default router;
