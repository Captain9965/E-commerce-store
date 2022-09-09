<template>
    <div class="page-success">
        <div class="columns is-multiline">
            <div class="column is-12" v-if="confirmed">
                <h1 class="has-text-success title"> Thank You for shopping with us!</h1>
                <p class="has-text-success">Your order will be processed within 24 hours</p>
            </div>
            <div class="column is-12 has-text-centered" v-if="confirming">
                <p class="has-text-success title">Confirming Payment. Please wait...</p>
                <button class="button is-danger mt-4" @click="cancel_request">Cancel</button>

            </div>
            <div class="column is-12 has-text-centered" v-if="cancelled">
                <p class="has-text-danger title">Confirmation cancelled!</p>
                <button class="button is-success mt-4" @click="confirm_order">Try again</button>
            </div>
            <div class="column is-12 has-text-centered" v-if="failed">
                <p class="has-text-success title">Confirmation failed.Retrying..</p>
                <button class="button is-danger mt-4" @click="cancel_request">Cancel</button>
            </div>
            
        </div>
    </div>
</template>
<script>
import axios from 'axios'
export default {
    name: 'Confirm',
    data(){
        return{
            errors:[],
            confirmed: false,
            cancelled: false,
            confirming: true,
            failed: false,
            intervalID: null

        }
    },
    mounted(){
        document.title = 'Confirm | Official Boots'
        this.$store.commit('clearInfos')
        this.$store.commit('clearErrors')
        this.confirm_order()
    },
    unmounted(){
        this.stop_interval()
    },
    methods:{
        get_checkoutRequestID(){
            let checkoutRequestID = ""
            if(sessionStorage.getItem('checkoutRequestID')){
                checkoutRequestID = sessionStorage.getItem('checkoutRequestID') 
            }
            return checkoutRequestID
        },
        confirm_order(){
            this.failed = false
            this.cancelled = false
            this.confirming = true
            this.confirmed = false
            this.$store.commit('setIsLoading', true)
            this.intervalID = setInterval(() => {
                this.send_confirmation_request()
            }, 5000);
        },
        async send_confirmation_request(){
            console.log("Sending request....")
            this.errors = []
            const data = {
                checkoutRequestID: this.get_checkoutRequestID()
            }
            await axios
                .post('api/v1/order/check/paystatus/',data)
                .then(response=>{
                    this.$store.commit('setIsLoading', false)
                    sessionStorage.removeItem('checkoutRequestID')
                    console.log(response.data)
                    this.confirming = false
                    this.stop_interval()
                    this.confirmed = true
                    this.$router.push('/order/success')
                    
                })/** can  do better error handling  */
                .catch(error=>{
                    console.log(error)
                    this.failed = true
                    this.cancelled = false
                    this.confirmed = false
                    this.confirming = false
                })
        },
        cancel_request(){
            this.failed = false
            this.confirming = false
            this.cancelled = true
            this.confirmed = false
            this.stop_interval()
        },
        stop_interval(){
            if(this.intervalID){
                clearInterval(this.intervalID)
                this.$store.commit('setIsLoading', false)
            }
        }
    }
    
}
</script>