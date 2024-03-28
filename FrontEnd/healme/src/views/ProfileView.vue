<template>
    <v-container max-width="1000">
        <v-card class="ma-7 pa-2 mx-auto" elevation="3" max-width="1000">
            <v-card-title class="justify-center align-center">
                <v-row class="fill-height" align="center" justify="center">
                    <v-col class="text-center">
                        <h1 class="font-weight-bold text-h3">Welcome Back</h1>
                        <h1 class="font-weight-bold text-h3 text-red-darken-1">
                            {{ this.userDetails.patientId }}
                        </h1>
                    </v-col>
                </v-row>
            </v-card-title>
            <v-tabs v-model="tab" color="red-darken-1" grow>
                <v-tab value="upcomingAppointments">
                    <v-icon start> mdi-domain </v-icon> Upcoming Appointments
                </v-tab>
                <v-tab value="completedAppointment">
                    <v-icon start> mdi-access-point </v-icon> Completed Appointments
                </v-tab>
                <v-tab value="ratingsGiven">
                    <v-icon start> mdi-access-point </v-icon> Review Givens
                </v-tab>
            </v-tabs>
            <v-window v-model="tab">
                <v-window-item value="upcomingAppointments">
                    <v-container>
                        <v-text-field v-model="searchUpcomingAppointmentByLocation" append-icon="mdi-magnify" label="Search" single-line hide-details ></v-text-field>
                        <v-tabs color="red-darken-1" v-model="currentFilter" centered grow>
                            <v-tab value="Upcoming">All</v-tab>
                        </v-tabs>
                        <br />
                        <h2 class="text-red-darken-1 centered" align="center">
                            Showing: {{ filteredUpcomingAppointment.length }} created appointments
                        </h2>
                        <br />
                        <v-container fill-height fluid lign-center v-if="filteredUpcomingAppointment.length == 0">
                            <v-row align="center" justify="center">
                                <v-col cols="12" class="text-center">
                                    <h3 class="mb-4" style="color: red">
                                        Wow no appointment found
                                    </h3>
                                    <p class="subtitle-1" style="color: grey">
                                        Maybe you would like to create an appointment?
                                    </p>
                                    <v-img class="mx-auto" cover :width="500" src="../assets/appointmentImages/noEvent.jpg" ></v-img>
                                    <v-btn class="mt-4" large color="red lighten-1" dark to="/bookAppointment" >Create Appointment</v-btn >
                                </v-col>
                            </v-row>
                        </v-container>
                        <v-card v-for="appointment in filteredUpcomingAppointment" class="mt-4" >
                            <router-link :to="{ name: 'appointment', params: { id: appointment.id } }" style="text-decoration: none; color: inherit" >
                                <div class="d-flex flex-no-wrap justify-space-between" >
                                    <v-row class="justify-space-between">
                                        <v-col cols="8" lg="8" md="8" sm="6" xs="6" >
                                            <div>
                                                <v-card-title class="text-h5 text-red-darken-1" >
                                                    Appointment Date: {{ appointment.date }}
                                                </v-card-title>
                                                <v-card-subtitle>
                                                    <v-icon >mdi-map-marker</v-icon >
                                                    Clinic: 
                                                    {{ appointment.clinicLocation }}
                                                </v-card-subtitle>
                                                    Doctor:
                                                    {{ appointment.doctorName }}
                                                <v-card-actions>
                                                    <v-btn color="red-darken-1" @click.prevent @click.stop="CancelAppointment(appointment)">Button</v-btn >
                                                </v-card-actions>
                                            </div>
                                        </v-col>
                                    </v-row>
                                </div>
                            </router-link>
                        </v-card>
                    </v-container>
                </v-window-item>
            </v-window>
        </v-card>
    </v-container>
    <div style="margin-bottom: 50px"></div>
</template>

<script>
    import moment from "moment";

    import { useStore, mapGetters, mapActions, mapState } from "vuex";
    import { computed, mounted } from "vue";
    export default {
        data() {
            return {
                upcomingAppointments: [
                    { id: 1, timeslot: '7:30', date: new Date(Date.now()+86400000), doctorName:"Marcus Yap", clinicName: "Alljuined Medical", clinicLocation:"389 Upper Aljunied Rd, SG367874"},
                    { id: 2, timeslot: '7:30', date: new Date(Date.now()+86400000 * 2), doctorName:"Data", clinicName: "Alljuined Medical", clinicLocation:"389 Upper Aljunied Rd, SG367874"},
                    { id: 3, timeslot: '7:30', date: new Date(Date.now()+86400000 * 2), doctorName:"Last", clinicName: "Alljuined Medical", clinicLocation:"389 Upper Aljunied Rd, SG367874"},
                ],
                tab: "option-1",
                currentFilter: "all",
                moment,
                searchCompletedEvent: "",
                searchUpcomingAppointmentByLocation: "",
            };
        },
        mounted() {
            // created by
            const queryGiven = ["createdBy", "==", this.userDetails.patientId];
            let bookMarkappointmentsId = this.userDetails.savedappointments;
        },
        computed: {
            ...mapGetters({
                userAppointments: "appointment/getUserAppointment",
                userDetails: "authModule/getUserDetails"
            }),
            filteredUpcomingAppointment() {
                let result = this.upcomingAppointments;
                switch (this.currentFilter) {
                    case "Upcoming":
                        result = result.sort(
                            (a, b) =>
                                new Date(a.date) - new Date(b.date)
                        );
                        break;
                }
                if (this.searchUpcomingAppointmentByLocation) {
                    result = result.filter((appointment) =>
                        appointment.clinicLocation.toLowerCase().includes(this.searchUpcomingAppointmentByLocation.toLowerCase())
                    );
                }
                return result;
            },

        },
        methods: {
        }
    };
</script>
