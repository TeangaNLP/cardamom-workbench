import axios from "axios";
import { useState, useRef } from "react";
import useClickOutside from "../utils/useClickOutside";
import "./Token.css";

export default function Token({
  downHandler,
  upHandler,
  deselectHandler,
  token,
  value,
}) {
  console.log(token);
  console.log("token above");
  const [isActive, setIsActive] = useState(false);
  // const [cursorPosition, setCursorPosition] = useState({
  //   x: 0,
  //   y: 0,
  //   visible: false,
  // });
  const [cursorPosition, setCursorPosition] = useState(null);

  // Custom hook that notifies when clicked outside this component.
  const ref = useRef();
  useClickOutside(ref, null, () => {
    deselectHandler();
  });

  const handleMouseDown = () => {
    downHandler(token.start_index);
  };

  const handleMouseUp = () => {
    upHandler(token.start_index);
  };

  // const handleOnClick = (e) => {
  //   const get_similar_words_url = process.env.REACT_APP_PORT
  //     ? `http://${process.env.REACT_APP_HOST}:${process.env.REACT_APP_PORT}/api/related_words/` +
  //       value
  //     : `https://${process.env.REACT_APP_HOST}/api/related_words/` + value;
  //   axios
  //     .get(get_similar_words_url)
  //     .then(function (response) {
  //       console.log(response);
  //     })
  //     .catch(function (err) {
  //       console.log(err);
  //     });
  // };
  const handleSpanClick = () => {
    // Clear cursor position when clicking outside a word
    setCursorPosition(null);
  };
  const handleSingleOnClick = (e, wordIndex) => {
    console.log(e);

    // console.log()
    setIsActive(!isActive);
    console.log("handle clikcs");
    const rect = e.target.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const characterWidth = rect.width / e.target.textContent.length;
    const offset = Math.round(x / characterWidth);

    setCursorPosition({ index: wordIndex, offset });
    // const get_similar_words_url = process.env.REACT_APP_PORT
    //   ? `http://${process.env.REACT_APP_HOST}:${process.env.REACT_APP_PORT}/api/related_words/` +
    //     value
    //   : `https://${process.env.REACT_APP_HOST}/api/related_words/` + value;
    // axios
    //   .get(get_similar_words_url)
    //   .then(function (response) {
    //     console.log(response);
    //   })
    //   .catch(function (err) {
    //     console.log(err);
    //   });
  };
  const handleWordClick = (e, wordIndex) => {
    const rect = e.target.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const characterWidth = rect.width / e.target.textContent.length;
    const offset = Math.round(x / characterWidth);

    setCursorPosition({ index: wordIndex, offset });
  };

  const words = value.split(" ").map((word, i) => (
    <span key={i} className="word" onClick={(e) => handleWordClick(e, i)}>
      {word}
    </span>
  ));

  return (
    <span
      ref={ref}
      className={`tag green ${token.type_} ${isActive ? "orange" : ""}`}
      style={{ position: "relative" }}
      onMouseDown={handleMouseDown}
      onMouseUp={handleMouseUp}
      onClick={(e) => handleSingleOnClick(e)}
    >
      {token.type_ == "manual"
        ? value.replace(/\\n/g, "\u000A")
        : value.replace(/\\n/g, "\u000A")}

      {cursorPosition !== null && (
        <span
          className="cursor"
          style={{
            position: "absolute",
            left: `${cursorPosition.offset * 8}px`,
            top: `${cursorPosition.index * 24}px`,
            width: "1px",
            height: "1em",
            backgroundColor: "black",
          }}
        ></span>
      )}
    </span>
  );
}
