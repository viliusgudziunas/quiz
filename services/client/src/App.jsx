import React, { useState, useEffect } from "react";
import { Route, Switch } from "react-router-dom";
import UsersList from "./components/UsersList";
import About from "./components/About";
import NavBar from "./components/NavBar";
import Form from "./components/Form";
import Logout from "./components/Logout";
import UserStatus from "./components/UserStatus";

const App = () => {
  const [userAdded, setUserAdded] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    setUserAdded(false);
  }, [userAdded, isAuthenticated]);

  useEffect(() => {
    if (window.localStorage.getItem("authToken")) {
      setIsAuthenticated(true);
    }
  }, []);

  const [title] = useState("TestDrivenTutorial.io");

  return (
    <div>
      <NavBar title={title} isAuthenticated={isAuthenticated} />
      <section className="section">
        <div className="container">
          <div className="columns">
            <div className="is-half">
              <br />
              <Switch>
                <Route exact path="/" render={() => <UsersList />} />
                <Route exact path="/about" component={About} />
                <Route
                  exact
                  path="/status"
                  render={() => (
                    <UserStatus isAuthenticated={isAuthenticated} />
                  )}
                />
                <Route
                  exact
                  path="/register"
                  render={() => (
                    <Form
                      formType={"Register"}
                      isAuthenticated={isAuthenticated}
                      setIsAuthenticated={setIsAuthenticated}
                    />
                  )}
                />
                <Route
                  exact
                  path="/login"
                  render={() => (
                    <Form
                      formType={"Login"}
                      isAuthenticated={isAuthenticated}
                      setIsAuthenticated={setIsAuthenticated}
                    />
                  )}
                />
                <Route
                  exact
                  path="/logout"
                  render={() => (
                    <Logout setIsAuthenticated={setIsAuthenticated} />
                  )}
                />
              </Switch>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default App;
