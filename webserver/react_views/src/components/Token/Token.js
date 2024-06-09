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
  const [isActive, setIsActive] = useState(false);
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

  const handleSpanClick = () => {
    // Clear cursor position when clicking outside a word
    setCursorPosition(null);
  };

  const handleSingleOnClick = (e, wordIndex) => {
    setIsActive(true);
    const rect = e.target.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const characterWidth = rect.width / e.target.textContent.length;
    const offset = Math.round(x / characterWidth);

    setCursorPosition({ index: wordIndex, offset });
  };

  const handleWordClick = (e, wordIndex) => {
    const rect = e.target.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const characterWidth = rect.width / e.target.textContent.length;
    const offset = Math.round(x / characterWidth);

    setCursorPosition({ index: wordIndex, offset });
  };

  const handleCrossClick = () => {
    setCursorPosition(null);
    setIsActive(false);
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
        <>
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
          {isActive && (
            <button
              className="cross-button"
              style={{
                position: "absolute",
                right: "-8px",
                top: "-4px",
                backgroundColor: "red",
                color: "white",
                border: "none",
                borderRadius: "50%",
                width: "12px",
                height: "12px",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                cursor: "pointer",
              }}
              onClick={handleCrossClick}
            >
              &times;
            </button>
          )}
        </>
      )}
    </span>
  );
}
