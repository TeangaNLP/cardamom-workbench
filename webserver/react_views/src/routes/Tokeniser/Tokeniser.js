import { useCallback, useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { Button } from "react-bootstrap";
import { NavBar, Token } from "../../components/";
import axios from "axios";

import "./Tokeniser.css";

const Tokeniser = () => {
  let [tokenData, setTokenData] = useState([]);
  let [originalTokenData, setOriginalTokenData] = useState([]);
  let [tokensAndGaps, setTokensAndGaps] = useState([]);
  let [fetched, setFetched] = useState(false);
  let [selecting, setSelecting] = useState({ mouseDown: false, mouseUp: false, rightClick: false, start: null, end: null, componentStartIndex: null });

  const location = useLocation();

  // Callback for saving
  const onEnter = useCallback((event) => {
    if (event.keyCode == 13 && selecting.start != null && selecting.end != null) {
      updateTokens(selecting.start, selecting.end);
      setSelecting({ mouseDown: false, mouseUp: false, rightClick: false, start: null, end: null, componentStartIndex: null });
    }
  }, [selecting]);

  useEffect(() => {
    const fileId = location.state.fileId;

    if (!fetched) {
      axios
        .get("http://localhost:5001/api/annotations/" + fileId)
        .then(function (response) {
          setOriginalTokenData(response.data.annotations);
          combineTokensAndGaps(response.data.annotations, location.state.content);
          setFetched(true);
        })
        .catch(function (err) {
          console.log(err);
        });
    }

    // https://stackoverflow.com/a/61740188/13082658
    document.addEventListener('keydown', onEnter);
    // Don't forget to clean up
    return function cleanup() {
      document.removeEventListener('keydown', onEnter);
    }
  }, [onEnter]);

  // Events

  const handleMouseDown = (index) => {
    selecting = setSelecting({
      ...selecting,
      mouseDown: true,
      mouseUp: false,
      componentStartIndex: index
    })
  }

  const handleMouseUp = (index) => {
    let selection = window.getSelection();
    let start = selecting.componentStartIndex + selection.anchorOffset;
    let end = index + selection.focusOffset;
    selecting = setSelecting({
      ...selecting,
      mouseUp: true,
      start: start,
      end: end
    });
    // updateTokens(start, end);
  }

  const deselect = () => {
    if (selecting.mouseUp && selecting.mouseDown && selecting.start && selecting.end) {
      setSelecting({ mouseDown: false, mouseUp: false, rightClick: false, start: null, end: null, componentStartIndex: null });
    }
  }

  // Functionality

  const updateTokens = (start, end) => {
    let i = 0;
    let replaceIndex = null;
    let replaceTokens = [];

    while (i < tokensAndGaps.length) {
      if (start >= tokensAndGaps[i].start_index && !(tokensAndGaps[i].end_index <= start)) {
        replaceIndex = i;
        while (end > tokensAndGaps[i].end_index) {
          replaceTokens.push(tokensAndGaps[i]);
          i += 1;
        }
        replaceTokens.push(tokensAndGaps[i]);
        break
      }
      i += 1;
    }

    // Remove tokens
    let changedTokens = [...tokenData]
    for (let replaceToken of replaceTokens) {
      changedTokens = changedTokens.filter(token => token !== replaceToken);
    }
    // Add new tokens
    const newToken = { 'token': location.state.content.substring(start, end), 'type': 'token', 'start_index': start, 'end_index': end, 'provenance': 1 }
    changedTokens.splice(replaceIndex, 0, newToken);
    // Sort array based on start index
    changedTokens.sort((a, b) => {
      return a.start_index - b.start_index;
    });
    // Update UI
    combineTokensAndGaps(changedTokens, location.state.content);
  }

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
            end_index: start_index > currData.start_index ? start_index : currData.start_index,
            index: 0,
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
            end_index: start_index > currData.start_index ? start_index : currData.start_index,
            index: 0,
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
          });
          // continue;
        }
      }

      if (nextData && currData.end_index != nextData.start_index) {
        let start_index = currData.end_index;
        gaps.push({
          start_index: start_index,
          end_index: start_index > nextData.start_index ? start_index : nextData.start_index,
          index: i + 1,
        });
      }
    }

    let newTokensAndGaps = [...data];
    let originalLength = newTokensAndGaps.length;
    for (let gap of gaps) {
      newTokensAndGaps.splice((newTokensAndGaps.length - originalLength) + gap.index, 0, gap);
    }

    if (data.length == 0 && newTokensAndGaps.length == 0) {
      const gap = {
        start_index: 0,
        end_index: text.length,
        index: 0,
      }
      newTokensAndGaps.push(gap);
    }

    setTokenData(data);
    setTokensAndGaps(newTokensAndGaps);
  };

  // Buttons

  const autoTokenise = () => {

    const data = new FormData()
    data.append("data", location.state.content);

    axios
      .post("http://localhost:5001/api/auto_tokenise", data, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then(function (response) {
        combineTokensAndGaps(response.data.annotations, location.state.content);
      })
      .catch(function (e) {
        console.log(e);
        console.log("Could not tokenise");
      });
  }

  const saveTokens = (event) => {
    let difference = tokenData.filter(x => !originalTokenData.includes(x));
    console.log(difference);
    const data = {
      "tokens": difference,
      "file_id": location.state.fileId
    }
    axios
      .post("http://localhost:5001/api/annotations", data, {
        headers: {
          "Content-Type": "application/json",
        },
      })
      .then(function (response) {
        console.log(response);
      })
      .catch(function (e) {
        console.log(e);
        console.log("Could not tokenise");
      });
  };

  return (
    <div>
      <NavBar />
      <div onKeyPress={onEnter} className="tokenise-area">
        <div className="tokenise-text">
          {
            tokensAndGaps.map(token => {
              let text = location.state.content;
              let backgroundColour = token.type ? "yellow" : "transparent";
              let tokenValue = text.substring(token.start_index, token.end_index);
              return (
                <Token downHandler={handleMouseDown} upHandler={handleMouseUp} deselectHandler={deselect} colour={backgroundColour} token={token} value={tokenValue} />
              )
            })
          }
        </div>
      </div>
      <div className="tokenise-area buttons">
        <div>{selecting.mouseDown && !selecting.mouseUp ? <div>Selecting...</div> : selecting.mouseDown && selecting.mouseUp ? <div>Text Selected!</div> : <div>Nothing Selected!</div>}</div>
        <Button className="button" onClick={autoTokenise} variant="dark">
          Auto-Tokenise
        </Button>
        <Button className="button" onClick={saveTokens} variant="dark">
          Save
        </Button>
      </div>
    </div>
  );
};
export default Tokeniser;
