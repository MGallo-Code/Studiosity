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
    { path: "/", component: PublicSetsComponent, name: "Home", meta: { title: "Home Page" } },
    { path: "/login", component: LoginComponent, name: "Login", meta: { title: "Login" } },
    { path: "/signup", component: SignupComponent, name: "Signup", meta: { title: "Sign Up" } },
    {
        path: "/my-study-sets/:page?",
        component: MySetsComponent,
        meta: { requiresAuth: true, title: "My Study Sets" },
        name: "MyStudySets",
    },
    {
        path: "/my-study-set/:id/:page?",
        component: MySetDetailComponent,
        meta: { requiresAuth: true, title: "My Study Set Details" },
    },
    {
        path: "/public-study-sets/:page?",
        component: PublicSetsComponent,
        meta: { title: "Public Study Sets" },
    },
    {
        path: "/study-set/:id",
        component: SetDetailComponent,
        meta: { title: "Study Set Details" },
    },
    {
        path: "/my-profile",
        component: MyProfileComponent,
        meta: { requiresAuth: true, title: "My Profile" },
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach(async (to, from, next) => {
    // Set the document title using the meta field of the route
    document.title = to.meta.title || "Studiosity";

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
