import { createStore } from "vuex";
import notificationModule from "./notification/index.js";
import authModule from "./auth/index.js";
import appointmentModule from "./appointment/index.js";

const store = createStore({
    modules: {
        authModule,
        notificationModule,
        appointmentModule
    }
});

export default store;
