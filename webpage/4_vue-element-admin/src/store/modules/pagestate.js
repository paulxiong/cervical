const state = {
  pagestate: { }
}

const mutations = {
  SET_PAGE_STATE: (state, _pagestate) => {
    if (!state.pagestate[_pagestate.routerpath]) {
      state.pagestate[_pagestate.routerpath] = { }
    }
    state.pagestate[_pagestate.routerpath][_pagestate.subpath] = _pagestate
  }
}

const actions = {
  setPageState({ commit }, _pagestate) {
    commit('SET_PAGE_STATE', _pagestate)
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
