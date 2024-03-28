import axios from 'axios';
import router from "../../router";
import { msgError, msgSuccess } from "../../Tools/tools";

const ratingsModule = {
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
        
    }
};

export default ratingsModule;
