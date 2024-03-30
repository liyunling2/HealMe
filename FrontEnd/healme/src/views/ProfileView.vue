<template>
    <v-container max-width="1000">
        <v-card class="ma-7 pa-2 mx-auto" elevation="3" max-width="800">
            <v-card-title class="justify-center align-center">
                <v-row class="fill-height" align="center" justify="center">
                    <v-col class="text-center">
                        <h1 class="font-weight-bold text-h3">Welcome Back</h1>
                        <h1 class="font-weight-bold text-h3 text-blue-lighten-1">
                            {{ this.userDetails.name }}
                        </h1>
                    </v-col>
                </v-row>
            </v-card-title>
            <v-tabs v-model="tab" color="blue-lighten-1" grow>
                <v-tab value="upcomingAppointments">
                    <v-icon start> mdi-domain </v-icon> Upcoming Appointments
                </v-tab>
                <v-tab value="completedAppointments">
                    <v-icon start> mdi-access-point </v-icon> Completed Appointments
                </v-tab>
                <v-tab value="reviewGiven" v-if="isPatient">
                    <v-icon start> mdi-access-point </v-icon> Review Givens
                </v-tab>
                <v-tab value="reviewReceived" v-if="isDoctor">
                    <v-icon start> mdi-access-point </v-icon> Review Received
                </v-tab>
            </v-tabs>
            <v-window v-model="tab">
                <v-window-item value="upcomingAppointments">
                    <v-container>
                        <v-text-field v-model="searchUpcomingAppointment" append-icon="mdi-magnify" label="Search Appointment By Date, Clinic, Location or Doctor" single-line hide-details ></v-text-field>
                        <br />
                        <h2 class="text-blue-darken-1 centered" align="center">
                            Showing: {{ filteredUpcomingAppointment.length }} appointments
                        </h2>
                        <v-container fill-height fluid lign-center v-if="filteredUpcomingAppointment.length == 0 && isPatient">
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
                        <v-container fill-height fluid lign-center v-if="filteredUpcomingAppointment.length == 0 && isDoctor">
                            <v-row align="center" justify="center">
                                <v-col cols="12" class="text-center">
                                    <h3 class="mb-4" style="color: primary">
                                        Wow you have no upcoming appointments!
                                    </h3>
                                    <p class="subtitle-1" style="color: grey">
                                        GOOD JOB YOU'VE CLEARED ALL APPOINTMENT TAKE A BREAK 
                                    </p>
                                    <v-img class="mx-auto" cover :width="500" src="../assets/appointmentImages/takeABreak.jpg" ></v-img>
                                </v-col>
                            </v-row>
                        </v-container>
                        <v-card v-for="appointment in filteredUpcomingAppointment" class="mt-2">
                            <v-card-item>
                                <div>
                                <div class="text-overline mb-1">
                                    Appointment
                                </div>
                                <v-divider></v-divider>
                                <div class="text-h6 mb-1">
                                    <v-icon small class="mr-2">mdi-calendar</v-icon>
                                    {{ moment(appointment.date).format("YYYY-MMM-DD")}}
                                    {{ getTimeFromSlotNo(appointment.slotNo)}}
                                        Status: {{appointment.bookingStatus}}
                                </div>
                                <v-divider></v-divider>
                                <v-list-item two-line>
                                    <v-list-item-title>Clinic Details</v-list-item-title>
                                    <v-list-item-subtitle>
                                    <v-icon small class="mr-2">mdi-map-marker</v-icon>
                                    Clinic: {{ appointment.clinicName }}
                                    </v-list-item-subtitle>
                                    <v-list-item-subtitle>
                                    <v-icon small class="mr-2">mdi-city</v-icon>
                                    Location: {{ appointment.clinicLocation }}
                                    </v-list-item-subtitle>
                                    <v-list-item-title>Doctor Details</v-list-item-title>
                                    <v-list-item-subtitle>
                                    <v-icon small class="mr-2">mdi-account</v-icon>
                                    Selected Doctor: {{ appointment.doctorName }}
                                    </v-list-item-subtitle>
                                    <v-list-item-subtitle>
                                    <v-icon small class="mr-2">mdi-stethoscope</v-icon>
                                    Doctor Specialty: {{ appointment.doctorSpecialty }}
                                    </v-list-item-subtitle>
                                </v-list-item>
                            </div>
                            </v-card-item>
                            <v-divider></v-divider>
                                <v-card-actions>
                                    <v-btn color="blue-lighten-1" @click="openDeleteDialog(appointment)">Cancel Appointment</v-btn>
                                    <v-btn color="blue-lighten-1" variant="flat" prepend-icon="mdi-pencil" v-if="isDoctor" @click="openUpdateDialog(appointment)">Update Appointment </v-btn>
                                </v-card-actions>
                        </v-card>
                    </v-container>
                </v-window-item>
                <v-window-item value="completedAppointments">
                    <v-container>
                        <v-text-field v-model="searchCompletedAppointment" append-icon="mdi-magnify" label="Search Appointment By Date, Clinic, Location or Doctor" single-line hide-details ></v-text-field>
                        <br />
                        <h2 class="text-blue-darken-1 centered" align="center">
                            Showing: {{ filteredCompletedAppointment.length }} appointments
                        </h2>
                        <br />
                        <v-container fill-height fluid lign-center v-if="filteredCompletedAppointment.length == 0 && isDoctor">
                            <v-row align="center" justify="center">
                                <v-col cols="12" class="text-center">
                                    <h3 class="mb-4" style="color: primary">
                                        Wow no completed appointment found
                                    </h3>
                                    <p class="subtitle-1" style="color: grey">
                                        Maybe you would like clear complete some appointments?
                                    </p>
                                    <v-img class="mx-auto" cover :width="500" src="../assets/appointmentImages/noEvent.jpg" ></v-img>
                                    <v-btn class="mt-4" large color="blue-lighten-1" dark @click="changeCompleteTab('upcomingAppointments')" >Clear Appointments</v-btn >
                                </v-col>
                            </v-row>
                        </v-container>
                        <v-container fill-height fluid lign-center v-if="filteredCompletedAppointment.length == 0 && isPatient">
                            <v-row align="center" justify="center">
                                <v-col cols="12" class="text-center">
                                    <h3 class="mb-4" style="color: red">
                                        Wow no appointment found
                                    </h3>
                                    <p class="subtitle-1" style="color: grey">
                                        Maybe you would like to create an appointment?
                                    </p>
                                    <v-img class="mx-auto" cover :width="500" src="../assets/appointmentImages/noEvent.jpg" ></v-img>
                                    <v-btn class="mt-4" large color="red lighten-1" dark to="/bookAppointment" >Clear Appointment</v-btn >
                                </v-col>
                            </v-row>
                        </v-container>
                        <v-card v-for="appointment in filteredCompletedAppointment" class="mt-2">
                            <v-card-item>
                                <div>
                                <div class="text-overline mb-1">
                                    Appointment
                                </div>
                                <div class="text-h6 mb-1">
                                    <v-icon small class="mr-2">mdi-calendar</v-icon>
                                    {{ moment(appointment.date).format("YYYY-MMM-DD")}}
                                    {{ getTimeFromSlotNo(appointment.slotNo)}}
                                    <br>
                                    Status: {{appointment.bookingStatus}}
                                </div>
                                <v-list-item two-line>
                                    <v-list-item-title>Clinic Details</v-list-item-title>
                                    <v-list-item-subtitle>
                                    <v-icon small class="mr-2">mdi-map-marker</v-icon>
                                    Clinic: {{ appointment.clinicName }}
                                    </v-list-item-subtitle>
                                    <v-list-item-subtitle>
                                    <v-icon small class="mr-2">mdi-city</v-icon>
                                    Location: {{ appointment.clinicLocation }}
                                    </v-list-item-subtitle>
                                    <v-list-item-title>Doctor Details</v-list-item-title>
                                    <v-list-item-subtitle>
                                    <v-icon small class="mr-2">mdi-account</v-icon>
                                    Selected Doctor: {{ appointment.doctorName }}
                                    </v-list-item-subtitle>
                                    <v-list-item-subtitle>
                                    <v-icon small class="mr-2">mdi-stethoscope</v-icon>
                                    Doctor Specialty: {{ appointment.doctorSpecialty }}
                                    </v-list-item-subtitle>
                                </v-list-item>
                            </div>
                            </v-card-item>
                                <v-card-actions v-if="isPatient">
                                    <v-btn variant="flat" prepend-icon="mdi-delete" color="blue-lighten-1" @click="openReviewDialog(appointment)">Give Review </v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-container>
                </v-window-item>
                <v-window-item value="reviewGiven" v-if="isPatient">
                    <v-container>
                        <v-text-field v-model="searchReviewGiven" append-icon="mdi-magnify" label="Search Review By Date, Clinic, Location or Doctor" single-line hide-details ></v-text-field>
                        <br />
                        <h2 class="text-blue-darken-1 centered" align="center">
                            Showing: {{ filteredReviews.length }} Ratings
                        </h2>
                        <br />
                        <v-container fill-height fluid lign-center v-if="filteredReviews.length == 0">
                            <v-row align="center" justify="center">
                                <v-col cols="12" class="text-center">
                                    <h3 class="mb-4" style="color: red">
                                        Wow no ratings found
                                    </h3>
                                    <p class="subtitle-1" style="color: grey">
                                        Maybe you would like to give feedback to your completed  ?
                                    </p>
                                    <v-img class="mx-auto" cover :width="500" src="../assets/appointmentImages/noEvent.jpg" ></v-img>
                                    <v-btn class="mt-4" large color="red lighten-1" @click="changeCompleteTab()">Give Feedback</v-btn>
                                </v-col>
                            </v-row>
                        </v-container>
                        <v-container>
                            <v-card v-for="review in filteredReviews" class="mt-2" prepend-icon="mdi-comment-text" title="Review">
                                <v-card-text class="text-h5 py-2">
                                    "{{review.comments}}"
                                </v-card-text>
                                <v-rating v-model=review.ratingGiven half-increments readonly></v-rating>
                                <v-card-text>
                                    <v-icon small class="mr-2">mdi-hospital-building</v-icon>
                                    Clinic: name {{ review.clinicID }}
                                    <br>
                                    <v-icon small class="mr-2">mdi-doctor</v-icon>
                                    doctor: Name {{ review.clinicID }}
                                    <br>
                                    <v-icon small class="mr-2">mdi-calendar</v-icon>
                                    Reviewed On: {{ review.timeStamp }} by {{ review.patientName }}
                                    <br>
                                </v-card-text>
                            </v-card>
                        </v-container>
                    </v-container>
                </v-window-item>
                <v-window-item value="reviewReceived" v-if="isDoctor">
                    <v-container>
                        <v-text-field v-model="searchReviewGiven" append-icon="mdi-magnify" label="Search Review By Date, Clinic, Location or Doctor" single-line hide-details ></v-text-field>
                        <br />
                        <h2 class="text-blue-darken-1 centered" align="center">
                            Showing: {{ filteredReviews.length }} Ratings
                        </h2>
                        <br />
                        <v-container fill-height fluid lign-center v-if="filteredReviews.length == 0 & isPatient">
                            <v-row align="center" justify="center">
                                <v-col cols="12" class="text-center">
                                    <h3 class="mb-4" style="color: red">
                                        Wow no ratings found
                                    </h3>
                                    <p class="subtitle-1" style="color: grey">
                                        Maybe you would like to give feedback to your completed appointments?
                                    </p>
                                    <v-img class="mx-auto" cover :width="500" src="../assets/appointmentImages/noEvent.jpg" ></v-img>
                                    <v-btn class="mt-4" large color="red lighten-1" @click="changeCompleteTab('completedAppointments')">Clear Appointments</v-btn>
                                </v-col>
                            </v-row>
                        </v-container>
                        <v-container>
                            <v-card v-for="review in filteredReviews" class="mt-2" prepend-icon="mdi-comment-text" title="Review">
                                <v-card-text class="text-h5 py-2">
                                    "{{review.comments}}"
                                </v-card-text>
                                <v-rating v-model=review.ratingGiven half-increments readonly></v-rating>
                                <v-card-text>
                                    <v-icon small class="mr-2">mdi-hospital-building</v-icon>
                                    Clinic: name {{ review.clinicID }}
                                    <br>
                                    <v-icon small class="mr-2">mdi-doctor</v-icon>
                                    doctor: Name {{ review.clinicID }}
                                    <br>
                                    <v-icon small class="mr-2">mdi-calendar</v-icon>
                                    Reviewed On: {{ review.timeStamp }} by {{ review.patientName }}
                                    <br>
                                </v-card-text>
                            </v-card>
                        </v-container>
                    </v-container>
                </v-window-item>
            </v-window>
        </v-card>
    </v-container>
    <div v-if="isDataRetrieving" class="overlay">
      <v-progress-circular
        color="primary"
        indeterminate
        size="64"
        class="loader"
      ></v-progress-circular>
    </div>
    <v-dialog v-model="deleteDialogVisible" width="auto">
      <v-card class="mx-auto pa-6 elevated-3" style="border-radius: 20px">
        <v-card-title class="text-center text-h3 text-blue-lighten-1 font-weight-bold">Cancel Appointment?</v-card-title>
        <v-card-text class="text-center text-h6 font-weight-light">
          This action is not irreversible. Are you sure you want to cancel the appointment?
        </v-card-text>
        <v-card-actions class="justify-center">
          <v-btn size="large" variant="elevated" @click="deleteDialogVisible = false">No</v-btn>
          <v-btn size="large" color="blue-lighten-1" variant="elevated" @click="deleteAppointment(currentAppointment)">Yes</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="updateDialogVisible" width="auto">
      <v-card class="mx-auto pa-6 elevated-3" style="border-radius: 20px">
        <v-card-title class="text-center text-h3 text-blue-lighten-1 font-weight-bold">Cancel Appointment?</v-card-title>
        <v-card-text class="text-center text-h6 font-weight-light">
          This action is not irreversible. Are you sure you want to cancel the appointment?
        </v-card-text>
        <v-card-actions class="justify-center">
          <v-btn size="large" variant="elevated" @click="updateDialogVisible = false">No</v-btn>
          <v-btn size="large" color="blue-lighten-1" variant="elevated" @click="updateAppointment(currentAppointment)">Yes</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="reviewDialog" width="auto" >
        <v-form>
            <v-card max-width="550px" class="mx-auto pa-6 elevated-3" style="border-radius: 20px" >
                <v-card-title class="text-center text-h3 text-blue-lighten-1 font-weight-bold" >Leave a review for</v-card-title>
                <v-card-title class="text-center text-h4 text-blue-lighten-1 font-weight-bold" >Dr {{ reviewDoc.doctorName }}</v-card-title>
                <v-card-text>
                    <span class="subtitle-1">Rate him!</span>
                    <br>
                    <div class="full-width-rating">
                        <v-rating v-model="ratingGiven" half-increments hover :item-labels="['Poor', '', '', '', 'Excellent']" item-label-position="top" ></v-rating>
                    </div>
                    <!-- <v-rating v-model="ratingGiven" width="50%" half-increments hover :item-labels="['Poor', '', '', '', 'Excellent']" class="ma-2" item-label-position="top"></v-rating> -->
                    <v-textarea v-model="comment" label="Your Review" outlined rows="3" auto-grow ></v-textarea>
                </v-card-text>
                <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn :disabled="!isReviewValid" color="primary" @click="submitReview(appointment)">Submit</v-btn>
                </v-card-actions>
            </v-card>
        </v-form>
    </v-dialog>
