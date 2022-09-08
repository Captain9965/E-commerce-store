<template>
    <div class="page-checkout">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="has-text-primary title">Checkout</h1>
            </div>
            <div class="bck-grey column is-12 box">
                <table class=" has-text-warning bck-grey table is-fullwidth" v-if="cartTotalLength">
                    <thead>
                        <tr>
                            <th class="has-text-warning">Product</th>
                            <th class="has-text-warning">Price</th>
                            <th class="has-text-warning">Quantity</th>
                            <th class="has-text-warning">Total</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                       <tr
                            v-for="item in cart.items"
                            v-bind:key="item.product.id"
                       >
                            <td>{{item.product.name}}</td>
                            <td>Ksh.{{item.product.price}}</td>
                            <td>{{item.quantity}}</td>
                            <td>Ksh.{{parseInt(getItemTotal(item))}}</td>
                       </tr>
                    </tbody>
                    <tfoot>
                        <tr>
                            <td colspan="2" class="has-text-warning">Total</td>
                            <td class="has-text-warning">{{cartTotalLength}}</td>
                            <td class="has-text-warning">Ksh.{{parseInt(cartTotalPrice)}}</td>
                        </tr>
                    </tfoot>
                </table>
                <p v-else class="has-text-warning"> No items to check out....</p>
            </div>
        </div>
        <div class="column is-12">
                <h1 class="has-text-primary title">Delivery Details</h1>
        </div>
        <div class="bck-grey column is-12 box">
            <p class="has-text-danger mb-4">*All fields are required</p>
            <div class="columns is-multiline">
                <div class="column is-6">
                    <div class="field">
                        <label class="has-text-warning">First Name*</label>
                        <div class="control">
                            <input type="text" class="input bck-light-grey" v-model="first_name">
                        </div>
                    </div>
                    <div class="field">
                        <label class="has-text-warning">Last Name*</label>
                        <div class="control">
                            <input type="text" class="input bck-light-grey" v-model="last_name">
                        </div>
                    </div>
                    <div class="field">
                        <label class="has-text-warning">Email*</label>
                        <div class="control">
                            <input type="email" class="input bck-light-grey" v-model="email">
                        </div>
                    </div>
                    <div class="field">
                        <label class="has-text-warning">Mpesa Number*</label>
                        <div class="control">
                            <input type="text" class="input bck-light-grey" v-model="phone">
                        </div>
                    </div>
                    <div class="field">
                        <label class="has-text-warning">Delivery Address*</label>
                        <div class="control">
                            <input type="text" class="input bck-light-grey" v-model="place">
                        </div>
                    </div>
                </div>
            </div>
                <div id="card-element" class="mb-5"></div>
                <template v-if="cartTotalLength">
                    <hr>
                    <button class="button is-black has-text-primary mr-4" @click="submitPayRequest" v-bind:class="{'is-loading':this.$store.state.isLoading}">Pay now with Mpesa</button>

                    <button class="button is-black has-text-info" @click="submitNoPayRequest" v-bind:class="{'is-hidden': this.$store.state.isLoading}"> Pay on delivery</button>
                </template>
        </div>
    </div>
</template>
<script>
import axios from 'axios'
export default {
    name: 'Checkout',
    data(){
        return{
            cart:{
                items:[]
            },
            first_name:'',
            last_name:'',
            email:'',
            phone:'',
            address:'',
            zipcode:'',
            place:'',
            payNow: true
            
            
        }
    },
    mounted(){
        document.title = 'Checkout | Official Boots'
        this.cart = this.$store.state.cart
        if (this.cartTotalLength > 0){
            //create mpesa instance
        }

    },
    methods:{
        getItemTotal(item){
            return item.quantity * item.product.price
        }, 
        submitPayRequest(){
           
            if (this.valid_inputs()){
                this.$store.commit('setIsLoading',true)
                this.payNow = true
                this.sendPayRequest()
                
            }
        },
        submitNoPayRequest(){
            if (this.valid_inputs()){
                this.$store.commit('setIsLoading', true)
                this.payNow = false
                this.sendPayRequest()
            }
        },
        valid_inputs(){
            if (this.first_name === ''){
                this.$store.dispatch('dispatchError', 'The First Name is missing')
            }
            if (this.last_name === ''){
                this.$store.dispatch('dispatchError', 'The Last Name is missing')
            }
            if (this.place === ''){
                this.$store.dispatch('dispatchError', 'The delivery address is missing')
            }
            return !this.$store.state.errors.length
        },
        async sendPayRequest(){
            const items = []
            for (let i = 0; i < this.cart.items.length; i++){
                const item = this.cart.items[i]
                const obj = {
                    product: item.product.id,
                    quantity: item.quantity,
                    price: item.product.price * item.quantity
                }
                items.push(obj)
            }
            const data ={
                'first_name': this.first_name,
                'last_name': this.last_name,
                'email': this.email,
                'delivery_address': this.place,
                'phone': this.phone,
                'items': items,
                'payNow': this.payNow
            }
            await axios
                .post('api/v1/checkout/',data)
                .then(response=>{
                    this.$store.commit('clearCart')
                    if (sessionStorage.getItem('checkoutRequestID')){
                        sessionStorage.removeItem('checkoutRequestID')
                        sessionStorage.setItem('checkoutRequestID', response.data.CheckoutRequestID)
                    } else{
                        sessionStorage.setItem('checkoutRequestID', response.data.CheckoutRequestID)
                    }
                    console.log(response.data.CheckoutRequestID)
                    this.$router.push('/order/confirm')
                    
                })/** can  do better error handling  */
                .catch(error=>{
                    this.$store.dispatch('dispatchError','something went wrong. please log in and try again')
                    console.log(error)
                })
                this.$store.commit('setIsLoading', false)
        }
    },
    computed: {
        cartTotalLength(){
            return this.cart.items.reduce((acc, curVal) => {
                return acc += curVal.quantity
            }, 0)
        },
        cartTotalPrice(){
            return this.cart.items.reduce((acc, curVal) =>{
                return acc += curVal.quantity * curVal.product.price
            },0)
        },
        awaiting_pay(){
            return this.$store.state.isLoading
        }
    }
}
</script>
<style scoped>
    .bck-grey{
      background-color:#363636;
    }
    .bck-light-grey{
        background-color: #999DA0;
    }
</style>