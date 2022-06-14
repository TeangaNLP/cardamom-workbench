import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { Button } from "react-bootstrap";
import { NavBar } from "../../components/";
import axios from "axios";

import "./Tokeniser.css";




const Tokeniser = () => {
  let [tokens, setTokens] = useState([]);
  let [contentOffsets, setContentOffsets] = useState([]);

  const location = useLocation();

  useEffect(() => {
    const fileId = location.state.fileId;

    axios
      .get("http://localhost:5001/api/annotations/" + fileId)
      .then(function (response) {
        console.log(response);
        setTokens({
          annotations: response.data.annotations,
          content: location.state.content,
        });

        combineTokensAndGaps(response.data.annotations, location.state.content)

  
      })
      .catch(function (err) {
        console.log(err);
      });
  }, []);

  
  
  const saveTokens = (event) => {
    console.log(event);
  };

  const combineTokensAndGaps = (data, text) => {
    let tokens = data;
    let gaps = [];
    console.log(tokens.length)
    for (let i = 0; i < tokens.length; i++) {
      let currToken = tokens[i];
      let nextToken = tokens[i + 1];
      let ifContinue = false;
      console.log(currToken, nextToken, i)
      if (i == 0) {
        console.log("Inside 0")
        if (currToken.start_index != 0) {
          gaps.push({
            "start_index": 0,
            "end_index": currToken.start_index - 1,
            "index": 0
          });
          continue
        }
      }
      console.log(i == tokens.length - 1)
      if (i == tokens.length - 1) {
        console.log("Inside 1")
        if (currToken.end_index != text.length) {
          gaps.push({
            "start_index": currToken.end_index + 1,
            "end_index": text.length - 1,
            "index": tokens.length
          });
          continue
        }
      }
      
      if (currToken.end_index != nextToken.start_index) {
        gaps.push({
          "start_index": currToken.end_index + 1,
          "end_index": nextToken.start_index - 1,
          "index": i + 1
        });
      }
    }
    let newTokens = [...tokens];
    let gapSum = 0;
    for(let gap of gaps){
      newTokens.splice(gapSum + gap.index, 0, gap); 
      gapSum += gap.index;
    }
    console.log(newTokens);
  }

  return (
    <div>
      <NavBar />
      <div className="tokenise-area">
        {/* <textarea className="tokenise-text" defaultValue={data}></textarea> */}
      </div>
      <div className="tokenise-area save-button">
        <Button onClick={saveTokens} variant="dark">
          Save
        </Button>
      </div>
    </div>
  );
};
export default Tokeniser;
