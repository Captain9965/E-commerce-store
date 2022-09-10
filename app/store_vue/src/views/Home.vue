<template>
  <div class="home">
    <section  class="hero is-medium has-background-black mb-6 semi-opaque">
      <div>
        <figure class="image is-3by2">
          <img src="../assets/Official_boots_Kenya_logo.jpeg">
        </figure>
      </div>
      <div class="hero-body has-text-centered">
        <p class="title mb=6 has-text-warning">
          Welcome to Official Boots Collection
        </p>
        <p class="subtitle has-text-warning">
          We offer the best value for your money!
        </p>
      </div>
    </section>
    <div class="columns is-multiline">
      <div class="column is-12">
        <h2 class="is-size-2 has-text-centered has-text-warning"> Latest stock </h2>
      </div>
      <ProductBox
        v-for = "product in latestProducts"
        v-bind:key = "product.id"
        v-bind:product = "product"
      />
  </div>
  </div>
</template>

<script>
import axios from 'axios'
import ProductBox from '@/components/ProductBox.vue'

export default {
  name: 'Home',
  data(){
    return{
      latestProducts:[]
    }
  },
  components: {
    ProductBox
  },
  mounted(){
    this.getLatestProducts()
    document.title = 'Home | Official Boots Kenya'
  },
  methods:{
    getLatestProducts(){
      axios
      .get('/api/v1/latest-products')
      .then(response =>{
        this.latestProducts = response.data
      })
      .catch(error =>{
        console.log(error)
      })
    }
  }
}
</script>
<style>
.semi-opaque{
  opacity: .7;
}
</style>