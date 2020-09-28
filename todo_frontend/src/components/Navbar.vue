<template>
  <v-app-bar
    app
    color="white"
    flat
  >
    <v-container class="py-0 fill-height">
      <h3 style="margin-left:7px">VUE TODO APP</h3>
      <div style="margin-left : 155px">
      <router-link :to="{'name': 'Todo'}">
        <v-btn
          text
        >
          Home
        </v-btn>
      </router-link>
      <router-link :to="{'name': 'SharedTodo'}">
        <v-btn
          text
        >
          Shared To Me
        </v-btn>
      </router-link>
      </div>
      <v-spacer></v-spacer>
      <v-btn 
        @click="sign_out"
        text
      >
      SIGN OUT
      </v-btn>
    </v-container>
  </v-app-bar>
</template>

<script>

import auth from '../auth';

export default {
  name: "Navbar",
  data: function() {
    return {
    };
  },
  methods: { 
    sign_out (){
      auth.logout();
      this.$router.replace({name : 'Login'});
    }   
  },
  created() {
  },
};
</script>

<style>
</style>
