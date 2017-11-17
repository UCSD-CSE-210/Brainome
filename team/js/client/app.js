import React from 'react'
import { render } from 'react-dom'
import Ensemble from '../containers/ensembleTabularContainer'
import configureStore from '../stores/store'
import { Provider } from 'react-redux'

let initialState = {
 test:{
 	data:"Yella My React Redux App is on"
 }
}


let store = configureStore(initialState)
console.log("updated")
render(
    <Provider store={store}>
        <Ensemble />
    </Provider>,
    document.getElementById('app') 
)
