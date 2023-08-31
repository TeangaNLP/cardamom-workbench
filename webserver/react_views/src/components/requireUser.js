import React from 'react';
import { Navigate } from 'react-router-dom';

function RequireUser({ children, user, setUser, redirectTo }) {
    if( user !== null && user !== undefined && user.isAuth === true){
	    return children 
    }
    else if( (user === null || user === undefined) && localStorage.getItem('user') !== null ){
	    const user = JSON.parse(localStorage.getItem('user')); 
	    setUser(user)
    }
    else{
	    return <Navigate to={redirectTo} />;
    }
}

export default RequireUser;
