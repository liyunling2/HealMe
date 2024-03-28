import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'
import Toaster from "@meforma/vue-toaster";

loadFonts()

const app = createApp(App);

app.use(router);
app.use(store);
app.use(vuetify);
app.use(Toaster);
app.mount("#app");


