import React from 'react';
import { Navigate } from 'react-router-dom';

function CheckCachedUser({ children, user, setUser, redirectTo }) {
    if( user !== null && user !== undefined && user.isAuth === true){
	    return <Navigate to={redirectTo} />;
    }
    else if( (user === null || user === undefined) && localStorage.getItem('user') !== null ){
	    const user = JSON.parse(localStorage.getItem('user')); 
	    setUser(user)
    }
    else{
	    return children 
    }
}

export default CheckCachedUser;
