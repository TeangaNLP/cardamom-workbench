import { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { Button } from 'react-bootstrap';
import { NavBar } from '../../components/';

import "./Tokeniser.css";

const Tokeniser = () => {

  let [annoText, updateAnnoText] = useState([]);

  const location = useLocation();

  useEffect(() => {
    updateAnnoText(location.state.data);
  }, []);

  // Create Tokens for textarea.
  let data = '';
  for (let i = 0; i < annoText.length; i++) {
    data += `${annoText[i]["token"]} `;
  }

  return (
    <div>
      <NavBar />
      <div className='tokenise-area'>
        <textarea className="tokenise-text" defaultValue={data}>
        </textarea>
      </div>
      <div className="tokenise-area save-button">
        <Button variant="dark">Save</Button>
      </div>
    </div>
  );
};
export default Tokeniser;
