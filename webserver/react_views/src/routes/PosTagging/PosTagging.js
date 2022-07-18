import { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { NavBar, POSToken } from '../../components';
import { Button } from 'react-bootstrap';

import 'bootstrap/dist/css/bootstrap.css';
import "./POSTagging.css";

const POSTagging = () => {

  let [annoText, updateAnnoText] = useState([]);
  let [tags, updateTags] = useState([]);

  const location = useLocation();

  useEffect(() => {
    updateAnnoText(location.state.data);
  }, []);

  // Update the state of the token with a tag.
  const updateTagState = (token, tag) => {
    updateTags({ ...tags, [token]: tag });
  }

  console.log(tags);

  // Create Tokens for textarea.
  let data = [];
  for (let i = 0; i < annoText.length; i++) {
    data.push(<POSToken key={i} updateTagState={updateTagState} data={annoText[i]["token"]} />);
  }

  return (
    <div>
      <NavBar />
      <div className='annotation-area'>
        <div className="annotation-text">
          {data}
        </div>
      </div>
      <div className="annotation-area save-button">
        <Button variant="dark">Save</Button>
      </div>
    </div>
  );
};
export default POSTagging;
