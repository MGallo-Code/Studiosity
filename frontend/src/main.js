import { createApp } from "vue";
import App from "./App.vue";
import router from "./utils/router.js";
import store from "./utils/store";

store.dispatch("checkAuthState").then(() => {
    const app = createApp(App);
    app.use(store);
    app.use(router);
    app.mount("#app");
});
