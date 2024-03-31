<template>
      <v-container style="max-width: 800px" class="mt-8">
        <p class="font-weight-bold text-h3 text-blue-lighten-1 text-center">
            Let's Block an appointment slot
        </p>
        <br />
        <v-stepper v-model="step" :items="items" :hide-actions="true">
            <template v-slot:item.1>
                <v-card>
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
                            Showing Dr {{ this.userDetails.name }}'s
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
                </v-card>
            </template>
            <template v-slot:item.2>
                <v-card>
                    <h3 class="text-h6 text-blue-lighten-1">Give a reason for absence!</h3>
                    <br />
                    <v-form ref="form" v-model="formValid">
                        
                    <v-textarea
                        v-model="reasonGiven"
                        :rules="reasonRules"
                        label="Reason"
                        clearable
                    ></v-textarea>
                    <v-card-actions>
                        <v-btn class="text-none" prepend-icon="mdi-arrow-left" variant="text" border @click="goBack()">
                        Previous
                        </v-btn>
                        <v-spacer></v-spacer>
                        <!-- Disable the Next button if the form is not valid -->
                        <v-btn color="blue lighten-1" variant="flat" prepend-icon="mdi-arrow-right" @click="goNext()" :disabled="!formValid">
                        Next 
                        </v-btn>
                    </v-card-actions>
                    </v-form>
                </v-card>
            </template>
            <template v-slot:item.3>
                <v-card>
                    <h3 class="text-h6 text-blue-lighten-1">Review your block slot</h3>
                    <br />
                    <v-card-text >
                        <div class="mb-4">
                            <div class="text-h4 mb-2 text-blue-lighten-1">{{ moment(selectedDate).format("YYYY-MMM-DD") }} {{ getTimeFromSlotNo(selectedTimeslot.slotNo) }}</div>
                        </div>
                        <v-subheader>Reason Given:</v-subheader>
                        <br>
                        <p>{{ this.reasonGiven }}</p>
                    </v-card-text>
                    <v-card-actions>
                        <v-btn class="text-none" prepend-icon="mdi-arrow-left" variant="text" border @click="goBack()" >
                          Previous
                        </v-btn>
                        <v-spacer> </v-spacer>
                        <v-btn color="blue-lighten-1" variant="flat" prepend-icon="mdi-arrow-right" @click="createBlockSlot()" >
                          Create BlockSlot 
                        </v-btn>
                      </v-card-actions>
                    </v-card>
            </template>
    </v-stepper>
    </v-container>

<div v-if="isDataRetrieving" class="overlay">
    <v-progress-circular color="primary" indeterminate size="64" class="loader" ></v-progress-circular>
</div>
</template>
<script>
    import { useStore, mapGetters, mapActions, mapState } from "vuex";
    import { ref, onMounted, onBeforeUnmount, computed, mounted } from "vue";
    import router from "../../router";
    import moment from "moment";

    export default {
        components: {
        },
        async created(){
            this.generateTimeslotDictionary();
            this.getDoctorSlots()
        },
        watch: {
            async selectedDate(newDate, oldDate) {
                this.selectedDate = newDate
                const payload = {
                    clinicID: this.userDetails.clinicID,
                    doctorID: this.userDetails.id,
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
            }
        },
        setup() {
            onMounted(() => {
                
            });
            return {
            };
        },
        data() {
            return {
                moment,
                reasonGiven: '',
                formValid: false, // This will track the form's validation state
                step: 1,
                items: [
                "Select Timing",
                "Give a Reason",
                "Confirm BlockSlot",
                ],
                timeslots: null,
                isDataRetrieving:false,
                selectedTimeslot: null,
                selectedDate: new Date(),
                minDate: new Date(Date.now() - 86400000),
                reason: "",
                reasonRules: [
                    v => !!v.trim() || 'Reason is required', // Checks if the input is not empty
                ]
            };
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
            async getDoctorSlots () {
                this.isDataRetrieving = true;
                var payload = {
                    clinicID: this.userDetails.clinicID,
                    doctorID: this.userDetails.id,
                    date: moment(new Date()).format("YYYY-MM-DD"),
                }
                await this.$store.dispatch("appointmentModule/getDoctorAvailableSlots", payload);
                this.isDataRetrieving = false;
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
            goNext() {
                this.step++;
            },
            async createBlockSlot() {
                this.isDataRetrieving = true;
                var payload = {
                    "doctorID": this.userDetails.id,
                    "clinicID": this.userDetails.clinicID,
                    "date": moment(this.selectedDate).format("YYYY-MM-DD"),
                    "email": this.userDetails.email,
                    "slotNo": this.selectedTimeslot.slotNo,
                    "reason": this.reasonGiven
                }
                await this.$store.dispatch("appointmentModule/createBookedSlot", payload);
                this.isDataRetrieving = false;
                router.push("/profile")
                this.reasonGiven = ""
            }
        }
    }
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