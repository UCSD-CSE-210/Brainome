import React from 'react';
import { Route } from 'react-router';

import UserLoginContainer from './containers/userLoginContainer';
import GraphComponent from './components/graphComponent';

export default (
    <Route path="/" component={App}>
         <Route path="login" component={UserLoginContainer} />
        <Route path="graphs" component={GraphComponent} />
    </Route>
);