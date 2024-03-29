import axios from 'axios';
import router from "../../router";
import { msgError, msgSuccess } from "../../Tools/tools";
import Vue from 'vue';
import { nextTick } from 'vue';

const appointmentModule = {
    namespaced: true,
    state: {
        clinics: [],
        appointment: [],
        userAppointments: [],
        clinicDoctors: [],
        bookedSlots: null,
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
                await axios.get('api/clinic/view')
                    .then(response => {
                        commit("setClinics", response.data.data);
                    })
                    .catch(error => {
                        console.error(error);
                        // Handle login failure here (e.g., show error message)
                    });
                } 
            finally {
            }
        },
        async getAllDoctorsInClinic({ commit }, payload) {
            try {
                const clinicID = payload.clinicID;
                const response = await axios.get(`api/profile/doctor/view?clinicID=${clinicID}`);
                commit("setDoctors", response.data.data);
                msgSuccess(commit, "Successfully retrieved doctors");
            } catch (error) {
                msgError(commit, error.response ? error.response.data.message : error.message);
            } finally {
            }
        },        
        async getDoctorAvailableSlots({commit}, payload){
            const clinicID = payload.clinicID;
            const data = {
                "clinicID": "clinic1",
                "date": "2024-03-29",
                "doctorDesc": "Experienced General Practitioner",
                "doctorEmail": "doc1@example.com",
                "doctorID": "doctor1",
                "doctorName": "Dr. Alice Jones",
                "password": "pass1",
                "schedule": [
                    {
                        "clinicID": "clinic1",
                        "date": "Fri, 29 Mar 2024 00:00:00 GMT",
                        "doctorID": "doctor1",
                        "id": "84c7486d-0329-4565-8a13-6391e1b41d5c",
                        "reason": "leave",
                        "slotNo": 1
                    },
                    {
                        "bookingID": "156f66ab-4ac3-492f-b86c-3bbcd81e69c2",
                        "bookingStatus": "confirmed",
                        "clinicID": "clinic1",
                        "date": "Fri, 29 Mar 2024 00:00:00 GMT",
                        "doctorID": "doctor1",
                        "patientID": "123",
                        "slotNo": 2
                    }
                ],
                "specialty": "General Practice"
            }
            const url = "`http://localhost:9999?doctorID=${payload.doctorID}&clinicID=${payload.clinicID}&date=${payload.date}`"
            try {
                await axios.get(`api/profile/doctor/view?clinicID=${clinicID}`)
                    .then(response => {
                        commit("setBookedSlots", data);
                        msgSuccess(commit, "Successfully retrieved doctor's appointment");
                    })
                    .catch(error => {
                        // Handle login failure here (e.g., show error message)
                    });
                } 
            finally {
            }
        },
        async createAppointment({commit}, payload) {
            commit("notificationModule/setLoading", true, { root: true });
            try {
                await axios.get('https://5sv31llj-5002.asse.devtunnels.ms/')
                    .then(response => {
                        console.log(response)
                        //commit("setDoctors", response.data);
                        commit("notificationModule/setLoading", false, { root: true });
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