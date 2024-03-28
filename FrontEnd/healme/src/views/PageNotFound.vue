<template>
    <v-container fill-height fluid>
        <v-row align="center" justify="center">
            <v-col cols="12" class="text-center">
                <v-icon size="120" color="red darken-2" >mdi-alert-circle-outline</v-icon >
                <h1 class="display-2 font-weight-bold mb-2" style="color: red">
                    404
                </h1>
                <h4 class="mb-4" style="color: red">Oops! Page not found.</h4>
                <p class="subtitle-1" style="color: grey">
                    Sorry, the page you're looking for doesn't exist or has been
                    moved.
                </p>
                <v-btn large color="red lighten-1" dark to="/" >Back to Home</v-btn >
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
    export default {
        name: "PageNotFound"
    };
</script>

<style scoped></style>
