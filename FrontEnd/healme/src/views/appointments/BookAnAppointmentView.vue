<template>
    <v-container style="max-width: 1000px" class="mt-8">
    <v-stepper v-model="step" :items="items" :hide-actions=true>
    <template v-slot:item.1>
        <v-stepper-step step="1">
            <h3 class="text-h6">Select Your Clinic</h3>
            <br>
            <v-text-field v-model="search" label="Search by name or address" append-icon="mdi-magnify" single-line hide-details clearable ></v-text-field>
            <br>
            <h2 class="text-red-darken-1 centered">
                Showing: {{ filteredClinics.length }} Clinics
            </h2>
            <v-list-item-group v-model="selectedClinic" color="primary">
                <v-list-item v-for="clinic in filteredClinics" :key="clinic.id" @click="selectClinic(clinic)" :value="clinic" >
                    <v-list-item-content>
                        <v-list-item-title>{{ clinic.clinicName }}</v-list-item-title>
                        <v-list-item-subtitle>{{ clinic.location }}</v-list-item-subtitle>
                    </v-list-item-content>
                </v-list-item>
            </v-list-item-group>
        </v-stepper-step>
    </template>

    <template v-slot:item.2>
        <v-stepper-step>
            <h3 class="text-h6">Select Your Doctor</h3>
            <br>
            <v-text-field v-model="doctorSearch" label="Search by name" append-icon="mdi-magnify" single-line hide-details clearable ></v-text-field>
            <v-autocomplete class="mt-4" v-model="selectedSpecialty" :items="specialty" item-text="name" item-value="name" label="Filter by Specialty" multiple chips :deletable-chips="true" ></v-autocomplete>
            <br>
            <h2 class="text-red-darken-1 centered">
                Showing: {{ filteredDoctors.length }} doctor
            </h2>
            <v-list-item-group v-model="selectedDoctor" color="primary">
            <v-list-item v-for="doctor in filteredDoctors" :key="doctor.id" @click="selectDoctor(doctor)" :value="doctor" >
                <v-list-item-content>
                <v-list-item-title>{{ doctor.doctorName }}</v-list-item-title>
                <v-list-item-subtitle>{{ doctor.specialty }}</v-list-item-subtitle>
                </v-list-item-content>
            </v-list-item>
            </v-list-item-group>
        </v-stepper-step>
    </template>

    <template v-slot:item.3>
      <h3 class="text-h6">Showing Dr {{ selectedDoctor.doctorName }} timeslot availability</h3>
      <br>
      <v-stepper-step>
            <h3 class="text-h6"></h3>
            <br>
            <v-container>
                <v-row justify="center">
                <v-date-picker width="1000" v-model="selectedDate" :min="minDate"></v-date-picker>
                </v-row>
            </v-container>
            <br>
            <h2 class="text-red-darken-1 centered">
                Showing all available timeslots
            </h2>
            <v-list-item-group v-model="selectedDoctor" color="primary">
                <v-list-item v-for="timeslot in filteredTimeslots" :key="timeslot.id" @click="selectTimeslot(timeslot)" :value="timeslot" >
                    <v-list-item-content>
                    <v-list-item-title>{{ timeslot.timeslot }}</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
            </v-list-item-group>
        </v-stepper-step>
    </template>

    <template v-slot:item.4>
      <h3 class="text-h6">Review your appointment</h3>
            Please make sure these details belong to the individual visiting the clinic.
        <v-stepper-step>
            
        </v-stepper-step>
        <br>
        <v-card>
            {{ selectedClinic.clinicName }}
            {{ selectedClinic.location }}
        <br>
            {{ selectedDoctor.doctorName }}
            {{ selectedDoctor.ratings }}
        <br>
            {{ moment(selectedTimeslot.date).format("MMM Do YY") }}
        <v-card-actions>
            <v-btn @click = "goBack()">
                previous
            </v-btn>
            <v-spacer>
            </v-spacer>
            <v-btn @click = "makeAnAppointment()">
                Make An Appointment!
            </v-btn>
        </v-card-actions>
        
        </v-card>
      
    </template>
  </v-stepper>
</v-container>
   
</template>
 

<script>
import moment from 'moment';
import { useStore, mapGetters, mapActions, mapState } from "vuex";

