import { useEffect } from "react";

// Function to detect whether the user clicked outside the dropbox
// in order to save the tags.

export default function useClickOutside(ref, keyword, callback) {
    const onClickOutside = (event) => {
        // To check if the SVG clicked belongs to the Cascader.
        let element = event.target;
        let className = "";
        // If the element does not have a class name but has children
        // check if the children is part of the Cascader.
        if (event.target.className === "" && event.target.children.length > 0) {
            let child = event.target.children[0];
            // Check if the child is an SVG or a normal element.
            if (typeof child.className !== "string") {
                className = child.className.baseVal;
            } else {
                className = child.className;
            }
        } else if (typeof element.className !== "string") {
            // Check if the element is an SVG or a normal element.
            className = element.className.baseVal;
        } else {
            className = element.className;
        }

        if (
            ref.current &&
            !ref.current.contains(event.target) &&
            !keyword &&
            !className.includes(keyword)
        ) {
            callback();
        }
    };

    useEffect(() => {
        document.addEventListener("mousedown", onClickOutside);

        return () => document.removeEventListener("mousedown", onClickOutside);
    });
}
