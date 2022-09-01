<template>
    <div class="page-cart">
        <div class = "columns is-multiline">
            <div class = "column is-12">
                <h1 class="has-text-primary title">Cart</h1>
            </div>
            <div class="bck-grey column is-12 box">
                <table class="bck-grey has-text-warning table is-fullwidth" v-if="cartTotalLength">
                    <thead>
                        <tr>
                            <th class="has-text-warning">Product</th>
                            <th class="has-text-warning">Price</th>
                            <th class="has-text-warning">Quantity</th>
                            <th class="has-text-warning">Total</th>
                            <th ></th>
                        </tr>
                    </thead>
                    <tbody>
                        <CartItem
                            v-for = "item in cart.items"
                            v-bind:key = "item.product.id"
                            v-bind:initialItem ="item"
                            v-on:removeFromCart="removeFromCart"
                        />
                    </tbody>
                </table>
                <p v-else class="has-text-warning"> You dont have any products in your cart....</p>
            </div>
            <h2 class="subtitle has-text-primary">Summary</h2>
            <div class="has-text-warning bck-grey column is-12 box">
                <strong class="has-text-info">Ksh.{{ cartTotalPrice.toFixed(2)}}</strong> , {{ cartTotalLength }} items
                <hr>
                <router-link to="/cart/checkout" class="button is-black has-text-info">Proceed to checkout</router-link>
            </div>
        </div>
    </div>
</template>
<script>
import axios from 'axios'
import CartItem from '@/components/CartItem.vue'
export default{
    name : 'Cart',
    components:{
        CartItem
    },
    data(){
        return{
            cart:{
                items: []
            }
        }
    },
    methods:{
        removeFromCart(item){
            this.cart.items = this.cart.items.filter(i => i.product.id !== item.product.id)
        }
    },
    mounted(){
        this.cart = this.$store.state.cart
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