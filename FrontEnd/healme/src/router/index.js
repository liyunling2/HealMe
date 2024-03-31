import { createRouter, createWebHistory, START_LOCATION } from 'vue-router'
import store from '../store/index'; // Import your Vuex store

// Views Auth
import LoginView from "../views/auth/LoginView.vue";
import SignupView from "../views/auth/SignupView.vue";
import ProfileView from "../views/ProfileView.vue";
import NotFoundView from "../views/PageNotFound.vue";
import DoctorView from "@/views/DoctorProfile.vue";
import BookAnAppointmentView from '@/views/appointments/BookAnAppointmentView';
import CreateBlockSlot from '@/views/appointments/CreateBlockSlotView'

const routes = [
  { path: "/", name: "home", component: ProfileView, meta: { auth: true }},
  { path: "/login", name: "login", component: LoginView, },
  { path: "/signup", name: "signup", component: SignupView, },
  { path: "/DoctorProfile/:id", name: "doctorProfile", component: DoctorView, },
  { path: "/bookAppointment", name: "bookAppointment", component: BookAnAppointmentView, meta: { auth: true }},
  { path: "/createBlockSlot", name: "createBlockSlot", component: CreateBlockSlot, meta: { auth: true, doctor: true }},
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
  const isPatient = store.getters['authModule/ifPatient'];
  const isDoctor = store.getters['authModule/ifDoctor'];

  // Check if the route requires authentication
  const requiresAuth = to.matched.some(record => record.meta.auth);
  const requiresPatient = to.matched.some(record => record.meta.patient);

  
  if (requiresAuth && !isAuth) {
    // If the route requires authentication and the user is not authenticated,
    // redirect to the login page.
    next({ name: 'login' });
  } else if ((to.name === 'login' || to.name === 'signup') && isAuth) {
    // If the user is already authenticated and tries to visit the login or signup page,
    // redirect them to the home page as a default action.
    next({ name: 'home' });
  } else if (requiresPatient && isPatient) {
    // If the route requires the user to be a patient and they are not,
    // redirect to the home page or an appropriate page.
    next({ name: 'home' });
  } else if (requiresPatient && !isDoctor) {
    // If the route requires the user to be a doctor and they are not,
    // redirect to the home page or an appropriate page.
    next({ name: 'home' });
  }  else {
    // In all other cases, proceed as normal.
    next();
  }
});
export default router