// function call all clinics first on life cycle hook
// on select clinic, generate the doctors
// on select doctor, generate the availability
// on select finish appointment, create appointment
  export default {
    data: () => ({
        moment,
        shipping: 0,
        selectedClinic: null,
        selectedDoctor: null,
        selectedTimeslot: null,
        selectedDate: new Date(), // today's date in YYYY-MM-DD format
        minDate: new Date(Date.now()-86400000), // today's date for the min attribute
        search: '',
        menu: false,
        date: '', // This will hold the selected date
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
                    "General Doctor",
                    "Urology",
                    "Pediatrics",
        ],
        doctorSearch:'',
        step: 1,
        items: [
            'Select Your Clinic',
            'Select Your Doctor',
            'Select Appointment Timing',
            'Confirm Your Appointment',
        ],
        clinics: [
            { id: 1, clinicName: 'Aljunied Medical', location: '389 Upper Aljunied Rd, SG367874'},
            { id: 2, clinicName: 'Aljunied Medical', location: '389 Upper Aljunied Rd, SG367874'},
        ],
        doctors: [
            { id: 1, doctorName: 'Marcus Yap', ratings: '4.7', specialty:["Dermatology"]},
            { id: 2, doctorName: 'Marcus Yeet', ratings: '4.4', specialty:["General Doctor"]},
        ],
        timeslots: [
            { id: 1, timeslot: '7:30', date: new Date(Date.now()+86400000)},
            { id: 2, timeslot: '8:00', date: new Date(Date.now()+86400000 * 2)},
            { id: 3, timeslot: '8:30', date: new Date(Date.now()+86400000 * 3)},
            { id: 4, timeslot: '9:00', date: new Date(Date.now()+86400000)},
            { id: 5, timeslot: '9:30', date: new Date(Date.now()+86400000 * 2)},
            { id: 6, timeslot: '10:00', date: new Date(Date.now()+86400000 * 4)},
        ],
    }),
    created() {
    },
    methods: {
        selectClinic(clinic) {
            this.selectedClinic = clinic;
            this.step++; // Move to the next step in the stepper
            // call for the data
        },
        selectDoctor(doctor) {
            this.selectedDoctor = doctor;
            this.step++; // Move to the next step in the stepper
            // 
        },
        selectTimeslot(timeslot) {
            this.selectedTimeslot = timeslot;
            this.step++; // Move to the next step in the stepper
        },
        goBack() {
            this.step--;
        },
        makeAnAppointment() {
            const payload = {
                patientID: this.userDetails.patientID,
                doctorID: this.selectedDoctor.doctorID,
                doctorName: this.selectedDoctor.doctorName,
                patientID: this.userDetails.patientName,
                clinicID: this.selectedClinic.clinicID,
                clinicName: this.selectedClinic.clinicName,
                clinicLocation: this.selectedClinic.location,
                date: new Date(),
                slotNo: this.selectedTimeslot.slotID,
                bookingStatus: "confirmed"
            }
            console.log(payload)
            // this.$store.dispatch("appointmentModule/getAllClinics", payload);
        }
    },
    computed: {
        ...mapGetters({
            userDetails: "authModule/getUserDetails",
        }),
        filteredTimeslots() {
            return this.timeslots.filter(timeslot => {
                // Ensure 'timeslot.date' is a Moment.js object
                let timeslotDate = moment(timeslot.date);
                // Ensure 'this.selectedDate' is a Moment.js object
                let selectedDate = moment(this.selectedDate, 'YYYY-MM-DD');
                // Use Moment.js 'isSame' function to compare the two dates
                return timeslotDate.isSame(selectedDate, "date");
            });
        },
        filteredClinics() {
            const searchString = this.search.toLowerCase();
            return this.clinics.filter(clinic => {
                return (
                clinic.clinicName.toLowerCase().includes(searchString) ||
                clinic.location.toLowerCase().includes(searchString)
                );
            });
        },
        filteredDoctors() {
            let result = this.doctors;
            // Filter by name if search string is provided
            if (this.doctorSearch) {
            const searchString = this.doctorSearch.toLowerCase();
            result = result.filter(doctor =>
                doctor.doctorName.toLowerCase().includes(searchString)
            );
            }
            // Further filter by selected category/specialty if any are selected
            if (this.selectedSpecialty.length > 0) {
            result = result.filter(doctor =>
                this.selectedSpecialty.some(category =>
                doctor.specialty.includes(category)
                )
            );
            }
            return result;
        },
    },
  }
  </script>
  