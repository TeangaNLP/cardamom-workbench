from model import SpaceModel


def cardamom_space(string, provenance=None, uploaded_file_id=None):
    """Finds indeces of space and newline characters in a string of text
       Specifies whether it is a space or newline at each index"""

    # Create a list of all space and newline characters used in the string
    space_chars = "".join(string.split())
    space_chars = sorted(list(set(space_chars)))
    space_chars = [i for i in sorted(list(set(string))) if i not in space_chars]

    # Create a list of space-index tuples and newline indices
    space_list = [space for space in enumerate(string) if space[1] in space_chars]

    # Generate a space-model for each space instance in the space-list, adding each model to an output list.
    indexed_spaces = list()
    for space in space_list:
        space_model = SpaceModel(space_index=space[0], space_type=space[1], uploaded_file_id=uploaded_file_id)
        indexed_spaces.append(space_model)

    return indexed_spaces


# if __name__ == "__main__":
#
#     test_en = "This is some test text. It's short. It doesn't say very much. But, it is useful for the sake of " \
#               "testing!\nI hope it works because I don't want it to be a time-waste. Críoch."
#
#     print(cardamom_space(test_en))
