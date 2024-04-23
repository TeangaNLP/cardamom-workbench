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

  const handleOnClick = () => {
      const get_similar_words_url = process.env.REACT_APP_PORT ? `http://${process.env.REACT_APP_HOST}:${process.env.REACT_APP_PORT}/api/related_words/` + value: `https://${process.env.REACT_APP_HOST}/api/related_words/` + value
      axios
        .get(get_similar_words_url)
        .then(function (response) {
		console.log(response)
        })
        .catch(function (err) {
          console.log(err);
        });
    }

  return (
    /*
    <input
      ref={ref}
      className={`token ${token.type_}`}
      onMouseDown={handleMouseDown}
      onMouseUp={handleMouseUp}
      //onClick={handleOnClick}
      value={token.type_ == "manual" ?
        value.replace(/ /g, "⎵").replace(/\\n/g, "\u000A") :
        value.replace(/\\n/g, "\u000A")}
    />*/
    <span
      ref={ref}
      className={`token ${token.type_}`}
      onMouseDown={handleMouseDown}
      onMouseUp={handleMouseUp}
      onClick={handleOnClick}
    >
      {token.type_ == "manual" ?
        value.replace(/ /g, "⎵").replace(/\\n/g, "\u000A") :
        value.replace(/\\n/g, "\u000A")}
    </span>
  );
}
