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
        bookedSlots: [],
        ratings: []
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
        },
        getUserAppointments(state){
            return state.userAppointments
        },
        getRatings(state) {
            return state.ratings;
        },
    },
    mutations: {
        setClinics(state, payload) {
            state.clinics = payload
        },
        setDoctors(state,payload) {
            state.clinicDoctors = payload
        },
        setUserAppointments(state,payload) {
            state.userAppointments = payload
        },
        setBookedSlots(state, payload) {
            state.bookedSlots = payload
        },
        setRatings(state,payload) {
            state.ratings = payload
        }
    },
    actions: {
        async getAllClinics({commit}, payload) {
            try {
                await axios.get('/api/clinic/view')
                    .then(response => {
                        commit("setClinics", response.data.data);
                        msgSuccess(commit, "Successfully retrieved all clinics");
                    })
            }
            catch (error) {
                msgError(commit, error.response.data.message);
            } finally {
                commit("notificationModule/setLoading", false, { root: true });
            }
        },
        async getAllDoctorsInClinic({ commit }, payload) {
            try {
                const clinicID = payload.clinicID;
                const response = await axios.get(`/api/profile/doctor/view?clinicID=${clinicID}`);
                var doctors = response.data.data
                var doctorsWithRating = []
                for (let i = 0; i < doctors.length; i++) {
                    var newDoctorProfile = doctors[i]
                    const newreponse = await axios.get(`/api/profile/doctor/rating/${newDoctorProfile.doctorID}`)
                    newDoctorProfile.ratings = newreponse.data.data.averageRating
                    doctorsWithRating.push(newDoctorProfile)
                }
                await commit("setDoctors", doctorsWithRating);
                msgSuccess(commit, response.data.message);
            } catch (error) {
                msgError(commit, error.response.data.message);
            } finally {
                commit("notificationModule/setLoading", false, { root: true });
            }
        },        
        async getDoctorAvailableSlots({commit}, payload){
            const clinicID = payload.clinicID;
            const url = `/api/profile/doctor/schedule?date=${payload.date}&doctorID=${payload.doctorID}&clinicID=${payload.clinicID}`
            try {
                await axios.get(url)
                    .then(response => {
                        commit("setBookedSlots", response.data.schedule);
                        msgSuccess(commit, "Successfully retrieved doctor's appointment");
                    })
            } 
            catch (error) {
                msgError(commit, error.response.data.message);
            } finally {
            }
        },
        async createAppointment({commit}, payload) {
            try {
                await axios.post('api/createBooking', payload)
                    .then(response => {
                        msgSuccess(commit, response.data.message);
                        router.push("/profile");
                    })  
                }  
            catch (error) {
                msgError(commit, error.response.data.message);
            } 
            finally {
                commit("notificationModule/setLoading", false, { root: true });
            }
        },
        async getAllUserAppointments({commit}, payload) {
            var url 
            if (payload.request == "patient") {
                url = `api/booking/view/?patientID=${payload.data.givenId}`
            } else if (payload.request == "doctor") {
                url = `/api/booking/view/?doctorID=${payload.data.givenId}`
            }
            try {
                await axios.get(url)
                    .then(response => {
                        commit("setUserAppointments", response.data.data);
                        msgSuccess(commit, "Retrieved user's appointment");
                    })
                    
                } 
            catch (error) {
                msgError(commit, error.response.data.message);
            } finally {

            }
        },
        async editAppointment({commit}, payload) {
            try {
                await axios.put(`/api/booking/complete/${payload.bookingID}`)
                    .then(response => {
                        msgSuccess(commit, response.data.message);
                        //commit("setDoctors", response.data);
                    })
            }     
            catch (error) {
                msgError(commit, error.response.data.message);
            } finally {

            }
        },
        async deleteAppointment({commit}, payload) {
            var url = `/api/booking/delete/?bookingID=${payload.data.appointmentID}`
            try {
                await axios.delete(url)
                    .then(response => {
                        msgSuccess(commit, response.data.message);
                    })
                }
            catch (error) {
                msgError(commit, error.response.data.message);
            } finally {
                
            }
        },
        async getAllUserReview({commit}, payload) {
            var url 
            if (payload.request == "patient") {
                url = `/api/rating?patientID=${payload.data.givenId}`
            } else if (payload.request == "doctor") {
                url = `/api/rating?doctorID=${payload.data.givenId}`
            }
            try {
                axios.get(url)
                    .then(response => {
                        commit("setRatings", response.data.data);
                        msgSuccess(commit, "Retrieve User's Rating Given");
                    })
            }
            catch (error) {
                msgError(commit, error.response.data.message);
            } finally {
                
            }
        },
        async createReview({commit}, payload) {
            const url = `/api/rating/new/${payload.doctorID}`
            try {
                await axios.post(url, payload)
                    .then(response => {
                        msgSuccess(commit, response.data.message);
                    })  
                }  
            catch (error) {
                msgError(commit, error.response.data.message);
            } 
            finally {
                commit("notificationModule/setLoading", false, { root: true });
            }
        }

        
    }
};


export default appointmentModule;