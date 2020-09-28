import Vue from 'vue';
const API_URL = 'http://127.0.0.1:8000/api/';

export default {
    new_user(data) {
        return Vue.axios.post(API_URL + 'newuser/', data);
    }
};
