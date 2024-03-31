<template>
    <v-container max-width="1000">
        <v-card class="ma-7 pa-2 mx-auto" elevation="3" max-width="800">
            <v-card-title class="justify-center align-center">
                <v-row class="fill-height" align="center" justify="center">
                    <v-col class="text-center">
                        <h1 class="font-weight-bold text-h3">Welcome Back</h1>
                        <h1 class="font-weight-bold text-h3 text-blue-lighten-1" v-if="isPatient">
                            {{ this.userDetails.name }}
                        </h1>
                        <h1 class="font-weight-bold text-h3 text-blue-lighten-1" v-if="isDoctor">
                            Dr {{ this.userDetails.name }}
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
                <v-tab value="blockSlots" v-if="isDoctor">
                    <v-icon start> mdi-access-point </v-icon> Block Slot Created
                </v-tab>
                <v-tab value="reviewReceived" v-if="isDoctor">
                    <v-icon start> mdi-access-point </v-icon> Review Received
                </v-tab>
            </v-tabs>
            <v-window v-model="tab">
                <v-window-item value="upcomingAppointments">
                    <v-container>
                        <v-text-field v-model="searchUpcomingAppointment" append-icon="mdi-magnify" label="Search Appointment By Clinic, Location or Doctor" single-line hide-details ></v-text-field>
                        <br>
                        <v-btn @click="openDatePickerDialog = true" class="mb-4 mx-auto" align="center" color="blue lighten-1">
                            Filtering by date: {{ moment(this.blockslotDateFilter).format("YYYY-MMM-DD") }}
                        </v-btn>
                        <v-dialog v-model="openDatePickerDialog" width="290px" >
                            <v-date-picker v-model="blockslotDateFilter" :min="minDate" no-title></v-date-picker>
                        </v-dialog>
                        <br />
                        <h2 class="text-blue-darken-1 centered" align="center">
                            Showing: {{ filteredUpcomingAppointment.length }} upcoming appointments
                        </h2>
                        <br>
                        <v-container fill-height fluid lign-center v-if="filteredUpcomingAppointment.length == 0 && isPatient">
                            <v-row align="center" justify="center">
                                <v-col cols="12" class="text-center">
                                    <h3 class="mb-4" style="color: black">
                                        Wow no appointment found
                                    </h3>
                                    <p class="subtitle-1" style="color: grey">
                                        Maybe you would like to create an appointment?
                                    </p>
                                    <v-img class="mx-auto" cover :width="500" src="../assets/appointmentImages/noEvent.jpg" ></v-img>
                                    <v-btn class="mt-4" large color="blue lighten-1" dark to="/bookAppointment" >Create Appointment</v-btn >
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
                                        Take a break! You've earned it, you've cleared all your upcoming appointment for the day.
                                    </p>
                                    <v-img class="mx-auto" cover :width="500" src="../assets/appointmentImages/takeABreak.jpg" ></v-img>
                                </v-col>
                            </v-row>
                        </v-container>
                        <v-card v-for="(appointment, index) in filteredUpcomingAppointment" class="mt-2">
                            <v-card-item>
                                <div>
                                <div class="text-overline mb-1">
                                    Appointment {{index + 1}}
                                </div>
                                <div class="text-h6 mb-1 text-blue-lighten-1">
                                    <v-icon small class="mr-2">mdi-calendar</v-icon>
                                    {{ moment(appointment.date).format("YYYY-MMM-DD")}}
                                    {{ getTimeFromSlotNo(appointment.slotNo)}}
                                </div>
                                <div class="text-h6 mb-1">
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
                            <v-divider></v-divider>
                                <v-card-actions>
                                    <v-btn color="blue-lighten-1" variant="outlined" @click="openDeleteDialog(appointment)" prepend-icon="mdi-calendar-remove">Cancel Appointment</v-btn>
                                    <v-btn color="blue-lighten-1" variant="flat" v-if="isDoctor" @click="openUpdateDialog(appointment)" prepend-icon="mdi-calendar-check">Complete Appointment!</v-btn>
                                </v-card-actions>
                        </v-card>
                    </v-container>
                </v-window-item>
                <v-window-item value="completedAppointments">
                    <v-container>
                        <v-text-field v-model="searchCompletedAppointment" append-icon="mdi-magnify" label="Search Appointment By Clinic, Location or Doctor" single-line hide-details ></v-text-field>
                        <br>
                        <v-btn @click="openDatePickerDialog = true" class="mb-4 mx-auto" align="center" color="blue lighten-1">
                            Filtering by date: {{ moment(this.blockslotDateFilter).format("YYYY-MMM-DD") }}
                        </v-btn>
                        <v-dialog v-model="openDatePickerDialog" width="290px" >
                            <v-date-picker v-model="blockslotDateFilter" :min="minDate" no-title></v-date-picker>
                        </v-dialog>
                        <br />
                        <h2 class="text-blue-lighten-1 centered" align="center">
                            Showing: {{ filteredCompletedAppointment.length }} completed appointments
                        </h2>
                        <br />
                        <v-container fill-height fluid lign-center v-if="filteredCompletedAppointment.length == 0 && isDoctor">
                            <v-row align="center" justify="center">
                                <v-col cols="12" class="text-center">
                                    <h3 class="mb-4" style="color: primary">
                                        Wow no completed appointment found
                                    </h3>
                                    <p class="subtitle-1" style="color: grey">
                                        You may want to check your filters!
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
                        <v-card v-for="(appointment, index) in filteredCompletedAppointment" class="mt-2">
                            <v-card-item>
                                <div>
                                <div class="text-overline mb-1">
                                    Appointment {{ index + 1}}
                                </div>
                                <div class="text-h6 mb-1 text-blue-lighten-1">
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
                                    <v-btn color="blue-lighten-1" variant="outlined" prepend-icon="mdi-comment-quote" @click="openReviewDialog(appointment)">Give Review </v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-container>
                </v-window-item>
                <v-window-item value="reviewGiven" v-if="isPatient">
                    <v-container>
                        <v-text-field v-model="searchReviewGiven" append-icon="mdi-magnify" label="Search Review Clinic or Doctor Name" single-line hide-details ></v-text-field>
                        <br />
                        <h2 class="text-blue-darken-1 centered" align="center">
                            Showing: {{ filteredReviews.length }} Ratings
                        </h2>
                        <v-container fill-height fluid align-center v-if="filteredReviews.length == 0">
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
                            <v-card v-for="review in filteredReviews" class="mt-2 pt-5" >
                                <v-card-text class="text-h5 pb-5">
                                    "{{review.comments}}"
                                </v-card-text>
                                <v-rating color="blue-lighten-1" v-model=review.ratingGiven half-increments readonly></v-rating>
                                <v-card-text>
                                    <v-icon small class="mr-2">mdi-hospital-building</v-icon>
                                    Clinic Name: {{ review.clinicName }}
                                    <br>
                                    <v-icon small class="mr-2">mdi-doctor</v-icon>
                                    Doctor Name: Dr {{ review.doctorName }}
                                    <br>
                                    <v-icon small class="mr-2">mdi-calendar</v-icon>
                                    Reviewed On: {{ moment(review.timeStamp).format("YYYY-MMM-DD") }} by {{ review.patientName }}
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
                        <v-container fill-height fluid lign-center v-if="filteredReviews.length == 0 & isPatient">
                            <v-row align="center" justify="center">
                                <v-col cols="12" class="text-center">
                                    <h3 class="mb-4" style="color: black">
                                        Wow no ratings found
                                    </h3>
                                    <p class="subtitle-1" style="color: grey">
                                        Maybe you would like to give feedback to your completed appointments?
                                    </p>
                                    <v-img class="mx-auto" cover :width="500" src="../assets/appointmentImages/noEvent.jpg" ></v-img>
                                    <v-btn class="mt-4" large color="blue lighten-1" @click="changeCompleteTab('completedAppointments')">Clear Appointments</v-btn>
                                </v-col>
                            </v-row>
                        </v-container>
                        <v-container fill-height fluid lign-center v-if="filteredReviews.length == 0 & isDoctor">
                            <v-row align="center" justify="center">
                                <v-col cols="12" class="text-center">
                                    <h3 class="mb-4" style="color: black">
                                        Wow no ratings found
                                    </h3>
                                    <p class="subtitle-1" style="color: grey">
                                        Maybe you would like to mark appointments as completed?
                                    </p>
                                    <v-img class="mx-auto" cover :width="500" src="../assets/appointmentImages/review.jpg" ></v-img>
                                    <v-btn class="mt-4" large color="blue lighten-1" @click="changeCompleteTab('upcomingAppointments')">Clear Appointments</v-btn>
                                </v-col>
                            </v-row>
                        </v-container>
                        <v-container>
                            <v-card v-for="review in filteredReviews" class="mt-2 pt-5" >
                                <v-card-text class="text-h5 pb-5">
                                    "{{review.comments}}"
                                </v-card-text>
                                <v-rating color="blue-lighten-1" v-model=review.ratingGiven half-increments readonly></v-rating>
                                <v-card-text>
                                    <v-icon small class="mr-2">mdi-hospital-building</v-icon>
                                    Clinic Name: {{ review.clinicName }}
                                    <br>
                                    <v-icon small class="mr-2">mdi-doctor</v-icon>
                                    Doctor Name: Dr {{ review.doctorName }}
                                    <br>
                                    <v-icon small class="mr-2">mdi-calendar</v-icon>
                                    Reviewed On: {{ moment(review.timeStamp).format("YYYY-MMM-DD") }} by {{ review.patientName }}
                                    <br>
                                </v-card-text>
                            </v-card>
                        </v-container>
                    </v-container>
                </v-window-item>
                <v-window-item value="blockSlots" v-if="isDoctor">
                    <v-container>
                        <v-btn @click="openDatePickerDialog = true" class="mb-4" align="center" color="blue lighten-1">
                            Filtering by date: {{ moment(this.blockslotDateFilter).format("YYYY-MMM-DD") }}
                        </v-btn>
                        <br>
                        <v-dialog v-model="openDatePickerDialog" width="290px" >
                            <v-date-picker v-model="blockslotDateFilter" :min="minDate" no-title></v-date-picker>
                        </v-dialog>
                        <h2 class="text-blue-darken-1" align="center" >
                            Showing: {{ filterBlockSlots.length }} Blockslots
                        </h2>
                        <v-container fill-height fluid lign-center v-if="filterBlockSlots.length == 0 && isDoctor">
                            <v-row align="center" justify="center">
                                <v-col cols="12" class="text-center">
                                    <h3 class="mb-4" style="color: primary">
                                        Wow you have no blocked slots for the day!
                                    </h3>
                                    <p class="subtitle-1" style="color: grey">
                                        Would you like to create a block slot?
                                    </p>
                                    <v-img class="mx-auto" cover :width="500" src="../assets/appointmentImages/createBookSlot.jpg" ></v-img>
                                    <v-btn class="mt-4" large color="blue-lighten-1" dark @click='router.push("/createBlockSlot")'>Create a block slot</v-btn >
                                </v-col>
                            </v-row>
                        </v-container>
                        <v-container>
                            <v-card v-for="(blockSlot,index) in filterBlockSlots" class="mt-2">
                                <v-card-title class="headline mb-1">
                                    Blocked Slot #{{ index + 1 }}
                                </v-card-title>
                                <v-list-item three-line>
                                <v-list-item-content>
                                    <v-list-item-subtitle>
                                        <v-icon small class="mr-2">mdi-calendar</v-icon>
                                        {{ moment(blockSlot.date).format("YYYY-MMM-DD") }} {{ getTimeFromSlotNo(blockSlot.slotNo) }}
                                        <br>
                                        Reason: {{ blockSlot.reason }}
                                    </v-list-item-subtitle>
                                    </v-list-item-content>
                                </v-list-item>
                                <v-card-actions>
                                    <v-btn text variant = "outlined" color="blue lighten-1" prepend-icon="mdi-delete-forever" @click="openDeleteBlockSlotDialog(blockSlot)">
                                        Remove Blocked Slot
                                    </v-btn>
                                    <v-spacer></v-spacer> <!-- This pushes the following button to the right -->
                                </v-card-actions>
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
    <v-dialog v-model="deleteDialogVisible" width="auto" max-width="400">
      <v-card class="mx-auto pa-6 elevated-3" style="border-radius: 20px">
        <v-card-title class="text-center text-h4 text-blue-lighten-1 font-weight-bold" >Cancel Appointment?</v-card-title>
        <v-card-text class="text-center font-weight-light">
          This action is not irreversible. Are you sure you want to cancel the appointment?
        </v-card-text>
        <v-card-actions class="justify-center">
          <v-btn size="large" variant="outlined" color="blue lighten-1" @click="deleteDialogVisible = false">No</v-btn>
          <v-btn size="large" color="blue-lighten-1" variant="elevated" @click="deleteAppointment(currentAppointment)">Cancel Appointment!</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="updateDialogVisible" width="auto" max-width="400">
      <v-card class="mx-auto pa-6 elevated-3" style="border-radius: 20px">
        <v-card-title class="text-center text-h4 text-blue-lighten-1 font-weight-bold">Complete Appointment?</v-card-title>
        <v-card-text class="text-center font-weight-light">
          This action is not irreversible. Are you sure you want to mark the appointment as completed?
        </v-card-text>
        <v-card-actions class="justify-center">
          <v-btn size="large" variant="outlined" color="blue lighten-1" @click="updateDialogVisible = false">No</v-btn>
          <v-btn size="large" color="blue-lighten-1" variant="elevated" @click="updateAppointment(currentAppointment)">Mark as Complete!</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="reviewDialog" width="auto" >
        <v-form>
            <v-card class="mx-auto pa-6 elevated-3" style="border-radius: 20px" >
                <v-card-title class="text-center text-h3 text-blue-lighten-1 font-weight-bold" >Leave a review for</v-card-title>
                <v-card-title class="text-center text-h4 text-blue-lighten-1 font-weight-bold" >Dr {{ reviewDoc.doctorName }}</v-card-title>
                <v-card-text>
                    <div class="full-width-rating mt-2">
                        <v-rating  active-color="blue" color="blue-lighten-1" v-model="ratingGiven" half-increments hover :item-labels="['Poor', '', '', '', 'Excellent']" item-label-position="top" ></v-rating>
                    </div>
                    <v-textarea v-model="comment" label="Your Review" outlined rows="3" class="mt-3" auto-grow ></v-textarea>
                </v-card-text>
                <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn :disabled="!isReviewValid" color="primary" @click="submitReview(appointment)">Submit</v-btn>
                </v-card-actions>
            </v-card>
        </v-form>
    </v-dialog>
    <v-dialog v-model="deleteBlockSlotDialog" width="auto" max-width="400">
      <v-card class="mx-auto pa-6 elevated-3" style="border-radius: 20px">
        <v-card-title class="text-center text-h3 text-blue-lighten-1 font-weight-bold">Remove BlockSlot?</v-card-title>
        <v-card-text class="text-center text-h6 font-weight-light">
          This action is not irreversible. Are you sure you want to cancel the BlockSlot?
        </v-card-text>
        <v-card-actions class="justify-center">
          <v-btn size="large" variant="outlined" color="blue lighten-1" @click="this.deleteBlockSlotDialog = false">No</v-btn>
          <v-btn size="large" color="blue-lighten-1" variant="elevated" @click="deleteBlockSlot(currentBlockSlot)">Delete Blockslot</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    
