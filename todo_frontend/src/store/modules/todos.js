import TodoService from '../../services/TodoService';

const state = {
  todos: [],
  shared_todos: []
};

const actions = {
  get_todos({commit}) {
    TodoService.get_todos()
      .then(res => {
        commit('add_todos', res.data);
      });
  },
  get_shared_todos({commit}) {
    TodoService.get_shared_todos()
      .then(res => {
        commit('add_shared_todos', res.data);
      });
  }
};

const mutations = {
  add_todos (state, data) {
    state.todos = data;
  },
  add_shared_todos (state, data) {
    state.shared_todos = data;
  }
};

const getters = {
  todos () {
    return state.todos;
  },
  shared_todos () {
    return state.shared_todos;
  }
};

export default {
  state,
  actions,
  mutations,
  getters
};
