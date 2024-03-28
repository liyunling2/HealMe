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
        bookedSlots: []
    },
    getters: {
        getClinics(state) {
            return state.clinics;
        },
        getDoctorsClinics(state) {
            return state.clinicDoctors;
        },
        getDoctorAppointment(state) {
            return state.clinicDoctors;
        },
        getBookedSlots(state){
            return state.bookedSlots
        }
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
        setBookedSlots(state, payload) {
            state.bookedSlots = payload
        },
    },
    actions: {
        async getAllClinics({commit}, payload) {
            try {
                commit("notificationModule/setLoading", true, { root: true });
                axios.get('http://localhost:8100/clinic/view')
                    .then(response => {
                        commit("setClinics", response.data.data);
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
                // Extract clinicID from the payload
                const clinicID = payload.clinicID;
                axios.get(`http://localhost:8100/profile/doctor/view?clinicID=${clinicID}`)
                    .then(response => {
                        commit("setDoctors", response.data.data);
                    })
                    .catch(error => {
                        console.error(error);
                        // Handle login failure here (e.g., show error message)
                    });
            } finally {
                commit("notificationModule/setLoading", false, { root: true });
            }
        },
        async getBookedSlots({commit}, payload){
            try {
                commit("notificationModule/setLoading", true, { root: true });
                axios.get('http://localhost:8100/blockedslots/view')
                    .then(response => {
                        console.log(payload)
                        commit("setBookedSlots", response.data.data);
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