import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import { Provider } from 'react-redux';
import store from './store';
import App from './App';
import NavigationBar from './components/NavigationBar/NavigationBar';
import Component1 from './components/Component1/Component1';
import Component2 from './components/Component2/Component2';
import NotFound from './errros/NotFound/NotFound';

const routing = (
  <Router>
    <Provider store={store}>
      <NavigationBar />
      <Switch>
        <Route exact path='/' component={App} />
        <Route path='/component1' component={Component1} />
        <Route path='/component2' component={Component2} />
        <Route component={NotFound} />
      </Switch>
    </Provider>
  </Router>
);

ReactDOM.render(routing, document.getElementById('root'));
