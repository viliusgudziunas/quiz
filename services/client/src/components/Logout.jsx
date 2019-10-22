import React, { useEffect } from "react";
import { Link } from "react-router-dom";

const Logout = ({ setIsAuthenticated }) => {
  useEffect(() => {
    window.localStorage.clear();
    setIsAuthenticated(false);
  }, [setIsAuthenticated]);

  return (
    <div>
      <p>
        You are now logged out. Click <Link to="/login">here</Link> to log back
        in.
      </p>
    </div>
  );
};

export default Logout;
