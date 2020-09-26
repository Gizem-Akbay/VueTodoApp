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
              <v-toolbar-title>Register Todo App</v-toolbar-title>
            </v-toolbar>
            <v-card-text>
               <v-form
                  ref="form"
                  v-model="valid"
                  lazy-validation
                >
                <v-text-field
                  label="Username"
                  :rules="nameRules"
                  name="username"
                  prepend-icon="mdi-account"
                  type="text"
                  v-model="register_data.username"
                ></v-text-field>

                <v-text-field
                  label="Email"
                  :rules="emailRules"
                  name="email"
                  prepend-icon="mdi-account"
                  type="text"
                  v-model="register_data.email"
                ></v-text-field>

                <v-text-field
                  id="password"
                  :rules="passwordRules"
                  label="Password"
                  name="password"
                  prepend-icon="mdi-lock"
                  type="password"
                  v-model="register_data.password"
                ></v-text-field>

                <v-text-field
                  id="password"
                  :rules="re_passwordRules"
                  label="Repeat Password"
                  name="re_password"
                  prepend-icon="mdi-lock"
                  type="password"
                  v-model="register_data.re_password"
                ></v-text-field>

              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" @click="regsiter">Register</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script>

import RegisterService from '../services/RegisterService';

export default {
  data: () => ({
    register_data: {
      username: '',
      email : '',
      password: '',
      re_password: ''
    },
    valid: true,
    nameRules: [
      v => !!v || 'Name is required',
      v => (v && v.length > 2) || 'Name must be bigger than 2 characters'
    ],
    emailRules: [
      v => !!v || 'E-mail is required',
      v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
    ],
    passwordRules: [
      v => !!v || 'password is required',
      v => (v && v.length >= 6) || 'Password must be bigger than 6 characters'
    ]
  }),
  created () {
  },
  computed: {
    re_passwordRules () {
      return [
        v => !!v || 'Repeat password is required',
        v => (v && v === this.register_data.password) || 'Passwords must be equals.'
      ]
    }
  },
  methods: {
    regsiter () {
      if (this.$refs.form.validate()) {
        RegisterService.new_user(this.register_data)
          .then((response) => {
            if (response.status) {
              this.$router.push({'name': 'Login'});
            }
          }).catch (() => {
            alert('Something went be wrong, Please try again later');
          });
      } else {
        alert('Please check form');
      }
    }
  }
}
</script>