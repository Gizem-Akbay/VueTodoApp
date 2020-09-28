<template>
    <v-menu
        bottom
        min-width="200px"
        rounded
        offset-y
        >
        <template v-slot:activator="{ on }">
            <v-btn
                class="ml-4"
                icon
                x-large
                v-on="on"
                >
                <v-avatar
                    color="brown"
                    size="42"
                    >
                    <span class="white--text headline">{{user.username[0]}}</span>
                </v-avatar>
            </v-btn>
        </template>
        <v-card>
            <v-list-item-content class="justify-center">
                <div class="mx-auto text-center">
                    <v-avatar
                        color="brown"
                        >
                        <span class="white--text headline">{{user.username[0]}}</span>
                    </v-avatar>
                    <h3>{{user.username}}</h3>
                    <p class="caption mt-1">
                        {{user.email}}
                    </p>
                    <v-divider class="my-3"></v-divider>
                    <v-btn
                        @click="remove_user"
                        depressed
                        rounded
                        text
                        >
                        Remove User
                    </v-btn>
                </div>
            </v-list-item-content>
        </v-card>
    </v-menu>
</template>

<script>

import TodoService from '../services/TodoService';

export default {
    data : () => ({
    }),
    methods: {
        remove_user () {
            const todo_id = this.$route.params.todo_id;
            if (todo_id) {
                TodoService.delete_todo_user (todo_id, this.user.email)
                    .then(() => {
                        this.$emit('refresh', todo_id);
                    });
            }
        }
    },
    props: ['user']
}
</script>

<style>
</style>