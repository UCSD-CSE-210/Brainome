import React from 'react'
import { render } from 'react-dom'
import GraphComponent from '../components/graphComponent'
import configureStore from '../stores/store'
import { Provider } from 'react-redux'
import { Router, Redirect, browserHistory } from 'react-router';
import { syncHistoryWithStore } from 'react-router-redux';
import routes from '../routes';

let initialState = {

}


let store = configureStore(initialState);
const history = syncHistoryWithStore(browserHistory, store);

render(
  <Provider store={store}>
      <Router history={history}>
          <Redirect from="/" to="graphs" />
          {routes}
      </Router>
  </Provider>,
  document.getElementById('app') 
)
