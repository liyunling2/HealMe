import axios from 'axios';
import router from "../../router";
import { msgError, msgSuccess } from "../../Tools/tools";



const appointmentModule = {
    namespaced: true,
    state: {
        clinics: [],
        appointment: [],
        userAppointments: [],
        doctorClinic: [],
    },
    getters: {
        getClinics(state) {
            return state.clinics;
        },
    },
    mutations: {
        setClinics(state, payload) {
            state.clinics = payload
        },
        setDoctors(state,payload) {
            state.doctorClinic = payload
        },
        clearUser(state) {
            state.user = DEFAULT_USER;
            state.auth = false;
        },
        cleanUsers(state) {
            state.users = [];
        },
        addAllUsers(state, payload) {
            state.users.push(payload);
        }
    },
    actions: {
        async getClinicsService({commit}, payload) {
            try {
                commit("notificationModule/setLoading", true, { root: true });
                axios.get('https://5sv31llj-5002.asse.devtunnels.ms/')
                    .then(response => {
                        console.log(response)
                        //commit("setClinics", response.data);
                    })
                    .catch(error => {
                        console.error(error);
                        // Handle login failure here (e.g., show error message)
                    });
                } finally {
                    commit("notificationModule/setLoading", false, { root: true });
                }
        },
        async getDoctorsService({commit}, payload) {
            try {
                commit("notificationModule/setLoading", true, { root: true });
                axios.get('https://5sv31llj-5002.asse.devtunnels.ms/')
                    .then(response => {
                        console.log(response)
                        //commit("setDoctors", response.data);
                    })
                    .catch(error => {
                        console.error(error);
                        // Handle login failure here (e.g., show error message)
                    });
                } finally {
                    commit("notificationModule/setLoading", false, { root: true });
                }
        },
    }
};

export default appointmentModule;
