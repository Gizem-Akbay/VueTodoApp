import router from '../router';
// import Vue from 'vue';

const LOGIN_URL = 'http://127.0.0.1:8000/api/token/';

export default {
  user: {
    authenticated: false
  },
  login (context,creds) {
    return new Promise((resolve, reject) => {
      context.$http.post(LOGIN_URL, creds).then(response => {
        console.log(response);
        if (response.status===200) {
          localStorage.setItem('access_token', response.data.access);
          this.user.authenticated = true;
          resolve(response);
        } else {
          reject(response);
        }
      }, error => {
        reject(error);
      });
    });
  },
  logout () {
    localStorage.removeItem('access_token');
    localStorage.removeItem('access_expires_at');
    this.user.authenticated = false;
  },
  clearAuth () {
    this.user.authenticated = false;
    localStorage.removeItem('access_token');
  },
  checkAuth () {
    var jwt = localStorage.getItem('access_token');
    if (jwt) {
      this.user.authenticated = true;
    } else {
      this.user.authenticated = false;
    }
  },
  getAuthHeader () {
    if (localStorage.getItem('access_token')) {
      return 'Bearer ' + localStorage.getItem('access_token');
    } else {
      return false;
    }
  },
  checkExpiredToken (response) {
    return new Promise(function (resolve) {
      if (response.status === 401) {
        this.clearAuth();
        router.go({'name': 'login'});
      }
      resolve(response);
    }.bind(this));  
  }
};