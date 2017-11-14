import React from 'react'
import { render } from 'react-dom'
import GraphComponent from '../components/graphComponent'
import configureStore from '../stores/store'
import { Provider } from 'react-redux'

let initialState = {

}


let store = configureStore(initialState)

render(
  <Provider store={store}>
    <GraphComponent />
  </Provider>,
  document.getElementById('app') 
)
