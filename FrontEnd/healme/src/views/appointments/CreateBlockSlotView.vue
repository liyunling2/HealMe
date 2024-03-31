<template>
      <v-container style="max-width: 800px" class="mt-8">
        <v-stepper v-model="step" :items="items" :hide-actions="true">
            <template v-slot:item.1>
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
                        <v-card-actions>
                            <v-btn
                            class="text-none"
                            prepend-icon="mdi-arrow-left"
                            variant="text"
                            border
                            >
                            submit
                            </v-btn>
                            <v-spacer> </v-spacer>
                        </v-card-actions>
                </v-card>
            </template>
            <template v-slot:item.2>
                <v-card>
                    <v-textarea
                        v-model="reasonGiven"
                        label="Reason"
                        append-icon="mdi-magnify"
                        clearable
                    ></v-textarea>
                    <v-card-actions>
                        <v-btn class="text-none" prepend-icon="mdi-arrow-left" variant="text" border @click="goBack()" >
                          Previous
                        </v-btn>
                        <v-spacer> </v-spacer>
                        <v-btn color="blue-lighten-1" variant="flat" prepend-icon="mdi-arrow-right" @click="goNext()" >
                          Next 
                        </v-btn>
                      </v-card-actions>
                    </v-card>
            </template>
            <template v-slot:item.3>
                <v-card>
                    Hello
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
            };
        },
        methods: {
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
                    "slotNo": this.selectedTimeslot.slotNo,
                    "reason": this.reason
                }
                await this.$store.dispatch("appointmentModule/createBookedSlot", payload);
                this.isDataRetrieving = false;
                router.push("/profile")
                this.reason = ""
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