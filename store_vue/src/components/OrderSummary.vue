<template>
    <div class="box mb-4">
        <h3 class="has-text-warning is-size-4 mb-6">Order #{{order.id}}</h3>
        <h4 class="has-text-warning is-size-5">Products</h4>
        <table class="bck-grey table is-fullwidth">
            <head class="has-text-warning">
                <tr>
                    <th>Product</th>
                    <th>Price</th>
                    <th>Quantity</th>
                    <th>Total</th>
                </tr>
            </head>
            <tbody class="has-text-warning">
                <tr
                    v-for="item in order.items"
                    v-bind:key="item.product.id"

                >
                    <td>{{ item.product.name }}</td>
                    <td>{{ item.product.price }}</td>
                    <td>{{ item.quantity }}</td>
                    <td>Ksh.{{ parseInt(getItemTotal(item))}}</td>
                </tr>
            </tbody>
            <tfoot>
                <tr>
                    <td colspan="2" class="has-text-warning">Total</td>
                    <td class="has-text-warning">{{orderTotalLength(order)}}</td>
                    <td class="has-text-warning">Ksh.{{orderTotalPrice(order)}} </td>
                </tr>
            </tfoot>
        </table>
        <div>
            <button class="button is-black has-text-primary" @click="submitPayRequest" v-if="paymentPending"> Pay Now with Mpesa</button>
        </div>
    </div>
</template>
<script>
    import axios from 'axios'
export default {
    name: 'OrderSummary',
    data(){
        return{
            errors: [],
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
            this.errors = []
            this.$store.commit('setIsLoading', true)
            console.log("Sending request with order")
            console.log(this.order)
            await axios
                .post('api/v1/order/pay/',this.order)
                .then(response=>{
                    this.$router.push('/cart/success/')
                })
                /**@todo: show errors on ui */
                .catch(error=>{
                    this.errors.push('something went wrong. please try again')
                    console.log(error)
                })
            this.$store.commit('setIsLoading', false)
        }
    },
    computed:{
        paymentPending(){
            return !this.order.paid
        },
        sendingPayRequest(){
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