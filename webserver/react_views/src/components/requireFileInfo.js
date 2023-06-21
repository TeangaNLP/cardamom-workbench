import React from 'react';
import { Navigate, useParams } from 'react-router-dom';

function RequireFileInfo({ children, user, fileInfo, setFileInfo, redirectTo }) {
    const { fileId } = useParams();
    if( user === null || user === undefined ){
	    return
    }
    else if( fileInfo !== null && fileInfo !== undefined ){
	    return children 
    }
    else if( (fileInfo === null || fileInfo === undefined) && user.documents 
	&& user.documents.find( e => e.filename == fileId !== undefined )
    	  ){
	    const fileInfo_data = user.documents.find( e => e.filename == fileId )
	    setFileInfo(fileInfo_data)
    }
    else{
	    return <Navigate to={redirectTo} />;
    }
}

export default RequireFileInfo;
