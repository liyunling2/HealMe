<template>
    <v-container class="fill-height" fluid style="">
        <v-card
            width="500px"
            max-width="550px"
            class="mx-auto pa-6 elevated-3"
            style="border-radius: 20px"
        >
            <div class="text-center text-h3 text-blue-lighten-1 font-weight-bold">
                Login
            </div>
            <v-card-text class="text-center text-h6 font-weight-light">
                Login to your HealMe account
            </v-card-text>
            <v-card-text>
                <v-form @submit.prevent="onSubmit" ref="form" v-model="valid">
                    <v-text-field v-model="email" :rules="emailRules" label="Email" placeholder="Enter your Email" class="mb-2" clearable required > </v-text-field>
                    <v-text-field v-model="password" :rules="passwordRules" label="Password" placeholder="Enter your password" type="password" class="mb-2" clearable required > </v-text-field>
                    <v-checkbox v-model="doctorCheck" :label="`Sign in as a doctor.`"></v-checkbox>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn :disabled="!valid" color="blue-lighten-1" type="submit" variant="elevated" > Sign In </v-btn>
                    </v-card-actions>
                </v-form>
            </v-card-text>
            <v-card-subtitle>
                Don't have an account?
                <router-link style="color: red" to="/signup">
                    Sign Up Instead
                </router-link>
            </v-card-subtitle>
        </v-card>
    </v-container>
</template>

<script>
    import { useStore } from "vuex";
    import { useRouter } from "vue-router";

    export default {
        data() {
            return {
                doctorCheck: false,
                //email: "eileen@gmail.com",
                email: 'huimin@familycareclinic.sg',
                //password: "password",
                password: "securepassword123",
                valid: false, // This will be our form validity flag
                emailRules: [
                    // Email validation rules
                    (v) => !!v || "E-mail is required",
                    (v) => /.+@.+\..+/.test(v) || "E-mail must be valid"
                ],
                passwordRules: [
                    // Password validation rules
                    (v) => !!v || "Password is required",
                    (v) =>
                        v.length >= 6 ||
                        "Password must be at least 6 characters long"
                ]
            };
        },
        methods: {
            onSubmit() {
                if (this.doctorCheck) {
                        this.$store.dispatch("authModule/doctorSignIn", {
                        email: this.email,
                        password: this.password
                    });
                } else {
                    this.$store.dispatch("authModule/userSignIn", {
                        email: this.email,
                        password: this.password
                    });
                }
                
            }
        }
    };
</script>