</template>

<script>
    import moment from "moment";
    import { msgError, msgSuccess } from "../Tools/tools";

    import { useStore, mapGetters, mapActions, mapState } from "vuex";
    import { computed, mounted } from "vue";
    import axios from "axios";
    export default {
        data() {
            return {
                ratingGiven: 0, // Initial rating
                comment: '', // Initial review text
                deleteDialogVisible: false,
                currentAppointment: "", // Holds the appointment to delete
                reviewDoc: { doctorName : ""},                
                updateDialogVisible: false,
                reviewDialog: false,
                isDataRetrieving:true,
                tab: "option-1",
                currentFilter: "all",
                moment,
                searchCompletedAppointment: "",
                searchUpcomingAppointment: "",
                searchReviewGiven: "",
            };
        },
        created(){            
        },
        computed: {
            ...mapGetters({
                userAppointments: "appointmentModule/getUserAppointments",
                userDetails: "authModule/getUserDetails",
                userRatings: "appointmentModule/getRatings",
                isDoctor: "authModule/ifDoctor",
                isPatient: "authModule/ifPatient"
            }),
            isReviewValid() {
                return this.ratingGiven > 0 && this.comment.trim() !== '';
            },
            filteredUpcomingAppointment() {
                let result = this.userAppointments.filter(appointment => appointment.bookingStatus === "Confirmed");
                if (this.searchUpcomingAppointment) {
                    result = result.filter((appointment) =>
                        appointment.clinicLocation.toLowerCase().includes(this.searchUpcomingAppointment.toLowerCase()) ||
                        appointment.doctorName.toLowerCase().includes(this.searchUpcomingAppointment.toLowerCase()) ||
                        appointment.clinicName.toLowerCase().includes(this.searchUpcomingAppointment.toLowerCase()) ||
                        appointment.date.toLowerCase().includes(this.searchUpcomingAppointment.toLowerCase())
                    );
                }
                return result;
            },
            filteredCompletedAppointment() {
                let result = this.userAppointments.filter(appointment => appointment.bookingStatus === "Completed");
                if (this.searchCompletedAppointment) {
                    result = result.filter((appointment) =>
                        appointment.clinicLocation.toLowerCase().includes(this.searchCompletedAppointment.toLowerCase()) ||
                        appointment.doctorName.toLowerCase().includes(this.searchCompletedAppointment.toLowerCase()) ||
                        appointment.clinicName.toLowerCase().includes(this.searchCompletedAppointment.toLowerCase()) ||
                        appointment.date.toLowerCase().includes(this.searchCompletedAppointment.toLowerCase())
                    );
                }
                return result;
            },
            filteredReviews() {
                let result = this.userRatings
                if (this.searchReviewGiven) {
                    result = result.filter((appointment) =>
                        appointment.bookingID.toLowerCase().includes(this.searchReviewGiven.toLowerCase()) 
                        // ||
                        // appointment.doctorName.toLowerCase().includes(this.searchUpcomingAppointment.toLowerCase()) ||
                        // appointment.clinicName.toLowerCase().includes(this.searchUpcomingAppointment.toLowerCase()) ||
                        // appointment.date.toLowerCase().includes(this.searchUpcomingAppointment.toLowerCase())
                    );
                }
                return result;
            }
        },
        async mounted() {
            await this.getAppointments()
            await this.getReviews()
        },
        methods: {
            openDeleteDialog(appointment) {
                this.currentAppointment = appointment;
                this.deleteDialogVisible = true;
            },
            openUpdateDialog(appointment) {
                this.currentAppointment = appointment;
                this.updateDialogVisible = true;
            },
            openReviewDialog(appointment) {
                this.reviewDoc = appointment;
                this.reviewDialog = true;
            },
            enhancePayload(originalPayload) {
                var requestType = ""
                if (this.isDoctor) {
                    requestType = "doctor";
                } else if (this.isPatient) {
                    requestType = "patient";
                }
                return {
                    request: requestType,
                    data: originalPayload
                };
            },
            async getAppointments() {
                this.isDataRetrieving = true;
                var payload = {
                    givenId: this.userDetails.id,
                }
                payload = this.enhancePayload(payload)
                await this.$store.dispatch("appointmentModule/getAllUserAppointments", payload)
                this.isDataRetrieving = false;
            },
            async getReviews() {
                this.isDataRetrieving = true;
                var payload = {
                    givenId: this.userDetails.id,
                }
                payload = this.enhancePayload(payload)
                await this.$store.dispatch("appointmentModule/getAllUserReview", payload)
                this.isDataRetrieving = false;
            },
            changeCompleteTab(newTab) {
                this.tab = newTab
            },
            getTimeFromSlotNo(slotNo) {
                const baseTime = new Date('2024-01-20T07:00:00');
                baseTime.setMinutes(baseTime.getMinutes() + (slotNo - 1) * 30);
                const hours = baseTime.getHours();
                const minutes = baseTime.getMinutes();
                const isPM = hours >= 12;
                const isNoon = hours === 12 && minutes === 0;
                let formattedTime = "";
                if (isNoon) { // Special case for exactly 12:00
                    formattedTime = "12:00 PMP";
                } else if (isPM) {
                    const adjustedHours = hours > 12 ? hours - 12 : hours; // Convert 24h to 12h format
                    formattedTime = `${adjustedHours}:${minutes.toString().padStart(2, '0')} PM`;
                } else {
                    formattedTime = `${hours}:${minutes.toString().padStart(2, '0')} AM`;
                }
                return formattedTime;
            },
            async deleteAppointment(appointment) {
                this.deleteDialogVisible = false;
                this.isDataRetrieving = true;
                var payload = {
                    appointmentID: appointment.bookingID,
                }
                payload = this.enhancePayload(payload)
                await this.$store.dispatch("appointmentModule/deleteAppointment", payload)
                await this.getAppointments();
                this.isDataRetrieving = false;
                this.currentAppointment = null;

            },
            async updateAppointment(appointment) {
                this.updateDialogVisible = false;
                this.isDataRetrieving = true;
                appointment.bookingStatus = "Completed"
                await this.$store.dispatch("appointmentModule/editAppointment", appointment)
                this.isDataRetrieving = false;
            },
            async submitReview(appointment) {
                const reviewGiven = {
                    clinicID: this.reviewDoc.clinicID,
                    doctorName: this.reviewDoc.doctorName,
                    clinicName: this.reviewDoc.clinicName,
                    patientName: this.reviewDoc.patientName,
                    bookingDate: moment(new Date()).format("YYYY-MM-DD"),
                    patientID: this.reviewDoc.patientID,
                    bookingID: this.reviewDoc.bookingID,
                    ratingGiven: this.ratingGiven,
                    comments: this.comment,
                }
                this.isDataRetrieving = true;
                await this.$store.dispatch("appointmentModule/createReview", reviewGiven)
                this.ratingGiven = 0;
                this.comment = '';
                this.reviewDoc = { doctorName : ""}
                this.isDataRetrieving = false;
                this.reviewDialog = false
                this.changeCompleteTab("reviewGiven")
            },
        },
        watch: {
            async tab(newValue) {
                if (newValue === 'reviewGiven') {
                    this.getReviews()
                }
            }
        },
    };
</script>



<style>
.padded-list-item {
  margin: 10px 0; /* You can adjust the value to suit your needs */
}
.loader-position {
  position: fixed;
  left: 20px;
  bottom: 20px;
  z-index: 1000; /* Ensure it's above other content */
}

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(255, 255, 255, 0.5); /* Semi-transparent white background */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000000000000; /* Ensure it's above other content */
}

.full-width-rating .v-rating {
  width: 100%; /* Force the rating component to full width */
  display: flex;
  justify-content: space-evenly; /* Evenly distribute the stars */
}
.full-width-rating .v-rating .v-icon {
  flex-grow: 1; /* Allows the stars to grow and take up equal space */
}
</style>
