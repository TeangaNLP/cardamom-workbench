import { useState, useRef } from "react";
import useClickOutside from "../utils/useClickOutside";
import { CustomCascader } from "../CustomCascader";
import "./POSToken.css";

export default function POSToken({ key, defaultValue, cascaderData, updateTagState, token, tokenData }) {
    // Cascader.
    let [showCascader, setCascaderState] = useState(false);
    // Tags.
    let [tag, updateTag] = useState(defaultValue);

    // Custom hook that notifies when clicked outside this component.
    const ref = useRef();
    useClickOutside(ref, "rs", () => {
        console.log("Outside")
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
        updateTag(tag);
        console.log(tag);
        updateTagState(token.id, builtTag);
    };

    return (
        <span>
            <span
                className={`${token.type === "gap" ? "pos-gap" : "pos-token"} ${tag.length ? `highlight class${tag[0][0]}` : ""}`}
                onClick={onClick}
            >
                {tokenData.replace(/\\n/g, "\u000A")}
            </span>
            {token.type !== "gap" && showCascader ? (
                <CustomCascader
                    ref={ref}
                    data={cascaderData}
                    defaultValue={tag}
                    onUpdateTag={onUpdateTag}
                />
            ) : null}
        </span>
    );
}
