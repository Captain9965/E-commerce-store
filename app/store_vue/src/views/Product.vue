<template>
  <div class="page-product">
      <div class="columns is-multiline">
          <div class="column is-9">
              <figure class="image mb-6">
                  <img v-bind:src="product.get_image">
              </figure>
              <h1 class="title has-text-warning">{{product.name}}</h1>
              <p class="has-text-primary-dark">{{product.description}}</p>
          </div>
          <div class="column is-3">
              <h2 class="subtitle has-text-warning">Information</h2>
              <p class="has-text-primary-dark"><strong class="has-text-warning">Price: </strong>Ksh.{{product.price}}</p>
              <div class=" mt-4 select is-rounded">
                <select v-model="size">
                    <option v-for="i in [39, 40, 41, 42, 43, 44, 45]">{{i}}</option>
                </select>
              </div>
              <div class="field has-addons mt-6">
                  <div class="control">
                        <input type="number" class="input" min="1" v-model="quantity" >
                    </div>
                  <div class="control">
                      <a class="button is-dark" @click="addToCart">Add to cart</a>
                  </div>
              </div>
          </div>
      </div>
  </div>  
</template>
<script>
import axios from 'axios'
import { toast } from 'bulma-toast'
export default{
    name: 'Product',
    data(){
        return {
            product:{},
            quantity: 1,
            size: 39
        }
    },
    mounted(){
        this.getProduct()
    },
    methods:{
        /* read more on Promises, async, await*/
       async getProduct() {
            this.$store.commit('setIsLoading', true)
            const category_slug = this.$route.params.category_slug
            const product_slug = this.$route.params.product_slug
            await axios
            .get(`api/v1/products/${category_slug}/${product_slug}`)
            .then(response =>{
                this.product = response.data
                document.title = this.product.name + ' | Official Boots Kenya'
            })
            .catch(error =>{
                console.log(error)
            })
            this.$store.commit('setIsLoading', false)
        },
        addToCart(){
            if (isNaN(this.quantity)|| this.quantity < 1){
                this.quantity = 1
            }
            if (isNaN(this.size) || this.size < 39){
                this.quantity = 39
            }
            const item = {
                product : this.product,
                quantity : this.quantity,
                size : this.size
            }
            this.$store.commit('addToCart', item)
            toast({
                message: 'The product has been to the cart',
                type : 'is-success',
                dismissible : true,
                pauseOnHover : true,
                duration : 2000,
                position : 'bottom-right',
            })
        }
    }
}
</script>