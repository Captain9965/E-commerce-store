<template>
    <div class="page-my-account">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title has-text-primary"> My Account</h1>
            </div>
            <div class="column is-12">
                <button @click="logout()" class="button is-danger"> Log Out</button>
            </div>
            <hr>
            <div class="column is-12">
                <h2 class="subtitle has-text-primary">My Orders</h2>
                <OrderSummary
                    class="bck-grey"
                    v-for="order in orders"
                    v-bind:key="order.id"
                    v-bind:order="order"
                />
            </div>
        </div>
    </div>
</template>
<script>
import OrderSummary from '@/components/OrderSummary.vue'
import axios from 'axios'
export default {
    name: 'MyAccount',
    components: {
        OrderSummary
    },
    data(){
        return {
            orders: []
        }
    },
    mounted(){
        document.title = 'My Account | Official Boots'
        this.getMyOrders()
    },
    methods:{
        logout(){
            axios.defaults.headers.common["Authorization"] = ""
            localStorage.removeItem("token")
            localStorage.removeItem("username")
            localStorage.removeItem("userid")
            this.$store.commit('removeToken')
            this.$router.push('/')
        },
       async getMyOrders(){
            this.$store.commit('setIsLoading', true)
            await axios 
                .get('/api/v1/orders/')
                .then(response=>{
                    this.orders = response.data
                })
                .catch(error=>{
                    console.log(error)
                })
            this.$store.commit('setIsLoading', false)
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