import { useEffect, useState } from 'react';
import { NavBar, POSToken } from '../../components';
import { Button } from 'react-bootstrap';

import 'bootstrap/dist/css/bootstrap.css';
import "./Tagging.css";
import axios from 'axios';

const Tagging = (props) => {

  let [fetched, setFetched] = useState(false);
  let [tokenData, setTokenData] = useState([])
  let [originalTokenData, setOriginalTokenData] = useState([]);
  let [tokensAndGaps, setTokensAndGaps] = useState([]);
  let [tags, updateTags] = useState([]);
  let [cascaderData, setCascaderData] = useState([]);
  let [taggedTokens, setTaggedTokens] = useState([]);
  let [reverseLookup, setReverseLookup] = useState([]);

  let posTags = {
    "ADJ": [],
    "ADP": [{
      "Type": ["NA", "PREP"],
      "Case": ["NA", "ACC", "DAT"],
      "Definite": ["NA", "DEF", "IND"],
      "Gender": ["NA", "MASC", "MASC NEUT", "NEUT", "FEM"],
      "Number": ["NA", "DUAL", "SING", "PLUR"],
      "Person": ["NA", "1", "2", "3"],
      "PRON": ["NA", "ART", "PRS"]
    }],
    "ADV": [],
    "AUX": [],
    "CCONJ": [],
    "DET": [],
    "INTJ": [],
    "NOUN": [],
    "NUM": [],
    "PART": [],
    "PRON": [],
    "PROPN": [],
    "PUNCT": [],
    "SCONJ": [],
    "SYM": [],
    "VERB": [],
    "X": []
  };

  // Create data for Cascader from hardcoded list.
  const createCascaderData = () => {
    let data = [];
    let reverseLookup = {};
    let i = 1;
    for (let key of Object.keys(posTags)) {
      let currentData = posTags[key]
      if (posTags[key].length > 0) {
        let childrenData = [];
        let j = 1;
        for (let childKey of Object.keys(currentData[0])) {
          let grandChildrenData = [];
          for (let k = 0; k < currentData[0][childKey].length; k++) {
            let grandChildData = {
              value: i.toString() + "-" + j.toString() + "-" + (k + 1).toString(),
              label: currentData[0][childKey][k]
            }
            reverseLookup[grandChildData.label] = grandChildData.value
            grandChildrenData.push(grandChildData);
          }
          let childData = {
            value: i.toString() + "-" + j.toString(),
            label: childKey,
            children: grandChildrenData
          }
          reverseLookup[childData.label] = childData.value
          childrenData.push(childData);
          j += 1;
        }
        let keyData = {
          value: i.toString(),
          label: key,
          children: childrenData
        }
        reverseLookup[keyData.label] = keyData.value
        data.push(keyData);
      } else {
        let keyData = {
          value: i.toString(),
          label: key,
        }
        reverseLookup[keyData.label] = keyData.value
        data.push(keyData);
      }
      i += 1;
    }
    setCascaderData(data);
    setReverseLookup(reverseLookup);
  }

  useEffect(() => {
    const fileId = props.fileInfo.fileId;
    const content = props.fileInfo.content;

    if (!fetched) {
      axios
        .get("http://localhost:5001/api/pos_tag/" + fileId)
        .then(function (response) {
          createCascaderData();
          setOriginalTokenData(response.data.annotations);
          combineTokensAndGaps(
            response.data.annotations,
            content
          );
          setTaggedTokens(response.data.tags);
          setFetched(true);
        })
        .catch(function (err) {
          console.log(err);
        });
    }

  }, []);

  // Update the state of the token with a tag.
  const updateTagState = (tokenId, tag) => {
    updateTags({ ...tags, [tokenId]: tag });
  }

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

  // Send annotations to server.
  const saveTags = (event) => {
    // let difference = tokenData.filter((x) => !originalTokenData.includes(x));
    // console.log(difference);
    const data = {
      tags: tags,
    };
    axios
      .post("http://localhost:5001/api/pos_tag", data, {
        headers: {
          "Content-Type": "application/json",
        },
      })
      .then(function (response) {
        console.log(response);
      })
      .catch(function (e) {
        console.log(e);
        console.log("Could not save.");
      });
  };

  // Convert tags into their values.
  const convertTags = (tag) => {
    console.log(reverseLookup);
    if (tag["features"].length == 0) {
      console.log(reverseLookup[tag["tag"]], tag["tag"]);
      return [reverseLookup[tag["tag"]]]
    } else {
      let values = [];
      for (let feature of tag["features"]) {
        console.log(reverseLookup[feature["value"]], feature["value"]);
        values.push(reverseLookup[feature["value"]]);
      }
      return values;
    }
  }

  return (
    <div>
      <NavBar pages={[{ path: "/", name: "Home" }, { path: "/fileupload", name: "File Upload" }]} />
      <NavBar main={false} pages={[{ path: "/tokeniser", name: "Tokenisation" }, { path: "/tagging", name: "POS Tagging" }]} />
      <div className='tagging-area'>
        <div className="tagging-text">
          {tokensAndGaps.map((token, i) => {
            const text = props.fileInfo.content;
            const tokenData = text.substring(token.start_index, token.end_index);

            let tagList = []
            if (taggedTokens.hasOwnProperty(tokenData)) {
              const defaultTags = taggedTokens[tokenData];
              tagList = convertTags(defaultTags);
            }

            console.log("taglist", tagList);

            return (
              <POSToken
                key={i} defaultValue={tagList} cascaderData={cascaderData} updateTagState={updateTagState} token={token} tokenData={tokenData}
              />
            );
          })}
        </div>
      </div>
      <div className="tagging-area buttons">
        <Button className="button" onClick={saveTags} variant="dark">Save</Button>
      </div>
    </div>
  );
};
export default Tagging;