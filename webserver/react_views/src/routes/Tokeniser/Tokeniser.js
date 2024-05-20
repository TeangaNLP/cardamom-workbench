import { useCallback, useEffect, useState } from "react";
import { useNavigate, useLocation, useParams } from "react-router-dom";
import { Button } from "react-bootstrap";
import { NavBar, Token } from "../../components/";
import axios from "axios";
import SideNavBar from "./../../components/SideNavBar/SideNavBar"; // Adjust the import based on

import "./Tokeniser.css";
import { Sidenav } from "rsuite";
import { Box } from "@mui/material";

const Tokeniser = ({ user }) => {
  const { fileId } = useParams();
  const file_id = fileId;
  console.log(user);
  const fileInfo = user.documents.find((e) => e.file_id == fileId);

  // getAll();÷
  const navigate = useNavigate();
  const location = useLocation();
  const activeLink = location.pathname;
  let [tokenData, setTokenData] = useState([]);
  let [originalTokenData, setOriginalTokenData] = useState([]);
  let [tokensAndGaps, setTokensAndGaps] = useState([]);
  let [fetched, setFetched] = useState(false);
  //let [fileInfo, setFileState] = useState({});
  let [selecting, setSelecting] = useState({
    mouseDown: false,
    mouseUp: false,
    rightClick: false,
    start: null,
    end: null,
    componentStartIndex: null,
  });

  const getAll = () => {
    const get_tokens_url = process.env.REACT_APP_PORT
      ? `http://${process.env.REACT_APP_HOST}:${process.env.REACT_APP_PORT}/api/annotations/` +
        fileInfo.file_id
      : `https://${process.env.REACT_APP_HOST}/api/annotations/` +
        fileInfo.file_id;
    axios
      .get(get_tokens_url)
      .then(function (response) {
        window.originaltokens = response.data.annotations;
        setOriginalTokenData(response.data.annotations);
        combineTokensAndGaps(response.data.annotations, fileInfo.content);
        setFetched(true);
      })
      .catch(function (err) {
        console.log(err);
      });
  };

  useEffect(() => {
    if (!fetched) {
      getAll();
    }
  }, []);

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
        resetMouseSelection();
      }
    },
    [selecting]
  );

  useEffect(() => {
    console.log("use effect", fileInfo);
    if (!fetched && fileInfo !== undefined) {
    }
    // To check if file already selected before.
    /*
    let file_id;
    let content;
    console.log(location.state);
    if (location.state === null) {
      file_id = props.fileInfo.file_id;
      content = props.fileInfo.content;
    } else if (props.fileInfo.file_id === null || location.state.file_id != props.fileInfo.file_id) {
      file_id = location.state.file_id;
      content = location.state.content;
      props.setFileInfo({
        file_id: file_id,
        content: location.state.content
      });
    }


    setFileState({ file_id: file_id, content: content });
    */

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

  const resetMouseSelection = () => {
    if (window.getSelection) {
      if (window.getSelection().empty) {
        // Chrome
        window.getSelection().empty();
      } else if (window.getSelection().removeAllRanges) {
        // Firefox
        window.getSelection().removeAllRanges();
      }
    } else if (document.selection) {
      // IE?
      document.selection.empty();
    }
  };

  const handleMouseUp = (index) => {
    let selection = window.getSelection();
    let start = selecting.componentStartIndex + selection.anchorOffset;
    let end = index + selection.focusOffset;
    // Flip for backward selection;
    if (start > end) {
      let temp = start;
      start = end;
      end = temp;
    }
    console.log(start, end);
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
          tokensAndGaps[i].type_ != "manual" &&
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
    combineTokensAndGaps(changedTokens, fileInfo.content);
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
      type_: "manual",
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
    combineTokensAndGaps(changedTokens, fileInfo.content);
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
            type_: "gap",
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
              type_: "gap",
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
            type_: "gap",
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
            type_: "gap",
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
          type_: "gap",
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
        type_: "gap",
      };
      newTokensAndGaps.push(gap);
    }

    setTokenData(data);
    setTokensAndGaps(newTokensAndGaps);
    window.tokensAndGaps = newTokensAndGaps;
  };

  // Return manual tokens.
  const getReservedTokens = () => {
    let reservedTokens = [];
    for (let token of tokenData) {
      if (token.type_ == "manual") {
        const t = {
          type_: token.type_,
          start_index: token.start_index,
          end_index: token.end_index,
          provenance: 1,
        };
        reservedTokens.push(t);
      }
    }
    return reservedTokens;
  };

  // Buttons
  const autoTokenise = () => {
    const data = new FormData();
    data.append("file_data", JSON.stringify(fileInfo));
    data.append("reservedTokens", JSON.stringify(getReservedTokens()));
    window.sentFileI = fileInfo;
    window.sentFileF = JSON.stringify(fileInfo);

    const post_auto_tokenize_url = process.env.REACT_APP_PORT
      ? `http://${process.env.REACT_APP_HOST}:${process.env.REACT_APP_PORT}/api/auto_tokenise`
      : `https://${process.env.REACT_APP_HOST}/api/auto_tokenise`;
    axios
      .post(post_auto_tokenize_url, data, {
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
      file_id: fileInfo.file_id,
    };

    const post_tokens_url = process.env.REACT_APP_PORT
      ? `http://${process.env.REACT_APP_HOST}:${process.env.REACT_APP_PORT}/api/annotations`
      : `https://${process.env.REACT_APP_HOST}/api/annotations`;
    axios
      .post(post_tokens_url, data, {
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
      {/* <NavBar
        setUser={setUser}
        pages={[
          { path: "/", name: "Home" },
          { path: "/fileupload", name: "File Upload" },
        ]}
      />
      <SideNavBar
        main={false}
        pages={[
          { path: "/editor", name: "Text Editor" },
          { path: `/tokeniser/${fileInfo.file_id}`, name: "Tokenisation" },
          { path: "/identification", name: "Identification" },
          { path: "/annotation", name: "Annotation" },
          { path: activeLink, name: "POS Tagging" },
        ]}
      /> */}
      <div className="remaining-box">
        <Box
          component="main"
          sx={{
            flexGrow: 1,
            p: 3,
            marginLeft: "240px", // Matches the Drawer width
            border: 1,
            borderColor: "grey.300",
            borderRadius: 1,
            boxShadow: 1,
          }}
        >
          <div onKeyPress={onEnter} className="tokenise-area">
            <div className="tokenise-text">
              {fetched
                ? tokensAndGaps.map((token) => {
                    const text = fileInfo.content;
                    const tokenValue = text.substring(
                      token.start_index,
                      token.end_index
                    );
                    return (
                      <Token
                        downHandler={handleMouseDown}
                        upHandler={handleMouseUp}
                        deselectHandler={deselect}
                        token={token}
                        value={tokenValue}
                      />
                    );
                  })
                : "Loading..."}
            </div>
          </div>
        </Box>
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
    </div>
  );
};
export default Tokeniser;
