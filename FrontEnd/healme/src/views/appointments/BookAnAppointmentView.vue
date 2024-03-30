<template>
  <v-container style="max-width: 800px" class="mt-8">
    <p class="font-weight-bold text-h3 text-blue-lighten-1 text-center">
      Let's Create an appointment
    </p>
    <br />
    <v-stepper v-model="step" :items="items" :hide-actions="true">
      <template v-slot:item.1>
          <h3 class="text-h6">Select Your Clinic</h3>
          <v-text-field
            v-model="searchClinic"
            label="Search clinic by name or address"
            append-icon="mdi-magnify"
            single-line
            hide-details
            clearable
          ></v-text-field>
          <br />
          <h2 class="text-blue-lighten-1 text-center">
            Showing: {{ filteredClinics.length }} Clinics
          </h2>
            <v-list-item v-model="selectedClinic"
              v-for="clinic in filteredClinics"
              :key="clinic.id"
              @click="selectClinic(clinic)"
              :value="clinic"
              class="padded-list-item"
            >
              <template v-slot:prepend>
                <v-icon color="info">mdi-hospital-building</v-icon>
              </template>
              <v-list-item-title>{{ clinic.clinicName }}</v-list-item-title>
              <v-list-item-subtitle>
                <v-icon> mdi-hospital-marker </v-icon>
                Location: {{ clinic.location }}
              </v-list-item-subtitle>
              <template v-slot:append>
                <v-icon>mdi-arrow-right</v-icon>
              </template>
            </v-list-item>
            <v-container
              fill-height
              fluid
              lign-center
              v-if="filteredClinics.length == 0"
            >
              <v-row align="center" justify="center">
                <v-col cols="12" class="text-center">
                  <h3 class="mb-4 text-blue-lighten-1">Wow no Clinic found</h3>
                  <p class="subtitle-1" style="color: grey">
                    Maybe you would like to switch your search fitlers..?
                  </p>
                  <v-img
                    class="mx-auto"
                    cover
                    :width="500"
                    src="../../assets/appointmentImages/noClinic.jpg"
                  ></v-img>
                </v-col>
              </v-row>
            </v-container>
      </template>

      <template v-slot:item.2>
          <h3 class="text-h6">Select Your Doctor</h3>
          <br />
          <v-text-field
            v-model="doctorSearch"
            label="Search Doctor By Name"
            append-icon="mdi-magnify"
            single-line
            hide-details
            clearable
          ></v-text-field>
          <v-autocomplete
            class="mt-4"
            v-model="selectedSpecialty"
            :items="specialty"
            item-text="name"
            item-value="name"
            label="Filter by Specialty"
            multiple
            chips
            :deletable-chips="true"
          ></v-autocomplete>

          <h2 class="text-blue-lighten-1 text-center">
            Showing: {{ filteredDoctors.length }} doctor
          </h2>
          <br />
        <v-card>
            <v-container
              fill-height
              fluid
              lign-center
              v-if="filteredDoctors.length == 0"
            >
              <v-row align="center" justify="center">
                <v-col cols="12" class="text-center">
                  <h3 class="mb-4 text-blue-lighten-1">Wow no doctors found</h3>
                  <p class="subtitle-1" style="color: grey">
                    Maybe you would like to switch your search fitlers..?
                  </p>
                  <v-img
                    class="mx-auto"
                    cover
                    :width="500"
                    src="../../assets/appointmentImages/noDoctor.jpg"
                  ></v-img>
                </v-col>
              </v-row>
            </v-container>
            <v-list-item
              v-for="doctor in filteredDoctors"
              :key="doctor.id"
              @click="selectDoctor(doctor)"
              :value="doctor"
            >
              <template v-slot:prepend>
                <v-icon color="info">mdi-doctor</v-icon>
              </template>
              <v-list-item-title>{{ doctor.doctorName }}</v-list-item-title>
              <v-list-item-subtitle
                >Specialty: {{ doctor.specialty }}</v-list-item-subtitle
              >
              <v-list-item-subtitle> Rating: {{ doctor.ratings }} </v-list-item-subtitle>
              <v-list-item-subtitle> Description: {{ doctor.doctorDesc }} </v-list-item-subtitle>
              <template v-slot:append>
                <v-icon>mdi-arrow-right</v-icon>
              </template>
            </v-list-item>
          <br />
          <v-card-actions>
            <v-btn
              class="text-none"
              prepend-icon="mdi-arrow-left"
              variant="text"
              border
              color="blue-lighten-1"
              @click="goBack()"
            >
              Previous
            </v-btn>
            <v-spacer> </v-spacer>
          </v-card-actions>
        </v-card>
      </template>
      <template v-slot:item.3>
        <h3 class="text-h6">
          Showing Dr {{ selectedDoctor.doctorName }} availability
        </h3>
        <br />
        <v-card>
          <h3 class="text-h6"></h3>
          <br />
          <v-container>
            <v-row justify="center">
              <v-date-picker
                :dark="true"
                :scrollable="true"
                color="blue-lighten-1"
                width="1000"
                v-model="selectedDate"
                :min="minDate"
              ></v-date-picker>
            </v-row>
          </v-container>
          <br />
          <h2 class="text-blue-lighten-1 text-center">
            Showing Dr {{ selectedDoctor.doctorName }}'s
            {{ moment(selectedDate).format("DD-MM-YYYY") }} available timeslots
          </h2>
          <br />
            <v-row>
              <v-col
                cols="12"
                md="6"
                v-for="timeslot in availableTimeslots"
                :key="timeslot.slotNo"
              >
                <v-list-item
                  @click="selectTimeslot(timeslot)"
                  :value="timeslot"
                >
                  <v-list-item-content>
                    <v-list-item-title class="text-center">{{
                      timeslot.timeslot
                    }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-col>
            </v-row>
          <v-card-actions>
            <v-btn
              class="text-none"
              prepend-icon="mdi-arrow-left"
              variant="text"
              border
              @click="goBack()"
            >
              Previous
            </v-btn>
            <v-spacer> </v-spacer>
          </v-card-actions>
        </v-card>
      </template>

      <template v-slot:item.4>
        <h3 class="text-h6">Review your appointment</h3>
        <br />
        <v-card>
          <v-list dense class="pa-0">
            <!-- Clinic Details -->
            <v-list-item two-line>
              <v-list-item-content>
                <v-list-item-title>Clinic Details</v-list-item-title>
                <v-list-item-subtitle>
                  <v-icon small class="mr-2">mdi-map-marker</v-icon>
                  Clinic: {{ selectedClinic.clinicName }}
                </v-list-item-subtitle>
                <v-list-item-subtitle>
                  <v-icon small class="mr-2">mdi-city</v-icon>
                  Location: {{ selectedClinic.location }}
                </v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
            <v-divider></v-divider>
            <!-- Doctor Details -->
            <v-list-item two-line>
              <v-list-item-content>
                <v-list-item-title>Doctor Details</v-list-item-title>
                <v-list-item-subtitle>
                  <v-icon small class="mr-2">mdi-account</v-icon>
                  Selected Doctor: {{ selectedDoctor.doctorName }}
                </v-list-item-subtitle>
                <v-list-item-subtitle>
                  <v-icon small class="mr-2">mdi-stethoscope</v-icon>
                  Doctor Specialty:  {{ selectedDoctor.specialty }}
                </v-list-item-subtitle>
                <v-list-item-subtitle>
                  <v-icon small class="mr-2">mdi-star</v-icon>
                  Doctor Description: {{ selectedDoctor.doctorDesc }}
                </v-list-item-subtitle> 
                <v-list-item-subtitle>
                  <v-icon small class="mr-2">mdi-star</v-icon>
                  Doctor Rating: {{ selectedDoctor.ratings }}
                </v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
            <v-divider></v-divider>
            <!-- Appointment Timing -->
            <v-list-item two-line>
              <v-list-item-content>
                <v-list-item-title>Timing Details</v-list-item-title>
                <v-list-item-subtitle>
                  <v-icon small class="mr-2">mdi-calendar</v-icon>
                  Appointment Date: {{ moment(this.selectedDate).format("YYYY-MMM-DD") }}{{ getTimeFromSlotNo(selectedTimeslot.slotNo) }}
                </v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-list>
          <v-card-actions>
            <v-btn class="text-none" prepend-icon="mdi-arrow-left" variant="text" border @click="goBack()" >
              Previous
            </v-btn>
            <v-spacer> </v-spacer>
            <v-btn color="blue-lighten-1" variant="flat" prepend-icon="mdi-calendar-check" @click="makeAnAppointment()" >
              Make An Appointment!
            </v-btn>
          </v-card-actions>
        </v-card>
      </template>
    </v-stepper>
  </v-container>
  <div v-if="isDataRetrieving" class="overlay">
      <v-progress-circular
        color="primary"
        indeterminate
        size="64"
        class="loader"
      ></v-progress-circular>
    </div>
</template>


<script>
import moment from "moment";
import { useStore, mapGetters, mapActions, mapState } from "vuex";

export default {
  data: () => ({
    isDataRetrieving:false,
    moment,
    shipping: 0,
    selectedClinic: null,
    selectedDoctor: null,
    selectedTimeslot: null,
    selectedDate: new Date(), // today's date in YYYY-MM-DD format
    minDate: new Date(Date.now() - 86400000), // today's date for the min attribute
    searchClinic: "",
    menu: false,
    date: "", // This will hold the selected date
    selectedSpecialty: [],
    specialty: [
      "Cardiology",
      "Dermatology",
      "Endocrinology",
      "Gastroenterology",
      "Hematology",
      "Neurology",
      "Oncology",
      "Psychiatry ",
      "General Practice",
      "Urology",
      "Pediatrics",
    ],
    doctorSearch: "",
    step: 1,
    items: [
      "Select Clinic",
      "Select Doctor",
      "Select Timing",
      "Review Appointment",
    ],
    timeslots: null,
  }),
  async created() {
    this.isDataRetrieving = true;
    await this.$store.dispatch("appointmentModule/getAllClinics");
    this.isDataRetrieving = false;
    this.generateTimeslotDictionary();
  },
  methods: {
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
    async selectClinic(clinic) {
      this.selectedClinic = clinic;
      this.isDataRetrieving = true;
      await this.$store.dispatch("appointmentModule/getAllDoctorsInClinic", {
        clinicID: this.selectedClinic.clinicID,
      });
      this.isDataRetrieving = false;
      this.step++;
    },
    async selectDoctor(doctor) {
      this.selectedDoctor = doctor;
      this.isDataRetrieving = true;
      await this.$store.dispatch("appointmentModule/getDoctorAvailableSlots", {
          clinicID: this.selectedClinic.clinicID,
          doctorID: this.selectedDoctor.doctorID,
          date: moment(new Date()).format("YYYY-MM-DD"),
        }
      );
      this.isDataRetrieving = false;
      this.step++;
    },
    selectTimeslot(timeslot) {
      this.selectedTimeslot = timeslot;
      this.step++;
    },
    generateTimeslotDictionary() {
      const timeslots = [];
      let slotId = 1;
      const today = new Date(); // Get today's date
      today.setHours(0, 0, 0, 0); // Reset time to 00:00:00 for consistency
      for (let hour = 7; hour <= 18; hour++) {
        for (let minute = 0; minute < 60; minute += 30) {
          // Adjusting the condition to skip the slot immediately after the loop condition meets
          if (hour === 17 && minute === 30) continue;
          const formattedHour = hour.toString().padStart(2, "0");
          const formattedMinute = minute.toString().padStart(2, "0");
          const timeslotString = `${formattedHour}:${formattedMinute}`;
          timeslots.push({
            slotNo: slotId,
            timeslot: timeslotString,
            // date: new Date(today), // Clone today's date for each timeslot
          });
          slotId++;
        }
      }
      this.timeslots = timeslots;
    },
    goBack() {
      this.step--;
    },
    async makeAnAppointment() {
      const payload = {
        bookingStatus:"Confirm",
        clinicID: this.selectedClinic.clinicID,
        clinicLocation: this.selectedClinic.location,
        clinicName: this.selectedClinic.clinicName,
        date: moment(this.selectedDate).format("YYYY-MM-DD"),
        doctorEmail: this.selectedDoctor.email,
        doctorID: this.selectedDoctor.doctorID,
        doctorName: this.selectedDoctor.doctorName,
        doctorSpecialty: this.selectedDoctor.specialty,
        patientEmail: this.userDetails.email,
        patientID: this.userDetails.id,
        patientName: this.userDetails.name,
        slotNo: this.selectedTimeslot.slotNo
      }
      this.isDataRetrieving = true;
      await this.$store.dispatch("appointmentModule/createAppointment", payload);
      this.isDataRetrieving = false;
    },
  },
  watch: {
    async selectedDate(newDate, oldDate) {
      const payload = {
        clinicID: this.selectedClinic.clinicID,
        doctorID: this.selectedDoctor.doctorID,
        date: moment(newDate).format("YYYY-MM-DD"),
      };
      this.isDataRetrieving = true;
      await this.$store.dispatch("appointmentModule/getDoctorAvailableSlots", payload);
      this.isDataRetrieving = false;
    },
  },
  computed: {
    ...mapGetters({
      userDetails: "authModule/getUserDetails",
      clinicsDetails: "appointmentModule/getClinics",
      clinicDoctorsDetails: "appointmentModule/getDoctorsClinics",
      bookedSlots: "appointmentModule/getBookedSlots",
    }),
    availableTimeslots() {
      let result = this.timeslots
      if (this.bookedSlots.length >= 1) {
        const bookedSlotNumbers = this.bookedSlots.map(slot => slot.slotNo);
        result = result.filter(timeslot => 
          !bookedSlotNumbers.includes(timeslot.slotNo)
        );
      } 
      return result
    },
    filteredClinics() {
      let result = this.clinicsDetails;
      if (this.searchClinic) {
        result = result.filter(
          (clinic) =>
            clinic.clinicName
              .toLowerCase()
              .includes(this.searchClinic.toLowerCase()) ||
            clinic.location
              .toLowerCase()
              .includes(this.searchClinic.toLowerCase())
        );
      }
      return result;
    },
    filteredDoctors() {
      let result = this.clinicDoctorsDetails;
      // Filter by name if search string is provided
      if (this.doctorSearch) {
        const searchString = this.doctorSearch.toLowerCase();
        result = result.filter((doctor) =>
          doctor.doctorName.toLowerCase().includes(searchString)
        );
      }
      // Further filter by selected category/specialty if any are selected
      if (this.selectedSpecialty.length > 0) {
        result = result.filter((doctor) =>
          this.selectedSpecialty.some((category) =>
            doctor.specialty.includes(category)
          )
        );
      }
      return result;
    },
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
  z-index: 1000; /* Ensure it's above other content */
}
</style>