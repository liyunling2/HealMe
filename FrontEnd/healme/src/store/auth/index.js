import axios from 'axios';
import router from "../../router";
import { msgError, msgSuccess } from "../../Tools/tools";

const DEFAULT_USER = {
    uid: 123,
    email: "",
    firstName: "",
    lastName: "null",
};

const authModule = {
    namespaced: true,
    state: {
        currentUser: localStorage.getItem("currentUser"),
        
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
            console.log("payload", payload)
            state.user = payload
            state.auth = true;
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
        async signOut({ commit }) {
            try {
                commit("clearUser");
                msgSuccess(commit, "Bye :)");
                router.push("/login");
            } catch (error) {
                msgError(commit);
            }
        },
        async getUserProfile({ commit }, payload) {
            try {
                const docSnap = await getDoc(doc(db, "users", payload));
                if (docSnap.exists()) {
                    return docSnap.data();
                } else {
                    return null;
                }
            } catch (error) {
                msgError(commit);
                console.log();
            } finally {
            }
        },
        async signIn({commit}, payload) {
            try {
                commit("notificationModule/setLoading", true, { root: true });
                axios.post('http://127.0.0.1:5006/login', {
                    email: payload.email,
                    password: payload.password
                    })
                    .then(response => {
                        const userData = {
                            uid: 1245,
                            email: "",
                            firstName: "",
                            lastName: "null",
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
        async signUp({ commit }, payload) {
            try {
                const userCredential = await createUserWithEmailAndPassword(
                    auth,
                    payload.email,
                    payload.password
                );
                const newUser = {
                    uid: userCredential.user.uid,
                    email: userCredential.user.email,
                    firstName: payload.firstName,
                    lastName: payload.lastName,
                    displayPicture: payload.displayPicturePath,
                    savedIssues: [],
                    savedEvents: []
                };
                await setDoc(
                    doc(db, "users", userCredential.user.uid),
                    newUser
                );
                commit("setUser", newUser);
                msgSuccess(commit, "Welcome !!");
                router.push("/");
            } catch (error) {
                msgError(commit, fbErrors(error.code));
            }
        }      
    }
};

export default authModule;