</template>

<script>
    import moment from "moment";
    import { msgError, msgSuccess } from "../Tools/tools";
    import router from "../router"
    import { useStore, mapGetters, mapActions, mapState } from "vuex";
    import { computed, mounted } from "vue";
    import axios from "axios";
    export default {
        data() {
            return {
                router,
                blockslotDateFilter: new Date(), // Today's date in YYYY-MM-DD
                minDate: new Date(Date.now() - 86400000), // today's date for the min attribute
                openDatePickerDialog: false, // Controls the visibility of the date picker dialog
                dateRules: [
                    v => !!v || 'Date is required',
                    v => /^\d{4}-\d{2}-\d{2}$/.test(v) || 'Date must be in YYYY-MM-DD format',
                ],
                ratingGiven: 0, // Initial rating
                comment: '', // Initial review text
                deleteDialogVisible: false,
                deleteBlockSlotDialog: false,
                currentBlockSlot: "",
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
                userBlockSlots: "appointmentModule/getBookedSlots",
                isDoctor: "authModule/ifDoctor",
                isPatient: "authModule/ifPatient"
            }),
            filterBlockSlots() {
                let result = this.userBlockSlots.filter(bookslot=>
                    this.formatDate(bookslot.date) === this.formatDate(this.blockslotDateFilter)
                );
                return result
            },
            isReviewValid() {
                return this.ratingGiven > 0 && this.comment.trim() !== '';
            },
            filteredUpcomingAppointment() {
                let result = this.userAppointments.filter(appointment => appointment.bookingStatus === "Confirmed");
                result = result.filter(appointment =>
                    this.formatDate(appointment.date) === this.formatDate(this.blockslotDateFilter)
                );
                if (this.searchUpcomingAppointment) {
                    result = result.filter((appointment) =>
                        appointment.clinicLocation.toLowerCase().includes(this.searchUpcomingAppointment.toLowerCase()) ||
                        appointment.doctorName.toLowerCase().includes(this.searchUpcomingAppointment.toLowerCase()) ||
                        appointment.clinicName.toLowerCase().includes(this.searchUpcomingAppointment.toLowerCase())
                    );
                }
                return result;
            },
            filteredCompletedAppointment() {
                let result = this.userAppointments.filter(appointment => appointment.bookingStatus === "Completed");
                result = result.filter(appointment =>
                    this.formatDate(appointment.date) === this.formatDate(this.blockslotDateFilter)
                );
                if (this.searchCompletedAppointment) {
                    result = result.filter((appointment) =>
                        appointment.clinicLocation.toLowerCase().includes(this.searchCompletedAppointment.toLowerCase()) ||
                        appointment.doctorName.toLowerCase().includes(this.searchCompletedAppointment.toLowerCase()) ||
                        appointment.clinicName.toLowerCase().includes(this.searchCompletedAppointment.toLowerCase()) 
                    );
                }
                return result;
            },
            filteredReviews() {
                let result = this.userRatings
                if (this.searchReviewGiven) {
                    result = result.filter((appointment) =>
                        appointment.doctorName.toLowerCase().includes(this.searchReviewGiven.toLowerCase()) ||
                        appointment.clinicName.toLowerCase().includes(this.searchReviewGiven.toLowerCase()) 
                    );
                }
                return result;
            }
        },
        async mounted() {
        },
        methods: {
            onDateChange() {
                this.openDatePickerDialog = false; // Close the dialog after date selection
            },
            formatDate(dateString) {
                const date = new Date(dateString);
                const year = date.getFullYear();
                const month = ('0' + (date.getMonth() + 1)).slice(-2); // zero-based month +1
                const day = ('0' + date.getDate()).slice(-2);
                return `${year}-${month}-${day}`;
            },
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
            openDeleteBlockSlotDialog(blockSlot) {
                this.currentBlockSlot = blockSlot;
                this.deleteBlockSlotDialog = true;
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
            clearFilters() {
                this.searchCompletedAppointment = ""
                this.searchUpcomingAppointment = ""
                this.searchReviewGiven = ""
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
            async getBlockSlots(){
                this.isDataRetrieving = true;
                await this.$store.dispatch("appointmentModule/getAllUserBookSlot", this.userDetails.id)
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
            async deleteBlockSlot(blockSlots) {
                this.deleteBlockSlotDialog = false;
                this.isDataRetrieving = true;
                // payload = this.enhancePayload(payload)
                await this.$store.dispatch("appointmentModule/deleteBlockSlot", blockSlots.id)
                await this.getBlockSlots();
                this.isDataRetrieving = false;
                this.currentAppointment = null;
            },
        },
        watch: {
            async tab(newValue) {
                if (newValue === 'reviewGiven' || newValue === 'reviewReceived') {
                    this.blockslotDateFilter = new Date()
                    this.clearFilters()
                    this.getReviews()
                } else if (newValue === "upcomingAppointments" || newValue === 'completedAppointments'){
                    this.blockslotDateFilter = new Date()
                    this.clearFilters()
                    await this.getAppointments()
                } else if (newValue === "blockSlots") {
                    this.blockslotDateFilter = new Date()
                    this.clearFilters()
                    await this.getBlockSlots()
                }
            },
            blockslotDateFilter(newValue) {
                this.openDatePickerDialog = false;
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

.overflow-ellipsis {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
