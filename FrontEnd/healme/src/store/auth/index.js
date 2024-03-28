import axios from 'axios';
import router from "../../router";
import { msgError, msgSuccess } from "../../Tools/tools";

const authModule = {
    namespaced: true,
    state: {
        currentUser: [],
        auth: false,
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
    },
    mutations: {
        setUser(state, payload) {
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
                router.push("/login");
            } catch (error) {
                msgError(commit);
            }
        },
        async signIn({commit}, payload) {
            try {
                commit("notificationModule/setLoading", true, { root: true });
                // axios.post('http://127.0.0.1:5006/login', {
                //         email: payload.email,
                //         password: payload.password
                //     })

                axios.get('https://catfact.ninja/fact')
                    .then(response => {
                        // const userData = {
                        //     contactNum: response.data.contactNum,
                        //     email: response.data.contactEmail,
                        //     patientID: response.data.contactID,
                        //     patientName: response.data.patientName,
                        // }
                        const userData = {
                            contactNum: 12345,
                            email: "jialeso1227@gmail.com",
                            patientID: 123456,
                            patientName: "Jialeso",
                        }
                        localStorage.setItem('userData', JSON.stringify(userData));
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
