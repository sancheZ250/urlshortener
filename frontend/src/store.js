import { createStore } from 'vuex';

const store = createStore({
  state: {
    token: localStorage.getItem('token') || null,
    userId: localStorage.getItem('userId') || null,
    username: localStorage.getItem('username') || null,
    isAdmin: JSON.parse(localStorage.getItem('isAdmin')) || false, // Add isAdmin
  },
  mutations: {
    setUserId(state, userId) {
      state.userId = userId;
      localStorage.setItem('userId', userId);
    },
    setUsername(state, username) {
      state.username = username;
      localStorage.setItem('username', username);
    },
    setToken(state, token) {
      state.token = token;
      localStorage.setItem('token', token);
    },
    setIsAdmin(state, isAdmin) { // Add mutation for isAdmin
      state.isAdmin = isAdmin;
      localStorage.setItem('isAdmin', isAdmin);
    },
    clearUserId(state) {
      state.userId = null;
      localStorage.removeItem('userId');
    },
    clearUsername(state) {
      state.username = null;
      localStorage.removeItem('username');
    },
    clearToken(state) {
      state.token = null;
      localStorage.removeItem('token');
    },
    clearIsAdmin(state) { // Add mutation for clearing isAdmin
      state.isAdmin = false;
      localStorage.removeItem('isAdmin');
    },
  },
  actions: {
    login({ commit }, { userId, username, token, isAdmin }) {
      commit('setUserId', userId);
      commit('setUsername', username);
      commit('setToken', token);
      commit('setIsAdmin', isAdmin); // Set isAdmin on login
    },
    logout({ commit }) {
      commit('clearUserId');
      commit('clearUsername');
      commit('clearToken');
      commit('clearIsAdmin'); // Clear isAdmin on logout
    },
  },
  getters: {
    getUserId: (state) => state.userId,
    getUsername: (state) => state.username,
    isAuthenticated: (state) => !!state.token,
    getToken: (state) => state.token,
    isAdmin: (state) => state.isAdmin, // Getter for isAdmin
  },
});

export default store;
