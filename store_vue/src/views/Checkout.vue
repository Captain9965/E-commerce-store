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
                            <td>Ksh.{{getItemTotal(item).toFixed(2)}}</td>
                       </tr>
                    </tbody>
                    <tfoot>
                        <tr>
                            <td colspan="2" class="has-text-warning">Total</td>
                            <td class="has-text-warning">{{cartTotalLength}}</td>
                            <td class="has-text-warning">Ksh.{{cartTotalPrice.toFixed(2)}}</td>
                        </tr>
                    </tfoot>
                </table>
                <p v-else> No items to check out....</p>
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
                        <label class="has-text-warning">Phone Number*</label>
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
             <div class="notification is-danger mt-4" v-if="errors.length">
                    <p v-for="error in errors" v-bind:key="error">{{error}}</p>
                </div>
                <div id="card-element" class="mb-5"></div>
                <template v-if="cartTotalLength">
                    <hr>
                    <button class="button is-black has-text-primary" @click="submitForm">Pay with Mpesa</button>
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
            stripe:{},
            card:{},
            first_name:'',
            last_name:'',
            email:'',
            phone:'',
            address:'',
            zipcode:'',
            place:'',
            errors:[]
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
        submitForm(){
            this.errors = []
            if (this.first_name === ''){
                this.errors.push('The First Name is missing')
            }
            if (this.last_name === ''){
                this.errors.push('The Last name is missing')
            }
            if (this.place === ''){
                this.errors.push('The delivery address is missing')
            }
            if (!this.errors.length){
                this.$store.commit('setIsLoading',true)
                // this.mpesa.createToken(this.phone).then(result=>{
                //     if(result.error){
                //         this.$store.commit('setIsLoading', false)
                //         this.errors.push('Something went wrong with mpesa. Please try again')
                //         console.log(result.error.message)
                //     } else{
                //         this.mpesaTokenHandler(result.token)
                //     }
                // })
                const testToken = {
                    id: '239596js'
                }
                this.mpesaTokenhandler(testToken)
                
            }
        },
        async mpesaTokenhandler(token){
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
                'transaction_id': token.id
            }
            await axios
                .post('api/v1/checkout/',data)
                .then(response=>{
                    this.$store.commit('clearCart')
                    this.$router.push('/cart/success')
                })
                .catch(error=>{
                    this.errors.push('something went wrong. please try again')
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