import React from 'react';
import { Link } from 'react-router-dom';
import { Navbar, Nav } from 'react-bootstrap';

const NavigationBar = () => {
  return (
    <Navbar bg='dark' variant='dark'>
      <Navbar.Brand as={Link} to='/'>
        React Template
      </Navbar.Brand>
      <Nav>
        <Nav.Link as={Link} to='/component1'>
          Component1
        </Nav.Link>
        <Nav.Link as={Link} to='/component2'>
          Component2
        </Nav.Link>
      </Nav>
    </Navbar>
  );
};

export default NavigationBar;
