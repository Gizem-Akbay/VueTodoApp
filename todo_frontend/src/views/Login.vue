<template>
  <v-main>
    <v-container
      class="fill-height"
      fluid
    >
      <v-row
        align="center"
        justify="center"
      >
        <v-col
          cols="12"
          sm="8"
          md="4"
        >
          <v-card class="elevation-12">
            <v-toolbar
              color="primary"
              dark
              flat
            >
              <v-toolbar-title>Login Todo App</v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <v-form>
                <v-text-field
                  label="Login"
                  name="login"
                  prepend-icon="mdi-account"
                  type="text"
                  v-model="auth_data.username"
                ></v-text-field>

                <v-text-field
                  id="password"
                  label="Password"
                  name="password"
                  prepend-icon="mdi-lock"
                  type="password"
                  v-model="auth_data.password"
                ></v-text-field>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn @click="goto_register">Register</v-btn>
              <v-btn color="primary" @click="login">Login</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script>

import auth from '../auth';

export default {
  data: () => ({
    auth_data: {
      username: '',
      password: ''
    }
  }),
  created () {
  },
  methods: {
    login () {
      auth.login(this, this.auth_data)
        .then(() => {
          this.$router.replace({'name': 'Todo'});
        }).catch(() => {
          alert('Username or password erorr');
        });
    },
    goto_register () {
      this.$router.push({'name': 'Register'});
    }
  }
}
</script>
