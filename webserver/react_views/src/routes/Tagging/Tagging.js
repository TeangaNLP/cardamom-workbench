import { useEffect, useState } from 'react';
import { NavBar, POSToken } from '../../components';
import { Button } from 'react-bootstrap';
import { useNavigate, useLocation } from "react-router-dom";
import posTags from './tags';

import 'bootstrap/dist/css/bootstrap.css';
import "./Tagging.css";
import axios from 'axios';

const Tagging = ({ fileInfo, user, setUser }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const activeLink = location.pathname;
  let [fetched, setFetched] = useState(false); // For fetching data once.
  let [tokenData, setTokenData] = useState([]); // For tokens (not tags).
  let [tokensAndGaps, setTokensAndGaps] = useState([]); // For tokens and gaps.
  let [tags, setTags] = useState({}); // For saving and UI.
  let [cascaderData, setCascaderData] = useState([]); // For Cascader lookup.
  let [reverseLookup, setReverseLookup] = useState([]); // For reverse lookup.
  // let [fileState, setFileState] = useState({}); // To main router file state.

  useEffect(() => {

    if (!fetched) {
      axios
        .get("http://localhost:5001/api/pos_tag/" + fileInfo.file_id)
        .then(function (response) {
          createCascaderData();
          response.data.annotations = response.data.annotations.map( 
            (t) => {
                return {...t}  
            })
          combineTokensAndGaps(
            response.data.annotations,
            fileInfo.content
          );
          setTokenData(response.data.annotations);
          setTags(response.data.tags);
          setFetched(true);
        })
        .catch(function (err) {
          console.log(err);
        });
    }
  }, []);

  // Functionality
  // Update the state of the token with a tag.
  const updateTagState = (tokenId, tag) => {
    setTags({ ...tags, [tokenId]: tag });
  }

  // Create data for Cascader from hardcoded list.
  // TODO: Reverse Lookup names have clashing values, need fix.
  const createCascaderData = () => {
    let data = [];
    let reverseLookup = {};
    let i = 1;
    for (let key of Object.keys(posTags)) {
      let currentData = posTags[key]
      let j = 1;
      let childrenData = [];
      for (let childKey of Object.keys(currentData)) {
        let childData = currentData[childKey]
        let grandChildrenData = [];
        for (let k = 0; k < childData.length; k++) {
          let grandChildObj = {
            value: i.toString() + "-" + j.toString() + "-" + (k + 1).toString(),
            label: childData[k]
          }
          grandChildrenData.push(grandChildObj);
        }
        let childObj = {
          value: i.toString() + "-" + j.toString(),
          label: childKey,
          children: grandChildrenData
        }
        childrenData.push(childObj);
        j += 1;
      }
      let keyObj = {
        value: i.toString(),
        label: key,
        children: childrenData
      }
      reverseLookup[keyObj.label] = keyObj.value;
      data.push(keyObj);
      i += 1;
    }
    setCascaderData(data);
    setReverseLookup(reverseLookup);
    console.log(reverseLookup);
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
          let end_index = 
              start_index > currData.start_index
                ? start_index
                : currData.start_index;
          gaps.push({
            start_index: start_index,
            end_index: end_index,
            index: 0,
            type_: "gap",
            text: text.substring(start_index, end_index )
          });
        }
        // For end
        if (i == data.length - 1) {
          if (currData.end_index != text.length) {
            let start_index = currData.end_index;
            let end_index = start_index > text.length ? start_index : text.length;
            gaps.push({
              start_index: start_index,
              end_index: end_index, 
              index: data.length,
              type_: "gap",
              text: text.substring(start_index, end_index )
            });
          }
        }
        continue;
      }

      if (i == 0) {
        if (currData.start_index != 0) {
          let start_index = 0;
          let end_index = start_index > currData.start_index
                ? start_index
                : currData.start_index;
          gaps.push({
            start_index: start_index,
            end_index: end_index,
            index: 0,
            type_: "gap",
            text: text.substring(start_index, end_index )
          });
          // continue;
        }
      }

      if (i == data.length - 1) {
        if (currData.end_index != text.length) {
          let start_index = currData.end_index;
          let end_index = start_index > text.length ? start_index : text.length;
          gaps.push({
            start_index: start_index,
            end_index: end_index, 
            index: data.length,
            type_: "gap",
            text: text.substring(start_index, end_index )
          });
          // continue;
        }
      }

      if (nextData && currData.end_index != nextData.start_index) {
        let start_index = currData.end_index;
        let end_index = start_index > nextData.start_index
              ? start_index
              : nextData.start_index;
        gaps.push({
          start_index: start_index,
          end_index: end_index,
          index: i + 1,
          type_: "gap",
          text: text.substring(start_index, end_index )
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
      let start_index = 0;
      let end_index = text.length
      const gap = {
        start_index: start_index,
        end_index: end_index,
        index: 0,
        type_: "gap",
        text: text.substring(start_index, end_index )
    };
    newTokensAndGaps.push(gap);
  }
    setTokensAndGaps(newTokensAndGaps);
    window.gapsntokens = newTokensAndGaps; 
  };

  // Send annotations to server.
  const saveTags = () => {
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

  // Update Auto-tags;
  const updateAutoTags = (posTags) => {
    let newTags = { ...tags };
    for (let tag of posTags) {
      let tokenId = tag.token_id;
      // If type_ is auto but key does not exist then update.
      if (!newTags.hasOwnProperty(tokenId)) {
        newTags[tokenId] = tag;
      } else {
        // If type_ it auto and key exists and tag is auto then update.
        let oldTag = tags[tokenId];
        if (oldTag.type_ === "auto") {
          newTags[tokenId] = tag;
        }
      }
    }
    setTags(newTags);
  }

  // Auto-tag
  const autoTag = () => {
    const data = new FormData();
    window.sentTokens = JSON.stringify(tokenData);
    window.sentFile = JSON.stringify(fileInfo);
    window.sentRawContent = JSON.stringify(fileInfo.content);
    data.append("tokens", JSON.stringify(tokenData));
    data.append("file_data", JSON.stringify(fileInfo));
    /**/
    axios
      .post("http://localhost:5001/api/auto_tag", data, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then(function (response) {
        const posTags = response.data.POS;
        window.newAutoTags = posTags;
        updateAutoTags(posTags);
      })
      .catch(function (e) {
        console.log(e);
        console.log("Could not auto tag.");
      });
  }

  // Convert tags into their values.
  const convertTags = (tag) => {
    console.log(tag, tag.hasOwnProperty("features"))
    if (!tag.hasOwnProperty("features") || tag["features"].length == 0) {
      return [reverseLookup[tag["tag"]]]
    } else {
      let values = [];
      for (let feature of tag["features"]) {
        values.push(reverseLookup[feature["value"]]);
      }
      return values;
    }
  }

  return (
    <div>
      <NavBar setUser={setUser} pages={[{ path: "/", name: "Home" }, { path: "/fileupload", name: "File Upload" }]} />
      <NavBar main={false} pages={
        [
          { path: "/editor", name: "Text Editor" },
          { path: `/tokeniser/${fileInfo.file_id}`, name: "Tokenisation" },
          { path: "/identification", name: "Identification" },
          { path: "/annotation", name: "Annotation" },
          { path: activeLink, name: "POS Tagging" }
        ]
      } />
      <div className='tagging-area'>
        <div className="tagging-text">
          {fetched ? tokensAndGaps.map((token, i) => {
            const text = fileInfo.content;
            const tokenData = text.substring(token.start_index, token.end_index);
            console.log(token, tags);
            const tokenId = token.id;

            let tagList = []
            if (tags.hasOwnProperty(tokenId)) {
              const defaultTag = tags[tokenId];
              if (token.id === defaultTag.token_id) {
                tagList = convertTags(defaultTag);
              }
            }

            return (
              <POSToken
                key={i} defaultValue={tagList} cascaderData={cascaderData} updateTagState={updateTagState} token={token} tokenData={tokenData}
              />
            );
          }) : "Loading..."}
        </div>
      </div>
      <div className="tagging-area buttons">
        <Button className="button" onClick={autoTag} variant="dark">
          Auto-Tag
        </Button>
        <Button className="button" onClick={saveTags} variant="dark">Save</Button>
      </div>
    </div>
  );
};
export default Tagging;
