<template>
    <tr>
        <td><router-link :to ="item.product.get_absolute_url" class="has-text-warning">{{ item.product.name }}</router-link></td>
        <td>{{ item.product.price }}</td>
        <td>{{ item.quantity }}
            <a @click="decrementQuantity(item)" class="ml-2 mr-2 has-text-danger">-</a>
            <a @click="incrementQuantity(item)" class="has-text-primary">+</a>
        </td>

        <td>{{ getItemTotal(item).toFixed(2) }}</td>
        <td><button class="delete" @click="removeFromCart(item)"></button></td>
    </tr>
</template>
<script>
export default {
    name: 'CartItem',
    props:{
        initialItem: Object
    },
    data(){
        return {
            item: this.initialItem
        }
    },
    methods: {
        getItemTotal(item){
            return item.quantity * item.product.price
        },
        decrementQuantity(item){
            item.quantity -= 1
            if (item.quantity === 0){
                this.$emit('removeFromCart', item)
            }
            this.updateCart()
        },
        incrementQuantity(item){
            item.quantity += 1
            this.updateCart()
        }, 
        updateCart(){
            localStorage.setItem('cart', JSON.stringify(this.$store.state.cart))
        },
        removeFromCart(item){
            this.$emit('removeFromCart', item)
            this.updateCart()
        }
    },
}
</script>