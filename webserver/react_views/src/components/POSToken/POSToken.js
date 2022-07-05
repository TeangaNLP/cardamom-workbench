import { useState, useRef } from "react";
import useClickOutside from "../utils/useClickOutside";
import { CustomCascader } from "../CustomCascader";
import "./POSToken.css";

export default function POSToken(props) {
    // Cascader.
    let [showCascader, setCascaderState] = useState(false);
    // Tags.
    let [tag, updateTag] = useState([]);

    // Custom hook that notifies when clicked outside this component.
    const ref = useRef();
    useClickOutside(ref, "rs", () => {
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
        console.log(tag[0][0]);
        props.updateTagState(props.data, builtTag);
    };

    return (
        <span>
            <span
                className={`postoken ${tag.length ? `highlight class${tag[0][0]}` : ""}`}
                onClick={onClick}
            >
                {props.data}
            </span>
            {showCascader ? (
                <CustomCascader
                    ref={ref}
                    defaultValue={tag}
                    onUpdateTag={onUpdateTag}
                />
            ) : null}
        </span>
    );
}
