<template>
    <div class="box mb-4">
        <h3 class="has-text-warning is-size-4 mb-6">Order #{{order.id}}</h3>
        <h4 class="has-text-warning is-size-5 mb-4">Products</h4>
        <table class="bck-grey has-text-warning table is-fullwidth">
            <thead>
                <tr>
                    <th class="has-text-info">Product</th>
                    <th class="has-text-info">Price</th>
                    <th class="has-text-info">Quantity</th>
                    <th class="has-text-info">Size</th>
                    <th class="has-text-info">Total</th>
                    <th ></th>
                </tr>
            </thead>
            <tbody class="has-text-warning">
                <tr
                    v-for="item in order.items"
                    v-bind:key="item.product.id"

                >
                    <td>{{ item.product.name }}</td>
                    <td>{{ item.product.price }}</td>
                    <td>{{ item.quantity }}</td>
                    <td>{{item.size}}</td>
                    <td>Ksh.{{ parseInt(getItemTotal(item))}}</td>
                </tr>
            </tbody>
            <tfoot>
                <tr>
                    <td colspan="2" class="has-text-warning">Total</td>
                    <td class="has-text-warning">{{orderTotalLength(order)}}</td>
                    <td></td>
                    <td class="has-text-warning">Ksh.{{orderTotalPrice(order)}} </td>
                </tr>
            </tfoot>
        </table>
        <div>
    
            <button class="button is-black has-text-primary" @click="submitPayRequest" v-if="paymentPending" v-bind:class="{'is-loading': localLoading}"> Pay Now / confirm</button>
            <h2 v-else-if="orderDelivered" class="subtitle has-text-info"> Enjoy your shoes!</h2>
            <h2 v-else class="subtitle has-text-primary"> Your order will be delivered within 24 hrs</h2>
        </div>
    </div>
</template>
<script>
    import axios from 'axios'
export default {
    name: 'OrderSummary',
    data(){
        return{
            localLoading: false
        }
    },
    props:{
        order:Object
    },
    methods:{
        getItemTotal(item){
            return item.quantity * item.product.price
        },
        orderTotalLength(order){
            return order.items.reduce((acc, curVal) =>{
                return acc +=curVal.quantity
            },0)
        },
        orderTotalPrice(order){
            return order.items.reduce((acc, curVal)=>{
                return parseInt(acc += (curVal.product.price * curVal.quantity))
            },0)
        },
        async submitPayRequest(){
            this.$store.dispatch('dispatchInfo','Sending request...')
            this.localLoading = true
            await axios
                .post('api/v1/order/pay/',this.order)
                .then(response=>{
                    if(response.data.CheckoutRequestID){
                        if (sessionStorage.getItem('checkoutRequestID')){
                            sessionStorage.removeItem('checkoutRequestID')
                            sessionStorage.setItem('checkoutRequestID', response.data.CheckoutRequestID)
                        } else{
                            sessionStorage.setItem('checkoutRequestID', response.data.CheckoutRequestID)
                        }
                        console.log(response.data.CheckoutRequestID)
                        this.$router.push('/order/confirm')
                    }
                    else if (response.data.Info){
                        console.log(response.data.Info)
                        this.$router.push('/order/success')
                    }
                    
                })
                /**@todo: how do I show errors on ui? */
                .catch(error=>{
                    this.$store.dispatch('dispatchError','Something went wrong, try again')
                    console.log(error)
                })
            this.localLoading = false
        }
    },
    computed:{
        paymentPending(){
            return !this.order.paid
        },
        sendingPayRequest(){
            return this.$store.state.isLoading
        },
        orderDelivered(){
            return this.order.delivered
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