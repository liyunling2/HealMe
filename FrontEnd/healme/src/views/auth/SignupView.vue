<template>
    <v-container class="fill-height" fluid>
        <v-card width="500px" max-width="550px" class="mx-auto pa-6 elevated-3" style="border-radius: 20px" >
            <div class="text-center text-h3 text-red-darken-1 font-weight-bold">
                Sign up
            </div>
            <v-card-text class="text-center text-h6 font-weight-light">
                Create an account with us!
            </v-card-text>
            <v-card-text>
                <v-form @submit.prevent="onSubmit" ref="form" v-model="formValid" >
                    <v-row>
                        <v-col cols="12" md="6">
                            <v-text-field
                                v-model="firstName"
                                :rules="[required]"
                                label="First Name"
                                placeholder="Enter your first name"
                            ></v-text-field>
                        </v-col>
                        <v-col cols="12" md="6">
                            <v-text-field
                                v-model="lastName"
                                :rules="[required]"
                                label="Last Name"
                                placeholder="Enter your last name"
                            ></v-text-field>
                        </v-col>
                    </v-row>
                    <v-text-field
                        v-model="email"
                        :rules="[required, emailCheck]"
                        class="mb-2"
                        clearable
                        label="Email"
                        placeholder="Enter your Email"
                    ></v-text-field>
                    <v-text-field
                        type="password"
                        v-model="password"
                        :rules="[required, passwordMinLength]"
                        class="mb-2"
                        clearable
                        label="Password"
                        placeholder="Enter your password"
                    ></v-text-field>
                    <br />
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn
                            color="red"
                            :disabled="!formValid"
                            type="submit"
                            variant="elevated"
                        >
                            Sign Up
                        </v-btn>
                    </v-card-actions>
                </v-form>
            </v-card-text>
            <v-card-subtitle>
                Have an account?
                <router-link style="color: red" to="/login">
                    Sign in Instead
                </router-link>
            </v-card-subtitle>
        </v-card>
    </v-container>
</template>

<script>
    import { ref } from "vue";
    import { useStore } from "vuex";
    import { useRouter } from "vue-router";
    import { v4 as uuidv4 } from "uuid";

    export default {
        data() {
            return {
                firstName: "",
                lastName: "",
                email: "",
                password: "",
                picture: null,
                formValid: false,
                imageFile: null,
                imageUrl: null
            };
        },
        methods: {
            async onSubmit() {
                const valid = this.$refs.form.validate();
                if (!valid) return;
                const dataPayload = {
                    email: this.email,
                    password: this.password,
                    firstName: this.firstName,
                    lastName: this.lastName,
                    displayPicturePath: imageStore.imageUrlPath
                };
                this.$store.dispatch("authModule/signUp", dataPayload);
            },
            required(v) {
                return !!v || "This field is required";
            },
            passwordMinLength(v) {
                return (
                    (v && v.length >= 6) ||
                    "Password must be at least 6 characters long"
                );
            },
            emailCheck(v) {
                // Simple email regex, consider a more robust solution for production
                const pattern =
                    /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,4}\.[0-9]{1,4}\.[0-9]{1,4}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
                return pattern.test(v) || "Invalid e-mail.";
            },
        }
    };
</script>
