<template>
    <v-sheet min-height="70vh" rounded="lg">
        <v-form
            v-if="has_param"
            class="pa-4"
            ref="form"
            v-model="valid"
            lazy-validation
            >
            <v-text-field
                v-model="todoData.title"
                :rules="nameRules"
                label="Title"
                hide-details
                solo
                class="mb-4"
                required
                ></v-text-field>
            <wysiwyg style="height: 60vh" placeholder="Your Todo" v-model="todoData.content" />
            <v-combobox
                v-if="todoData.id && router_name === 'Todo'"
                v-model="todoData.label_todo"
                dense
                hide-details
                solo
                :items="all_labels"
                chips
                label="Labels"
                multiple
                prepend-inner-icon="mdi-label"
                class="mt-4"
                @input="changed_label"
                >
                <template v-slot:selection="{ attrs, item, select, selected }">
                    <v-chip
                        small
                        v-bind="attrs"
                        :input-value="selected"
                        close
                        @click="select"
                        @click:close="remove_label(item)"
                        >
                        <strong>{{ item }}</strong>
                    </v-chip>
                </template>
            </v-combobox>
            <v-card-actions>
                <div v-if="todoData.id && router_name === 'Todo'" style="display: flex">
                    <h1 style="cursor: pointer" class="overline pt-3" @click="show_user_input = !show_user_input">Add User</h1>
                    <v-expand-transition>
                        <div v-show="show_user_input">
                            <v-text-field  
                                hide-details
                                solo
                                dense
                                append-icon="mdi-send"
                                @click:append="add_todo_user"
                                placeholder="User Email"
                                v-model="user_value"
                                class="ml-4 mt-2"
                                ></v-text-field>
                        </div>
                    </v-expand-transition>
                    <todo-user :key="user.id" @refresh="get_todo_by_id" :user="user" v-for="user in todoData.assigned_users"></todo-user>
                </div>
                <v-spacer></v-spacer>
                <v-btn
                    class=""
                    depressed
                    color="primary"
                    @click="save"
                    >
                    Save
                </v-btn>
            </v-card-actions>
        </v-form>
        <div v-else class="d-flex align-center justify-center">
            <h1 class="overline mt-8">
                Please select todo
            </h1>
        </div>
    </v-sheet>
</template>

<script>
import TodoService from '../services/TodoService';
import TodoUser from './TodoUser';
export default{
    name:'TodoContent',
    components : {
        'todo-user' : TodoUser
    },
    data: () => ({
        valid : true,
        has_param: false,
        show_user_input: false,
        user_value: '',
        router_name: 'Todo',
        nameRules: [
            v => !!v || 'Title is required',
            v => (v && v.length >= 2) || 'Title must be bigger than 1 characters',
        ],
        all_labels: [],
        selected_labels: [],
        todoData: {
            title: '',
            content: ''
        }
    }),
    created () {
        this.init_todo();
    },
    methods: {
        get_todo_by_id (todo_id) {
            TodoService.get_todo(todo_id)
                .then(res => {
                    this.todoData = res.data;
                });

            TodoService.get_all_labels()
                .then(res => {
                    this.all_labels = res.data;
                });
        },
        add_todo_user () {
            const data = {email: this.user_value};
            TodoService.add_todo_user(this.todoData.id, data).
                then(() => {
                    this.get_todo_by_id(this.todoData.id);
                    this.user_value = '';
                    alert('User added');
                }).catch(err => {
                    if (err.response.status === 404) {
                        alert('User Email not found');
                        this.user_value = '';
                    }
                });
        },
        save () {
            if (this.$refs.form.validate()) {
                TodoService.new_todo(this.todoData)
                    .then(res => {
                        this.$store.dispatch('get_todos');
                        this.$router.replace({name : this.router_name, params: {'todo_id': res.data.id}}).catch(() => {});
                    });
            }          
        },
        init_todo () {
            var param_id = this.$route.params.todo_id;
            this.router_name = this.$route.name;
            if (!param_id) {
                this.has_param = false;
            } else {
                if (param_id === 'new') {
                    this.todoData = {
                        title: '',
                        content: ''
                    };
                } else {
                    this.get_todo_by_id(param_id);
                }
                this.has_param = true;
            }            
        },
        remove_label (todo) {
            var index = this.todoData.label_todo.indexOf(todo);
            if (index !== -1) {
                this.todoData.label_todo.splice(index, 1);
                this.changed_label();
            }
        },
        changed_label(){
            var todo_id = this.$route.params.todo_id;
            const data = {'labels': this.todoData.label_todo};
            TodoService.add_label(todo_id, data)
            .then(() => {
                });
        }
    },
    watch: {
        '$route' () {
            this.init_todo();
        }
    }
}
</script>

<style>
@import "~vue-wysiwyg/dist/vueWysiwyg.css";
.editr--toolbar {
    background: #eeeeee61 !important;
}
</style>
