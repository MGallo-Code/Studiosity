import { createApp } from "vue";
import App from "./App.vue";
import router from "./utils/router.js";
import store from "./utils/store";

const app = createApp(App);
app.use(router);
app.use(store);
store.dispatch("checkAuthState");
app.mount("#app");
