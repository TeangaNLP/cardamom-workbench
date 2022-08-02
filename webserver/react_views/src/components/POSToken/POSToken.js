import { useState, useRef, useEffect } from "react";
import useClickOutside from "../utils/useClickOutside";
import { CustomCascader } from "../CustomCascader";
import "./POSToken.css";

export default function POSToken({
  key,
  defaultValue,
  cascaderData,
  updateTagState,
  token,
  tokenData,
}) {
  // Cascader.
  let [showCascader, setCascaderState] = useState(false);
  // Tags.
  let [tag, setTag] = useState();

  // Custom hook that notifies when clicked outside this component.
  const ref = useRef();
  useClickOutside(ref, "rs", () => {
    console.log("Outside");
    setCascaderState(false);
  });

  // Whether token has been clicked.
  let onClick = () => {
    if (showCascader) {
      setCascaderState(false);
    } else {
      setCascaderState(true);
    }
  };

  // Update the tag of the selected token.
  let onUpdateTag = (tag, builtTag) => {
    setTag(tag);
    updateTagState(token.id, builtTag);
  };

  console.log(tag, defaultValue, token);
  return (
    <span>
      <span
        className={`${token.type === "gap" ? "pos-gap" : "pos-token"} ${
          tag
            ? `class${tag[0][0]}`
            : defaultValue.length > 0
            ? `class${defaultValue[0][0]}`
            : ""
        }`}
        onClick={onClick}
      >
        {tokenData.replace(/\\n/g, "\u000A")}
      </span>
      {token.type !== "gap" && showCascader ? (
        <CustomCascader
          ref={ref}
          data={cascaderData}
          defaultValue={tag ? tag : defaultValue}
          onUpdateTag={onUpdateTag}
        />
      ) : null}
    </span>
  );
}
