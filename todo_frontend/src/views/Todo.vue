<template>
  <v-app id="inspire">
    <nav-bar></nav-bar>
    <v-main class="grey lighten-3">
      <v-container>
        <v-row>
          <v-col cols="3">
            <todo-list></todo-list>
          </v-col>
          <v-col>
            <todo-content></todo-content>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>

import Navbar from '../components/Navbar';
import TodoList from '../components/TodoList';
import TodoContent from '../components/TodoContent';

export default {
  name: 'Todo',
  data: () => ({
  }),
  created () {
  },
  components:{
    'nav-bar': Navbar,
    'todo-list':TodoList,
    'todo-content':TodoContent,
  }
}
</script>
