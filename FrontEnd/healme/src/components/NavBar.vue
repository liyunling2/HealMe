<template>
    <v-app-bar :elevation="2" class="text-indigo-darken-2 mb-3">
        <v-toolbar-title style="cursor: pointer">
            <router-link style="text-decoration: none; color: inherit" to="/">
                <span class="font-weight-bold text-h6"> HEALME </span>
            </router-link>
        </v-toolbar-title>
        <span class="hidden-lg-and-up">
            <v-app-bar-nav-icon @click="sidebar = !sidebar">
            </v-app-bar-nav-icon>
        </span>
        <v-toolbar-items class="hidden-md-and-down align-center">
            <v-btn to="/appointment/123" v-if="isAuth">
                <v-icon left dark>mdi-calendar-plus</v-icon>
                <span class="ms-1.5"> VIEW UPCOMING APPOINTMENTS </span>
            </v-btn>
            <v-btn to="/bookAppointment" v-if="isAuth">
                <v-icon left dark>mdi-calendar-plus</v-icon>
                <span class="ms-1.5"> BOOK AN APPOINTMENT </span>
            </v-btn>
            <v-btn to="/profile" v-if="isAuth">
                <v-icon left dark>mdi-account</v-icon>
                <span class="ms-1.5"> View Profile </span>
            </v-btn>
            <v-btn @click="logoutUser" v-if="isAuth">
                <v-icon left dark>mdi-logout</v-icon>
                <span class="ms-1.5"> Logout </span>
            </v-btn>
            <v-btn to="/login" v-if="!isAuth">
                <v-icon left dark>mdi-account</v-icon>
                <span class="ms-1.5"> Login </span>
            </v-btn>
            <v-btn to="/signup" v-if="!isAuth">
                <v-icon left dark>mdi-arrow-up-bold-box-outline</v-icon>
                <span class="ms-1.5"> Sign Up </span>
            </v-btn>
        </v-toolbar-items>
    </v-app-bar>

    <v-navigation-drawer disable-resize-watcher class="text-indigo-darken-2 d-lg-none d-xl-none d-xxl-none hidden-lg-and-up" v-model="sidebar" >
        <v-list>
            <v-list-item link to="/profile" v-if="isAuth">
                <v-icon left dark>mdi-account</v-icon>
                <span class="ms-1.5"> View Profile </span>
            </v-list-item>
            <v-list-item to="/viewAppointment" v-if="isAuth">
                <v-icon left dark>mdi-calendar-plus</v-icon>
                <span class="ms-1.5"> VIEW UPCOMING APPOINTMENT</span>
            </v-list-item>
            <v-list-item to="/bookAppointment" v-if="isAuth">
                <v-icon left dark>mdi-calendar-plus</v-icon>
                <span class="ms-1.5"> BOOK AN APPOINTMENT </span>
            </v-list-item>
            <v-list-item @click="logoutUser" v-if="isAuth">
                <v-icon left dark>mdi-logout</v-icon>
                <span class="ms-1.5"> Logout </span>
            </v-list-item>
            <v-list-item link to="/login" v-if="!isAuth">
                <v-icon left dark>mdi-account</v-icon>
                <span class="ms-1.5"> Login </span>
            </v-list-item>
            <v-list-item link to="/signup" v-if="!isAuth">
                <v-icon left dark>mdi-arrow-up-bold-box-outline</v-icon>
                <span class="ms-1.5"> Sign Up </span>
            </v-list-item>
        </v-list>
    </v-navigation-drawer>
</template>

<script>
    //Import components
    import { useStore, mapGetters, mapActions, mapState } from "vuex";
    import { computed } from "vue";
    export default {
        data() {
            return {
                sidebar: false,
                group: null,
            };
        },
        components: {},
        computed: {
            ...mapGetters({
                isAuth: "authModule/isAuth",
                isAdmin: "authModule/isAdmin",
                userDetails: "authModule/getUserDetails"
            })
        },
        methods: {
            logoutUser() {
                this.$store.dispatch("authModule/signOut");
            }
        }
    };
</script>
