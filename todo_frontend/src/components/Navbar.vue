<template>
  <v-app-bar
    app
    color="white"
    flat
  >
    <v-container class="py-0 fill-height">
      <h3>VUE TODO APP</h3>

      <div style="margin-left : 55px">
      <v-btn
        text
      >
        Home
      </v-btn>


      <v-btn
        text
      >
        Shared To Me
      </v-btn>
      </div>

      <v-spacer></v-spacer>

      <v-responsive max-width="260">
        <v-text-field
          dense
          flat
          hide-details
          rounded
          solo-inverted
        ></v-text-field>
      </v-responsive>
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