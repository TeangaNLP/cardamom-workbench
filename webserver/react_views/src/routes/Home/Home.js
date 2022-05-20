import { useState } from 'react';
import { useLocation, Navigate } from 'react-router-dom';
import { ListGroup } from 'react-bootstrap';
import { NavBar } from '../../components';

import "./Home.css";

const Home = () => {

  const location = useLocation();
  const userAuthenticated = location.state;

  const alertClicked = () => {
    alert('You clicked the third ListGroupItem');
  }

  console.log(userAuthenticated);

  if (!userAuthenticated) {
    return <Navigate to="/login" replace={true} />
  }

  return (
    <div>
      <NavBar />
      <ListGroup className='list-item'>
        <ListGroup.Item action href="#link1">
          Document 1
        </ListGroup.Item>
        <ListGroup.Item action href="#link2">
          Document 2
        </ListGroup.Item>
        <ListGroup.Item action onClick={alertClicked}>
          Document 3
        </ListGroup.Item>
      </ListGroup>
    </div>
  );
}

export default Home