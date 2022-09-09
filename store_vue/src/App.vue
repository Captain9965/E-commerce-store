<template>
 <div class="wrapper bck-image container-flex">
   <nav class="navbar is-dark">
     <div class="navbar-brand">
       <router-link to="/" class="navbar-item">
        <i class="fas fa-light fa-shoe-prints"></i>
        <i class="ml-2"></i>
        <strong class="has-text-warning">Official Boots Collection</strong>
       </router-link>
       <a class="navbar-burger bck-dark" aria-label="menu" aria-expanded="false" data-target="navbar-menu" @click="showMobileMenu = !showMobileMenu">
         <span aria-hidden="true"></span>
         <span aria-hidden="true"></span>
         <span aria-hidden="true"></span>
       </a>
     </div>
     <div class="navbar-menu" id="navbar-menu" v-bind:class="{'is-active':showMobileMenu,'bck-dark': showMobileMenu}">
       <div class="navbar-start">
         <div class="navbar-item">
           <form method="get" action="/search">
           <div class="field has-addons">
             <div class="control">
               <input type="text" class="input" placeholder="what are you looking for?" name="query">
             </div>
             <div class="control">
               <button class="button is-success">
                 <span class="icon">
                   <i class="fas fa-search"></i>
                 </span>
               </button>
             </div>
          </div>
           </form>
         </div>
       </div>
       <div class="navbar-end">
          <router-link id="link1" to="/official" class="navbar-item has-text-primary">Official</router-link>
          <router-link id="link2" to="/casual" class="navbar-item has-text-primary">Casual</router-link>
         <div class="navbar-item">
           <div class="buttons">
             <template v-if="$store.state.isAuthenticated">
               <router-link to="/my-account" class="button is-light">My Account </router-link>
             </template>
             <template v-else>
               <router-link to="/log-in" class="button is-light">Log In</router-link>
             </template>
             <router-link to="/cart" class="button is-success">
             <span class="icon"> <i class="fas fa-shopping-cart"></i></span>
             <span>Cart ({{cartTotalLength}})</span>
             </router-link>
           </div>
         </div>   
       </div>
     </div>
   </nav>
   <div class="is-loading-bar has-text-centered" v-bind:class="{'is-loading':$store.state.isLoading}">
     <div class="lds-dual-ring">
     </div>
   </div>
   <section class="section section-flex">

    <router-view/>
    <div class="notification is-danger mt-4" v-if="this.$store.state.errors.length">
      <button class="delete" @click="clear_error"></button>
      <p v-for="error in this.$store.state.errors" v-bind:key="error">{{error}}</p>
    </div>
    <div class="notification is-success mt-4" v-if="this.$store.state.infos.length">
      <button class="delete" @click="clear_info"></button>
      <p v-for="info in this.$store.state.infos" v-bind:key="info">{{info}}</p>
    </div>
   </section>
   <footer class="pb-6">
     <p class="has-text-centered has-text-warning">Copyright (c) 2022</p>
   </footer>
 </div>
</template>
<script>
import axios from 'axios'
import { toast} from 'bulma-toast'
export default{
  data(){
    return{
      showMobileMenu:false,
    }
  },
  beforeCreate(){
    this.$store.commit('initializeStore')
    const token = this.$store.state.token
    if (token){
      axios.defaults.headers.common['Authorization'] = "Token"+ token
    }else{
      axios.defaults.headers.common['Authorization'] = ""
    }
  },
  computed:{
    cartTotalLength(){
      let totalLength = 0
      for (let i=0; i< this.$store.state.cart.items.length;i++){
        totalLength += this.$store.state.cart.items[i].quantity
      }
      return totalLength
    }
  },
  methods:{
    clear_info(){
      this.$store.commit('clearInfos')
    },
    clear_error(){
      this.$store.commit('clearErrors')
    }
  }
}
</script>
<style lang="scss">
@import '../node_modules/bulma';
.lds-dual-ring{
  display: inline-block;
  width: 80px;
  height: 80px;
}
.lds-dual-ring:after{
  content: "";
  display: block;
  height: 60px;
  margin: 8px;
  border-radius: 50%;
  border: 6px solid #ccc;
  border-color: #ccc transparent #ccc transparent;
  animation: lds-dual-ring 1.2s linear infinite;
}
@keyframes lds-dual-ring {
  0%{
    transform: rotate(0deg);
  }
  100%{
    transform: rotate(360deg);
  }
}
.is-loading-bar{
  height: 0;
  overflow: hidden;
  -webkit-transition: all 0.3s;
  transition: all 0.3s;

  &.is-loading{
    height: 80px;
  }
}
.bck-image{
  background-image: linear-gradient(rgba(0,0,0,0.9), rgba(0,0,0,0.9)),url("./assets/Official_boots_Kenya_logo.jpeg");
  height: 50%;
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
  position: relative;
  background-attachment: fixed;
}

.container-flex{
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
.section-flex{
  flex: 1;
}
.bck-dark{
  background-color:#2f2f2f;
}
#link1:hover,#link2:hover{
  background-color: black;
}
</style>