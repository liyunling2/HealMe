import axios from 'axios';
import router from "../../router";
import { msgError, msgSuccess } from "../../Tools/tools";

const authModule = {
    namespaced: true,
    state: {
        currentUser: [],
        auth: false,
        doctor: false,
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
        }
    },
    mutations: {
        setUser(state, payload) {
            state.user = payload
            state.auth = true;
        },
        setDoctor(state, payload) {
            state.user = payload
            state.auth = true;
            state.doctor = true;
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
                router.push("/login");
            } catch (error) {
                msgError(commit);
            }
        },
        async signIn({ commit }, payload) {
            console.log(payload);
            commit("notificationModule/setLoading", true, { root: true });
            try {
              const response = await axios.post('api/patient/login', payload);
              console.log(response.data.data);
              const userData = {
                contactNum: response.data.data.contactNum,
                email: response.data.data.contactEmail,
                patientID: response.data.data.patientID,
                patientName: response.data.data.patientName,
              };
              localStorage.setItem('userData', JSON.stringify(userData));
            commit("setUser", userData);
            msgSuccess(commit, "Successfully logged in");
            router.push("/");
            } catch (error) {
                msgError(commit, error.response.data.message);
            } finally {
                commit("notificationModule/setLoading", false, { root: true });
            }
          },
        async signUp({commit}, payload) {
            try {
                commit("notificationModule/setLoading", true, { root: true });
                axios.post('http://127.0.0.1:5006/login', {
                    email: payload.email,
                    password: payload.password
                    })
                    .then(response => {
                        const userData = {
                            contactNum: response.data.contactNum,
                            email: response.data.contactEmail,
                            patientID: response.data.contactID,
                            patientName: response.data.patientName,
                        }
                        commit("setUser", userData);
                        msgSuccess(commit, "Successfully logged in");
                        router.push("/")
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

export default authModule;
