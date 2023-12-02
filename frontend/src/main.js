import { createApp } from "vue";
import App from "./App.vue";
import router from "./utils/router.js";
import store from "./utils/store";
import { library } from "@fortawesome/fontawesome-svg-core";
import { faEdit, faTrashAlt, faClone } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

library.add(faEdit, faTrashAlt, faClone);

store.dispatch("checkAuthState").then(() => {
    const app = createApp(App);
    app.component("font-awesome-icon", FontAwesomeIcon);
    app.use(store);
    app.use(router);
    app.mount("#app");
});
