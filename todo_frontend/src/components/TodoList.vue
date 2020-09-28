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
            <div class="text-center" v-if="todo_list.length === 0">
                <span class="overline pa-1">Not yet created any todo</span>
            </div>
            <v-list-item
                v-for="todo in todo_list"
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
                <!-- TODO:: When click assigned user to unshared this todo -->
                <v-list-item-action v-if="router_name === 'Todo'">
                    <v-icon small @click.stop="delete_todo(todo)">mdi-delete</v-icon>
                </v-list-item-action>
                <span class="caption text--disabled" v-if="router_name === 'SharedTodo'">({{todo.user.username}})</span>
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
        router_name: 'Todo',
        active :true
    }),
    created () {
        this.get_todos();
    },
    computed: {
        todo_list () {
            if (this.router_name === 'Todo') {
                return this.$store.getters.todos;
            } else if (this.router_name == 'SharedTodo') {
                return this.$store.getters.shared_todos;
            } else {
                return [];
            }
        }
    },
    methods: {
        get_todos () {
            this.router_name = this.$route.name;
            if (this.router_name === 'Todo') {
                this.$store.dispatch('get_todos');
            } else if (this.router_name == 'SharedTodo') {
                this.$store.dispatch('get_shared_todos');
            }
        },
        add () {
            this.$router.push({'name': 'Todo', 'params': {'todo_id': 'new'}}).catch(() => {});
        },
        openTodo (todo_id) {
            this.router_name = this.$route.name;
            this.$router.push({'name': this.router_name, 'params': {'todo_id': todo_id}}).catch(() => {});
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
     },
     watch: {
        '$route' (val) {
            if (val.name == 'Todo' || val.name == 'SharedTodo') {
                this.router_name = val.name;
                this.get_todos();
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
