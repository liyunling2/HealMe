<template>
    <v-container style="max-width: 1000px" class="mt-8">
    <v-stepper v-model="step" :items="items" :hide-actions=true>
    <template v-slot:item.1>
        <v-stepper-step step="1">
            <h3 class="text-h6">Select Your Clinic</h3>
            <br>
            <v-text-field v-model="searchClinic" label="Search by name or address" append-icon="mdi-magnify" single-line hide-details clearable ></v-text-field>
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
                <v-date-picker width="1000" v-model="selectedDate" :min="minDate" @input="dateChanged"></v-date-picker>
                </v-row>
            </v-container>
            <br>
            <h2 class="text-red-darken-1 centered">
                Showing all available timeslots
            </h2>
            <v-list-item-group v-model="selectedTimeslot" color="primary">
                <v-row>
                    <v-col cols="12" md="6" v-for="timeslot in filteredTimeslots" :key="timeslot.id">
                    <v-list-item @click="selectTimeslot(timeslot)" :value="timeslot">
                        <v-list-item-content>
                        <v-list-item-title>{{ timeslot.timeslot }}</v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                    </v-col>
                </v-row>
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
            Clinic: {{ selectedClinic.clinicName }}
            <br>
            Location: {{ selectedClinic.location }}
        <br>
            Selected Doctor: {{ selectedDoctor.doctorName }}
            <br>
            Doctor Ratings: {{ selectedDoctor.ratings }}
        <br>
            Appointment Date: {{ moment(this.selectedDate).format("MMM Do YYYY") }} {{ selectedTimeslot.timeslot }}

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
        searchClinic: '',
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
        timeslots: [],
    }),
    created() {
        this.generateTimeslotDictionary()
    },
    methods: {
        selectClinic(clinic) {
            this.selectedClinic = clinic;
            this.step++;
            this.$store.dispatch("appointmentModule/getAllDoctorsInClinic", {clinicID: this.selectedClinic.clinicID});
        },
        selectDoctor(doctor) {
            this.selectedDoctor = doctor;
            this.step++; 
            this.$store.dispatch("appointmentModule/getAllDoctorsInClinic", {clinicID: this.selectedClinic.clinicID});
        },
        dateChanged() {
            console.log("this workslol")
            console.log('Date selected:', newDate);
            //this.$store.dispatch("appointmentModule/getBooked", {clinicID: this.selectedClinic.clinicID});
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
                        const formattedHour = hour.toString().padStart(2, '0');
                        const formattedMinute = minute.toString().padStart(2, '0');
                        const timeslotString = `${formattedHour}:${formattedMinute}`;
                        timeslots.push({
                            id: slotId,
                            timeslot: timeslotString,
                            // date: new Date(today), // Clone today's date for each timeslot
                        })
                            slotId++;
                        }
                    }
            this.timeslots = timeslots
        },
        goBack() {
            this.step--;
        },
        makeAnAppointment() {
            const payload = {
                patientID: this.userDetails.patientID,
                doctorID: this.selectedDoctor.doctorID,
                doctorName: this.selectedDoctor.doctorName,
                patientEmail: this.userDetails.email,
                doctorEmail: this.selectedDoctor.email,
                patientID: this.userDetails.patientName,
                clinicID: this.selectedClinic.clinicID,
                clinicName: this.selectedClinic.clinicName,
                clinicLocation: this.selectedClinic.location,
                date: new Date(),
                slotNo: this.selectedTimeslot.id,
                bookingStatus: "confirmed"
            }
            console.log(payload)
            // this.$store.dispatch("appointmentModule/getAllClinics", payload);
        }
    },
    watch: {
        selectedDate(newDate, oldDate) {
            const payload = {
                clinicID: this.selectedClinic.clinicID, 
                doctorID:this.selectedDoctor.doctorID,
                date: newDate
            }
            this.$store.dispatch("appointmentModule/getBookedSlots", payload);
        }
    },
    computed: {
        ...mapGetters({
            userDetails: "authModule/getUserDetails",
            clinicsDetails: "appointmentModule/getClinics",
            clinicDoctorsDetails: "appointmentModule/getDoctorsClinics",
            bookedSlots: "appointmentModule/getBookedSlots"
        }),
        filteredTimeslots() {
            // Filter out the slots that are booked
            // const bookedSlots = this.bookedSlots
            // const availableTimeslots = { ...timeslotDictionary };
            // bookedSlots.forEach(booking => {
            //     if (availableTimeslots[booking.slot]) {
            //         delete availableTimeslots[booking.slot];
            //     }
            // });
            const availableTimeslots = this.timeslots
            return availableTimeslots;
        },
        filteredClinics() {
            let result = this.clinicsDetails;
                if (this.searchClinic) {
                    result = result.filter((clinic) =>
                        clinic.clinicName.toLowerCase().includes(this.searchClinic.toLowerCase()) || 
                        clinic.location.toLowerCase().includes(this.searchClinic.toLowerCase())
                    );
                }
            return result;
        },
        filteredDoctors() {
            let result = this.clinicDoctorsDetails;
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
                    doctor.specialty.includes(category))
                );
            }
            return result;
        },
    },
  }
  </script>
  