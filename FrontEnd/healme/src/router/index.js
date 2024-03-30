import { createRouter, createWebHistory, START_LOCATION } from 'vue-router'
import store from '../store/index'; // Import your Vuex store


import HomeView from '../views/HomeView.vue'

// Views Auth
import LoginView from "../views/auth/LoginView.vue";
import SignupView from "../views/auth/SignupView.vue";
import ProfileView from "../views/ProfileView.vue";
import NotFoundView from "../views/PageNotFound.vue";
import BookAnAppointmentView from '@/views/appointments/BookAnAppointmentView';
import AppointmentView from "../views/appointments/ViewAppointment.vue"


const routes = [
  { path: "/", name: "home", component: ProfileView, meta: { auth: true }},
  { path: '/about', name: 'about', component: function () { return import(/* webpackChunkName: "about" */ '../views/AboutView.vue') } },
  { path: "/login", name: "login", component: LoginView, },
  { path: "/signup", name: "signup", component: SignupView, },
  { path: "/bookAppointment", name: "bookAppointment", component: BookAnAppointmentView, meta: { auth: true }},
  { path: "/appointment/:id", name: "appointment", component: AppointmentView, meta: { auth: true }, props: true },
  { path: "/profile", name: "profile", component: ProfileView, meta: { auth: true } },
  { path: "/:catchAll(.*)", component: NotFoundView }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  // Accessing the Vuex store's state to check if the user is authenticated
  const isAuth = store.getters['authModule/isAuth'];

  // Check if the route requires authentication
  const requiresAuth = to.matched.some(record => record.meta.auth);

  if (requiresAuth && !isAuth) {
    // If the route requires authentication and the user is not authenticated,
    // redirect to the login page.
    next({ name: 'login' });
  } else if ((to.name === 'login' || to.name === 'signup') && isAuth) {
    // If the user is already authenticated and tries to visit the login or signup page,
    // redirect them to the home page as a default action.
    next({ name: 'home' });
  } else {
    // In all other cases, proceed as normal.
    next();
  }
});
export default router
