import TodoService from '../../services/TodoService';

const state = {
  todos: []
};

const actions = {
  get_todos({commit}) {
    TodoService.get_todos()
      .then(res => {
        commit('add_todos', res.data);
      });
  }
};

const mutations = {
  add_todos (state, data) {
    state.todos = data;
  } 
};

const getters = {
  todos () {
    return state.todos;
  }
};

export default {
  state,
  actions,
  mutations,
  getters
};
