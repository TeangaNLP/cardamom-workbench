import { useState, useRef, useEffect } from "react";
import useClickOutside from "../utils/useClickOutside";
import { CustomCascader } from "../CustomCascader";
import "./POSToken.css";


/*
function POSTokenDefault(token, tokenData,
                         tag, defaultValue,
                         onClick, showCascader,
                         ref, onUpdateTag,
                         cascaderData
){
  return (
    <span
            className={`${token.type_ === "gap" ? "pos-gap" : "pos-token"} ${tag
              ? `class${tag[0][0]}`
              : defaultValue.length === 0
                ? ""
                : `class${defaultValue[0]}`
              }`}
            onClick={onClick}
          >
            {tokenData}
          {token.type_ !== "gap" && showCascader ? (
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

          <POSTokenDefault
                         token={token}
                         tokenData={tokenData}
                         tag={tag}
                         defaultValue={defaultValue}
                         onClick={onClick} 
                         showCascader={showCascader}
                         cascaderData={cascaderData}
                         ref={ref} 
                         onUpdateTag={onUpdateTag}
 
            />
*/

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

  console.log(tag);
  if(!tokenData.includes("\n")){
  return (
    <span>
          <span
                  className={`${token.type_ === "gap" ? "pos-gap" : "pos-token"} 
                    ${
                      token.type_ !== "gap" && token.pos_tags.length != 0
                    ? token.pos_tags[token.pos_tags.length - 1].tag.toLowerCase()
                    : ""
                    }
                    `}
                  onClick={onClick}
                >
                  {tokenData}
          </span>
          {token.type_ !== "gap" && showCascader ? (
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
else {
  if(tokenData.includes("\n\n")){
    return <><br/><br/></>
  }
  else{
    return <><br/></>
  }
}

}
