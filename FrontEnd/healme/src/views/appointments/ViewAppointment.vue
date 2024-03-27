<template>
    <v-card>
        
    </v-card>
</template>
<script>
    import { useStore, mapGetters, mapActions, mapState } from "vuex";
    import { ref, onMounted, onBeforeUnmount, computed, mounted } from "vue";
    import router from "../../router";
    import moment from "moment";

    export default {
        props: ["id"],
        components: {
        },
        Created(){
            
        },
        computed: {
            ...mapGetters({
            })
        },
        setup() {
            onMounted(() => {
            });
            onBeforeUnmount(() => {
            });
            return {
            };
        },
        data() {
            return {
            };
        },
        methods: {
            
        }
    }
</script>
