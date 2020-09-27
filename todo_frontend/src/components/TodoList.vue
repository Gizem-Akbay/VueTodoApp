<template>
    <v-sheet rounded="lg">
      <v-list color="transparent">
        <v-list-item
          link
          color="grey lighten-4"
          @click="add"
        >
          <v-list-item-icon>
            <v-icon>mdi-plus</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>
              Add todo
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-divider class="my-2"></v-divider>

        <div class="text-center" v-if="$store.getters.todos.length === 0">
            <span class="overline pa-1">Not yet created any todo</span>
        </div>
        <v-list-item
          v-for="todo in $store.getters.todos"
          :key="todo.id"
          link
          @click="openTodo(todo.id)"
        >
          <v-list-item-content>
            <v-list-item-title :class='todo.status ? "selectedTodo" : ""'>
              {{ todo.title }}
            </v-list-item-title>
            <v-list-item-subtitle>
                {{todo.updated_at.slice(0,-17)}}
            </v-list-item-subtitle>
          </v-list-item-content>
          <v-list-item-action>  
          </v-list-item-action>
            <v-icon small @click.stop="delete_todo(todo)">mdi-delete</v-icon>
          <v-list-item-action>
            <v-checkbox @click.stop="update_status(todo)" :input-value="todo.status"></v-checkbox>
           </v-list-item-action>
        </v-list-item>
    </v-list>
    </v-sheet>
</template>

<script>

import TodoService from '../services/TodoService';

export default{
    name:'TodoList',
    data: () => ({
        todos: [],
        active :true
    }),
    created () {
        this.$store.dispatch('get_todos');
    },
    methods: {
        add () {
            this.$router.push({'name': 'Todo', 'params': {'todo_id': 'new'}}).catch(() => {});
        },
        openTodo (todo_id) {
            this.$router.push({'name': 'Todo', 'params': {'todo_id': todo_id}}).catch(() => {});
        },
        update_status (todo) {
            todo.status = !todo.status;
            TodoService.new_todo(todo)
                .then(res => {
                    console.log(res);
                    this.$store.dispatch('get_todos');
                });
        },
        delete_todo (todo) {
            var res = confirm('Are you sure to delete this todo?');
            if (res) {
             TodoService.delete_todo(todo.id)
                .then(() => {
                    if (this.$route.params.todo_id === todo.id) {
                        this.$router.replace({'name': 'Todo'});
                    }
                    this.$store.dispatch('get_todos');
                });
            }
        }
     }
}
</script>
<style>
    .selectedTodo{
        -webkit-text-decoration-line: line-through; /* Safari */
        text-decoration-line: line-through; 
    }
</style>
