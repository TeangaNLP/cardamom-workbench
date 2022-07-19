import React, { useState } from "react";
import { MultiCascader } from "rsuite";
import "rsuite/dist/rsuite.min.css";
import "./CustomCascader.css";

const CustomCascader = React.forwardRef((props, ref) => {

    // Since onCheck does not return an array of items to build tags,
    // we will keep track of the tag items ourselves.
    let [tagItems, updateTagItems] = useState([]);
    let labelValue = null;
    let item = null;

    let buildTag = (items) => {

        // Check if the current tag can have multiple features.
        let multiFeatures = items[0]["parent"];

        // If the tag can have multiple features,
        // then tag structure:
        // tokenTag: {
        //     tag: tagName,
        //     features: [
        //         {
        //             feature: featureName,
        //             value: value
        //         },
        //         {
        //             feature: featureName,
        //             value: value
        //         },
        //     ]
        // }
        // else:
        // tokenTag: {
        //     tag: tagName,
        //     features: []
        // }

        let tokenTag = {};

        if (!multiFeatures) {
            let item = items[0];
            tokenTag = {
                tag: item["label"],
                features: [],
            }
        } else {
            console.log(items);
            let tagName = items[0]["parent"]["parent"]["label"];
            let features = [];
            for (let i = 0; i < items.length; i++) {
                let item = items[i];
                let featureObj = {
                    feature: item["parent"]["label"],
                    value: item["label"]
                }
                features.push(featureObj);
            }
            tokenTag = {
                tag: tagName,
                features: features,
            }
        }

        return tokenTag;
    };

    let onCheck = (value, item, checked) => {
        // If something is checked, then run validation, else return.
        if (!checked) {
            return;
        }
        // Value is going to be previously selected values.
        // So if a new value has been checked, it would be the last value entered.

        let newVal = value[value.length - 1];
        let newValSplit = newVal.split("-");
        let tags = [];
        let tempTagItems = [];

        // For all previous values, check if new value has an effect.
        for (let i = 0; i < value.length - 1; i++) {
            let reference = value[i].split("-");
            let tag = value[i];

            // If the new value is a completely different tag, then overwrite.
            if (newValSplit[0] !== reference[0]) {
                tags = [];
                break;
            }
            // If new value is a different value of a previously seen feature,
            // then overwrite the previously seen feature.
            if (newValSplit[1] === reference[1] && newValSplit[2] !== reference[2]) {
                continue;
            }
            tags.push(tag);
            tempTagItems.push(tagItems[i]);
        }
        tags.push(newVal);
        tempTagItems.push(item);
        updateTagItems(tempTagItems);

        let builtTag = buildTag(tempTagItems);
        props.onUpdateTag(tags, builtTag);
    };

    // Create uncheckable items in Cascader based on levels.
    let createUncheckable = (levels) => {
        let uncheckables = [];
        for (let l of levels) {
            uncheckables.push(String(l[0]));
            for (let sl = 1; sl <= l[1]; sl++) {
                let s = l[0] + "-" + sl;
                uncheckables.push(s);
            }
        }
        return uncheckables;
    };

    return (
        <div ref={ref} className="cascader">
            <MultiCascader
                data={props.data}
                onCheck={onCheck}
                defaultValue={props.defaultValue}
                renderValue={(value, selectedItems) =>
                    selectedItems.map((item) => item.label).join(" , ")
                }
                uncheckableItemValues={createUncheckable([[2, 7]])}
            />
        </div>
    );
});

export default CustomCascader;
