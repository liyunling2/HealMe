import { createStore } from "vuex";
import authModule from "./auth/index.js";
import appointmentModule from "./appointment/index.js";
import ratingsModule from "./ratings/index.js";
import notificationModule from "./notification/index.js";

const store = createStore({
    modules: {
        authModule,
        notificationModule,
        appointmentModule,
        ratingsModule
    }
});

export default store;
