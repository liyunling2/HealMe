<template>
  <v-app>
    <v-main>
        <Navbar />
        <router-view v-if="!isLoading"/>
        <div v-else>
            <appLoader />
        </div>
    </v-main>
  </v-app>
</template>

<script>
    import { onMounted } from "vue";
    import { useStore, mapGetters, mapActions, mapState } from "vuex";
    import Navbar from "./components/NavBar.vue";
    import appLoader from "./components/utils/loader.vue";
    import router from "./router/";
    export default {
        name: "App",
        components: {
            Navbar,
            appLoader
        },
        created(){
            this.checkLogin()
        },
        mounted() {
        },
        computed: {
          ...mapGetters({
              toastMsg: "notificationModule/getToastMsg",
              isLoading: "notificationModule/isLoading",
          })
        },
        watch: {
            toastMsg(toastMsg) {
                if (toastMsg[0] === true) {
                    if (toastMsg[2] === "error") {
                        this.$toast.error(toastMsg[1]);
                    }
                    if (toastMsg[2] === "success") {
                        this.$toast.success(toastMsg[1]);
                    }
                }
            }
        },
        methods: {
            checkLogin() {
                const userData = JSON.parse(localStorage.getItem('userData'));
                if(userData !== null) {
                    this.$store.commit("authModule/setUser", userData);
                    if (userData.authType == "user") {
                        this.$store.commit("authModule/setPatientAuth", true);
                    } else if(userData.authType == "doctor") {
                        this.$store.commit("authModule/setDoctorAuth", true);
                    }
                    router.push('/profile');
                }
            }
        },
        data: () => ({
        })
    };
</script>

<style>
</style>