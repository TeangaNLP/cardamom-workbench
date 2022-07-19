import { useEffect, useState } from 'react';
import { NavBar, POSToken } from '../../components';
import { Button } from 'react-bootstrap';

import 'bootstrap/dist/css/bootstrap.css';
import "./Tagging.css";
import axios from 'axios';

const Tagging = (props) => {

  let [tokenData, setTokenData] = useState([])
  let [originalTokenData, setOriginalTokenData] = useState([]);
  let [tokensAndGaps, setTokensAndGaps] = useState([]);
  let [tags, updateTags] = useState([]);

  useEffect(() => {
    const fileId = props.fileInfo.fileId;
    const content = props.fileInfo.content;

    // Fetch annotations from server.
    axios
      .get("http://localhost:5001/api/annotations/" + fileId)
      .then(function (response) {
        setOriginalTokenData(response.data.annotations);
        combineTokensAndGaps(
          response.data.annotations,
          content
        );
      })
      .catch(function (err) {
        console.log(err);
      });
  }, []);

  // Update the state of the token with a tag.
  const updateTagState = (token, tag) => {
    console.log(token, tag)
    updateTags({ ...tags, [token]: tag });
  }

  console.log(tags);

  // Create Tokens for textarea.
  const combineTokensAndGaps = (data, text) => {
    let gaps = [];

    for (let i = 0; i < data.length; i++) {
      let currData = data[i];
      let nextData = data[i + 1];

      if (i == 0 && i == data.length - 1) {
        // For start
        if (currData.start_index != 0) {
          let start_index = 0;
          gaps.push({
            start_index: start_index,
            end_index:
              start_index > currData.start_index
                ? start_index
                : currData.start_index,
            index: 0,
            type: "gap",
          });
        }
        // For end
        if (i == data.length - 1) {
          if (currData.end_index != text.length) {
            let start_index = currData.end_index;
            gaps.push({
              start_index: start_index,
              end_index: start_index > text.length ? start_index : text.length,
              index: data.length,
              type: "gap",
            });
          }
        }
        continue;
      }

      if (i == 0) {
        if (currData.start_index != 0) {
          let start_index = 0;
          gaps.push({
            start_index: start_index,
            end_index:
              start_index > currData.start_index
                ? start_index
                : currData.start_index,
            index: 0,
            type: "gap",
          });
          // continue;
        }
      }

      if (i == data.length - 1) {
        if (currData.end_index != text.length) {
          let start_index = currData.end_index;
          gaps.push({
            start_index: start_index,
            end_index: start_index > text.length ? start_index : text.length,
            index: data.length,
            type: "gap",
          });
          // continue;
        }
      }

      if (nextData && currData.end_index != nextData.start_index) {
        let start_index = currData.end_index;
        gaps.push({
          start_index: start_index,
          end_index:
            start_index > nextData.start_index
              ? start_index
              : nextData.start_index,
          index: i + 1,
          type: "gap",
        });
      }
    }

    let newTokensAndGaps = [...data];
    let originalLength = newTokensAndGaps.length;
    for (let gap of gaps) {
      newTokensAndGaps.splice(
        newTokensAndGaps.length - originalLength + gap.index,
        0,
        gap
      );
    }

    if (data.length == 0 && newTokensAndGaps.length == 0) {
      const gap = {
        start_index: 0,
        end_index: text.length,
        index: 0,
        type: "gap",
      };
      newTokensAndGaps.push(gap);
    }

    setTokenData(data);
    setTokensAndGaps(newTokensAndGaps);
  };

  return (
    <div>
      <NavBar pages={[{ path: "/", name: "Home" }, { path: "/fileupload", name: "File Upload" }]} />
      <NavBar main={false} pages={[{ path: "/tokeniser", name: "Tokenisation" }, { path: "/tagging", name: "POS Tagging" }]} />
      <div className='tagging-area'>
        <div className="tagging-text">
          {tokensAndGaps.map((token, i) => {
            const text = props.fileInfo.content;
            const tokenData = text.substring(token.start_index, token.end_index);
            return (
              <POSToken
                key={i} updateTagState={updateTagState} token={token} tokenData={tokenData}
              />
            );
          })}
        </div>
      </div>
      <div className="tagging-area buttons">
        <Button className="button" variant="dark">Save</Button>
      </div>
    </div>
  );
};
export default Tagging;