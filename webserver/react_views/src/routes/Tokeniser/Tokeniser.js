import { useCallback, useEffect, useState } from "react";
import { Button } from "react-bootstrap";
import { NavBar, Token } from "../../components/";
import axios from "axios";

import "./Tokeniser.css";

const Tokeniser = (props) => {
  let [tokenData, setTokenData] = useState([]);
  let [originalTokenData, setOriginalTokenData] = useState([]);
  let [tokensAndGaps, setTokensAndGaps] = useState([]);
  let [fetched, setFetched] = useState(false);
  let [fileState, setFileState] = useState({});
  let [selecting, setSelecting] = useState({
    mouseDown: false,
    mouseUp: false,
    rightClick: false,
    start: null,
    end: null,
    componentStartIndex: null,
  });

  // Callback for saving
  const onEnter = useCallback(
    (event) => {
      if (
        event.keyCode == 13 &&
        selecting.start != null &&
        selecting.end != null
      ) {
        updateManualTokens(selecting.start, selecting.end);
        setSelecting({
          mouseDown: false,
          mouseUp: false,
          rightClick: false,
          start: null,
          end: null,
          componentStartIndex: null,
        });
      }
    },
    [selecting]
  );

  useEffect(() => {
    // To check if file already selected before.
    const fileId = props.fileInfo.fileId;
    const content = props.fileInfo.content;
    setFileState({ fileId: fileId, content: content, langId: props.fileInfo.langId });

    if (!fetched) {
      axios
        .get("http://localhost:5001/api/annotations/" + fileId)
        .then(function (response) {
          setOriginalTokenData(response.data.annotations);
          combineTokensAndGaps(
            response.data.annotations,
            content
          );
          setFetched(true);
        })
        .catch(function (err) {
          console.log(err);
        });
    }

    // https://stackoverflow.com/a/61740188/13082658
    document.addEventListener("keydown", onEnter);
    // Don't forget to clean up
    return function cleanup() {
      document.removeEventListener("keydown", onEnter);
    };
  }, [onEnter]);

  // Events
  const handleMouseDown = (index) => {
    selecting = setSelecting({
      ...selecting,
      mouseDown: true,
      mouseUp: false,
      componentStartIndex: index,
    });
  };

  const handleMouseUp = (index) => {
    let selection = window.getSelection();
    let start = selecting.componentStartIndex + selection.anchorOffset;
    let end = index + selection.focusOffset;
    selecting = setSelecting({
      ...selecting,
      mouseUp: true,
      start: start,
      end: end,
    });
    // updateTokens(start, end);
  };

  const deselect = () => {
    if (
      selecting.mouseUp &&
      selecting.mouseDown &&
      selecting.start &&
      selecting.end
    ) {
      setSelecting({
        mouseDown: false,
        mouseUp: false,
        rightClick: false,
        start: null,
        end: null,
        componentStartIndex: null,
      });
    }
  };

  // Functionality
  const updateAutoTokens = (autoTokens) => {
    let changedTokens = [...tokenData];

    for (let autoToken of autoTokens) {
      let i = 0;
      let replaceIndex = null;
      let replaceTokens = [];

      let start = autoToken["start_index"];
      let end = autoToken["end_index"];

      while (i < tokensAndGaps.length) {
        if (
          tokensAndGaps[i].type != "manual" &&
          start >= tokensAndGaps[i].start_index &&
          !(tokensAndGaps[i].end_index <= start)
        ) {
          replaceIndex = i;
          while (end > tokensAndGaps[i].end_index) {
            replaceTokens.push(tokensAndGaps[i]);
            i += 1;
          }
          replaceTokens.push(tokensAndGaps[i]);
          break;
        }
        i += 1;
      }

      // Remove tokens
      for (let replaceToken of replaceTokens) {
        changedTokens = changedTokens.filter((token) => token !== replaceToken);
      }
      // Add token only if it replaces something (meaning that there is something to be changed).
      if (replaceTokens.length > 0)
        changedTokens.splice(replaceIndex, 0, autoToken);
    }
    // Sort array based on start index
    changedTokens.sort((a, b) => {
      return a.start_index - b.start_index;
    });
    // Update UI
    combineTokensAndGaps(changedTokens, fileState.content);
  };

  const updateManualTokens = (start, end) => {
    let i = 0;
    let replaceIndex = null;
    let replaceTokens = [];

    while (i < tokensAndGaps.length) {
      if (
        start >= tokensAndGaps[i].start_index &&
        !(tokensAndGaps[i].end_index <= start)
      ) {
        replaceIndex = i;
        while (end > tokensAndGaps[i].end_index) {
          replaceTokens.push(tokensAndGaps[i]);
          i += 1;
        }
        replaceTokens.push(tokensAndGaps[i]);
        break;
      }
      i += 1;
    }

    // Remove tokens
    let changedTokens = [...tokenData];
    for (let replaceToken of replaceTokens) {
      changedTokens = changedTokens.filter((token) => token !== replaceToken);
    }
    // Add new tokens
    const newToken = {
      type: "manual",
      start_index: start,
      end_index: end,
      provenance: 1,
    };
    changedTokens.splice(replaceIndex, 0, newToken);
    // Sort array based on start index
    changedTokens.sort((a, b) => {
      return a.start_index - b.start_index;
    });
    // Update UI
    combineTokensAndGaps(changedTokens, fileState.content);
  };

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

  // Return manual tokens.
  const getReservedTokens = () => {
    let reservedTokens = [];
    for (let token of tokenData) {
      if (token.type == "manual") {
        const t = {
          type: token.type,
          start_index: token.start_index,
          end_index: token.end_index,
          provenance: 1
        }
        reservedTokens.push(t)
      }
    }
    return reservedTokens
  }

  // Buttons
  const autoTokenise = () => {
    const data = new FormData();
    data.append("data", fileState.content);
    data.append("reservedTokens", JSON.stringify(getReservedTokens()));
    data.append("lang_id", fileState.langId);

    axios
      .post("http://localhost:5001/api/auto_tokenise", data, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then(function (response) {
        updateAutoTokens(response.data.annotations);
      })
      .catch(function (e) {
        console.log(e);
        console.log("Could not tokenise");
      });
  };

  const saveTokens = (event) => {
    let difference = tokenData.filter((x) => !originalTokenData.includes(x));
    const data = {
      tokens: difference,
      file_id: fileState.fileId
    };
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
      <NavBar pages={[{ path: "/", name: "Home" }, { path: "/fileupload", name: "File Upload" }]} />
      <NavBar main={false} pages={
        [
          { path: "/editor", name: "Text Editor" },
          { path: "/tokeniser", name: "Tokenisation" },
          { path: "/identification", name: "Identification" },
          { path: "/annotation", name: "Annotation" },
          { path: "/tagging", name: "POS Tagging" }
        ]
      } />
      <div onKeyPress={onEnter} className="tokenise-area">
        <div className="tokenise-text">
          {fetched ? tokensAndGaps.map((token) => {
            const text = fileState.content;
            const tokenValue = text.substring(token.start_index, token.end_index)
            return (
              <Token
                downHandler={handleMouseDown}
                upHandler={handleMouseUp}
                deselectHandler={deselect}
                token={token}
                value={tokenValue}
              />
            );
          }) : "Loading..."}
        </div>
      </div>
      <div className="tokenise-area buttons">
        <div>
          {selecting.mouseDown && !selecting.mouseUp ? (
            <div>Selecting...</div>
          ) : selecting.mouseDown && selecting.mouseUp ? (
            <div>Text Selected!</div>
          ) : (
            <div>Nothing Selected!</div>
          )}
        </div>
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
