import Vue from 'vue';
import VueRouter from 'vue-router';
import Todo from '../views/Todo.vue';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
// import Navbar from '/components/Navbar.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/:todo_id?',
    name:  'Todo',
    component: Todo
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  }
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
});

export default router;
