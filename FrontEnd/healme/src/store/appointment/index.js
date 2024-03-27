import axios from 'axios';
import router from "../../router";
import { msgError, msgSuccess } from "../../Tools/tools";

const appointmentModule = {
    namespaced: true,
    state: {
        clinics: [],
        appointment: [],
        userAppointments: [],
        clinicDoctors: [],
    },
    getters: {
        getClinics(state) {
            return state.clinics;
        },
        getAppointment(state) {
            return state.clinics;
        },
    },
    mutations: {
        setClinics(state, payload) {
            state.clinics = payload
        },
        setDoctors(state,payload) {
            state.clinicDoctors = payload
        },
        setAppointments(state,payload) {
            state.availableAppointment = payload
        },
    },
    actions: {
        async getAllClinics({commit}, payload) {
            try {
                commit("notificationModule/setLoading", true, { root: true });
                axios.get('https://5sv31llj-5002.asse.devtunnels.ms/')
                    .then(response => {
                        commit("setClinics", response.data);
                    })
                    .catch(error => {
                        console.error(error);
                        // Handle login failure here (e.g., show error message)
                    });
                } 
            finally {
                commit("notificationModule/setLoading", false, { root: true });
            }
        },
        async getAllDoctorsInClinic({commit}, payload) {
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
                } 
            finally {
                commit("notificationModule/setLoading", false, { root: true });
            }
        },
        async getDoctorAvailableAppointment({commit}, payload){
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
                } 
            finally {
                commit("notificationModule/setLoading", false, { root: true });
            }
        },
        async createAppointment({commit}, payload) {
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
                }     
            finally {
                commit("notificationModule/setLoading", false, { root: true });
            }
        },
        async getAllUserAppointments({commit}, payload) {
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
                } 
            finally {
                commit("notificationModule/setLoading", false, { root: true });
            }
        },
        async getAppointmentDetails({commit}, payload) {
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
        async editAppointment({commit}, payload) {
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
                }     
            finally {
                commit("notificationModule/setLoading", false, { root: true });
            }
        },
        async deleteAppointment({commit}, payload) {
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
                } 
            finally {
                commit("notificationModule/setLoading", false, { root: true });
            }
        },
    }
};

export default appointmentModule;
