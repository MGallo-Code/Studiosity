import { createRouter, createWebHistory } from "vue-router";
import store from "@/utils/store";
import LoginComponent from "@/components/LoginComponent.vue";
import SignupComponent from "@/components/SignupComponent.vue";
import MySetDetailComponent from "@/components/MySetDetailComponent.vue";
import MySetsComponent from "@/components/MySetsComponent.vue";
import PublicSetsComponent from "@/components/PublicSetsComponent.vue";
import SetDetailComponent from "@/components/SetDetailComponent.vue";
import MyProfileComponent from "@/components/MyProfileComponent.vue";
// import HomeComponent from "@/components/HomeComponent.vue";

const routes = [
    { path: "/", component: PublicSetsComponent },
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

router.beforeEach(async (to, from, next) => {
    // If the route requires authentication
    if (to.matched.some(record => record.meta.requiresAuth)) {
      // Check if the Vuex state already knows the user is authenticated
      if (store.state.isAuthenticated) {
        // User appears to be authenticated; proceed with navigation
        next();
      } else {
        // Vuex state is not authenticated; check localStorage
        const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';
        if (isAuthenticated) {
          // Local storage indicates the user is authenticated; validate the session
          await store.dispatch('validateSession');
          if (store.state.isAuthenticated) {
            // Session is valid; proceed with navigation
            next();
          } else {
            // Session is not valid; redirect to login
            next('/login');
          }
        } else {
          // User is definitely not authenticated; redirect to login
          next('/login');
        }
      }
    } else {
      // No authentication required for this route; proceed with navigation
      next();
    }
  });

export default router;
