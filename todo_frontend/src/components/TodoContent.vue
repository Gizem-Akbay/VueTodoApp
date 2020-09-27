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
          required
        ></v-text-field>
        <!--
        <v-textarea
          v-model="todoData.content"
          label="Content"
          hint="Content Text"
        ></v-textarea> -->
        <wysiwyg v-model="todoData.content" />
        <v-combobox
            v-if="todoData.id"
            v-model="todoData.label_todo"
            :items="all_labels"
            chips
            label="Labels"
            multiple
            prepend-icon="mdi-label"
            @input="changed_label"
        >
            <template v-slot:selection="{ attrs, item, select, selected }">
              <v-chip
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
        <v-btn
          depressed
          color="primary"
          @click="save"
        >
          Save
        </v-btn>
      </v-form>
      <h3 v-else>
        Please select todo
      </h3>
    </v-sheet>
</template>

<script>

import TodoService from '../services/TodoService';

export default{
    name:'TodoContent',
    data: () => ({
        valid : true,
        has_param: false,
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
        save () {
            if (this.$refs.form.validate()) {
                TodoService.new_todo(this.todoData)
                    .then(res => {
                        this.$store.dispatch('get_todos');
                        this.$router.replace({name : 'Todo', params: {'todo_id': res.data.id}}).catch(() => {});
                    });
            }          
        },
        init_todo () {
            var param_id = this.$route.params.todo_id;
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
</style>