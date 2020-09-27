import Vue from 'vue';
const API_URL = 'http://127.0.0.1:8000/api/';

export default {
	get_all_labels () {
		return Vue.axios.get(API_URL + 'labels/');
	},
	get_todo_labels (todo_id) {
		return Vue.axios.get(API_URL + 'labels/todo/' + todo_id + '/');
	},
	add_label (todo_id,data) {
		return Vue.axios.put(API_URL + 'labels/todo/' + todo_id + '/' , data);
	},
	delete_label () {
	},
	add_todo () {
	},
	delete_todo (todo_id) {
		return Vue.axios.delete(API_URL + 'todos/' + todo_id + '/');
	},
	get_todos () {
		return Vue.axios.get(API_URL + 'todos/');
	},
	get_todo (todo_id) {
		return Vue.axios.get(API_URL + 'todos/' + todo_id + '/');
	},
	new_todo (data) {
		return Vue.axios.put(API_URL + 'todos/', data);
	}
};
