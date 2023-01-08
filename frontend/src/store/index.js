import { createStore } from 'vuex'

export default createStore({
	state: {
		token: '',
		isLoading: false,
		permissions: {},
	},
	getters: {
	},
	mutations: {
		setIsLoading(state, status) {
			state.isLoading = status
		},
	},
	actions: {
	},
	modules: {
	}
})