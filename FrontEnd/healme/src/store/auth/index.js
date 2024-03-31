import axios from 'axios';
import router from "../../router";
import { msgError, msgSuccess } from "../../Tools/tools";

const authModule = {
    namespaced: true,
    state: {
        user: [],
        auth: false,
        doctor: false,
        patient: false,
    },
    getters: {
        getUserDetails(state) {
            return state.user;
        },
        isAuth(state) {
            if (state.auth) {
                return true;
            }
            return false;
        },
        ifDoctor(state){
            return state.doctor
        },
        ifPatient(state){
            return state.patient
        }
    },
    mutations: {
        setUser(state, payload) {
            state.user = payload
            state.auth = true;
        },
        setDoctorAuth(state, payload){
            state.doctor = payload
        },
        setPatientAuth(state, payload){
            state.patient = payload
        },
        setDoctor(state, payload) {
            state.user = payload
            state.auth = true;
        },
        clearUser(state) {
            state.user = {
                contactNum: "",
                email: "",
                patientID: 0,
                patientName: "",
            };

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
        async signOut({ commit }) {
            try {
                commit("clearUser");
                msgSuccess(commit, "Bye :)");
                localStorage.removeItem('userData'); // Remove user data from localStorage
                commit("setPatientAuth", false);
                commit("setDoctorAuth", false);
                router.push("/login");
            } catch (error) {
                msgError(commit);
            }
        },
        async userSignIn({ commit }, payload) {
            console.log(payload)
            commit("notificationModule/setLoading", true, { root: true });
            try {
              const response = await axios.post('api/patient/login', payload);
              console.log(response)
              const userData = {
                contactNum: response.data.data.contactNum,
                email: response.data.data.email,
                id: response.data.data.patientID,
                name: response.data.data.patientName,
                authType: "user",
              };
              localStorage.setItem('userData', JSON.stringify(userData));
            commit("setUser", userData);
            commit("setPatientAuth", true);
            msgSuccess(commit, "Successfully logged in");
            router.push("/profile");
            } catch (error) {
                msgError(commit, error.response.data.message);
            } finally {
                commit("notificationModule/setLoading", false, { root: true });
            }
        },
        async doctorSignIn({ commit }, payload) {
            commit("notificationModule/setLoading", true, { root: true });
            try {
              const response = await axios.post('api/doctor/login', payload);
              const userData = {
                contactNum: response.data.data.contactNum,
                email: response.data.data.email,
                id: response.data.data.doctorID,
                name: response.data.data.doctorName,
                clinicID: response.data.data.clinicID,
                authType: "doctor",
              };
              localStorage.setItem('userData', JSON.stringify(userData));
            commit("setUser", userData);
            commit("setDoctorAuth", true);
            msgSuccess(commit, "Successfully logged in");
            router.push("/profile");
            } catch (error) {
                msgError(commit, error.response.data.message);
            } finally {
                commit("notificationModule/setLoading", false, { root: true });
            }
        },
        async signUp({commit}, payload) {
            try {
                commit("notificationModule/setLoading", true, { root: true });
                await axios.post('/api/profile/patient/new', payload)
                    .then(response => {
                        const userData = {
                            contactNum: response.data.data.contactNum,
                            email: response.data.data.email,
                            id: response.data.data.patientID,
                            name: response.data.data.patientName,
                            authType: "user",
                        }
                        commit("setUser", userData);
                        msgSuccess(commit, "Successfully created account");
                        router.push("/profile")
                    })
                    .catch(error => {
                        console.error(error);
                        msgError(commit, error.response.data.message);
                    });
                } finally {
                    commit("notificationModule/setLoading", false, { root: true });
                }
        },
    }
};

export default authModule;
