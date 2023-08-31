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

  return (
    <span
      ref={ref}
      className={`token ${token.type_}`}
      onMouseDown={handleMouseDown}
      onMouseUp={handleMouseUp}
    >
      {token.type_ == "manual" ?
        value.replace(/ /g, "⎵").replace(/\\n/g, "\u000A") :
        value.replace(/\\n/g, "\u000A")}
    </span>
  );
}
