<template>
    <div class="page-sign-up">
        <div class="columns">
            <div class="column is-4 is-offset-4">
                <h1 class="title has-text-primary">Log In</h1>
                <form @submit.prevent="submitForm">
                    <div  class="field">
                    <label class="has-text-info">Username:</label>
                        <div class="control">
                            <input type="text" class="input" v-model= "username">
                        </div>
                    </div>
                    <div  class="field">
                    <label class="has-text-info">Password:</label>
                        <div class="control">
                            <input type="password" class="input" v-model= "password">
                        </div>
                    </div>
                    <div class="notification is-danger" v-if="errors.length">
                        <p v-for="error in errors" v-bind:key="error">{{ error }}</p>

                    </div>
                    <div class="field">
                        <div class="control">
                            <button class="button is-dark">Log In</button>
                        </div>

                    </div>
                    <hr>
                    <p class="has-text-warning">
                        Or <router-link class="has-text-success" to="/sign-up">click here </router-link>to sign up!
                    </p>
                </form>
            </div>
        </div>
    </div>
</template>
<script>
import axios from 'axios'
import { toast } from 'bulma-toast'
export default{
    name: 'LogIn',
    data(){
        return{
            username:'',
            password:'',
            errors:[]
        }
    },
    mounted(){
        document.title = 'Log In | Official Boots'
    },
    methods:{
       async submitForm(){
           axios.defaults.headers.common["Authorization"] = ""
           localStorage.removeItem("token")
           const formData = {
               username:this.username,
               password:this.password
           }
           await axios
            .post("api/v1/token/login/", formData)
            .then(response=>{
                const token = response.data.auth_token
                // console.log("This is the token:")
                // console.log(token)
                this.$store.commit('setToken',token)
                axios.defaults.headers.common["Authorization"] = "Token " + token
                localStorage.setItem("token", token)
                const toPath = this.$route.query.to || '/cart'     
                this.$router.push(toPath)      
            })
            .catch(error=>{
                if (error.response){
                            for (const property in error.response.data){
                                this.errors.push(`${property}: ${error.response.data[property]}`)
                            }
                            console.log(JSON.stringify(error.response.data))
                        } else if (error.message){
                            this.errors.push('Something went wrong. Please try again')
                            console.log(JSON.stringify(error.message))
                        }
            })
        }
            
    }
}
</script>
<style scoped>
.bck-light-grey{
    background-color: #999DA0;
}
</style>