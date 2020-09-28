import Vue from 'vue';
import VueRouter from 'vue-router';
import Todo from '../views/Todo.vue';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: {
      required_authorization: false
    }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: {
      required_authorization: false
    }
  },
  {
    path: '/:todo_id?',
    name:  'Todo',
    component: Todo,
    meta: {
      type: 'todo',
      required_authorization: true 
    }
  },
  {
    path: '/shared/:todo_id?',
    name:  'SharedTodo',
    component: Todo,
    meta: {
      type: 'shared',
      required_authorization: true 
    }
  }
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
});

export default router;
