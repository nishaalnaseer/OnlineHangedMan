def separator(text):
    out = []
    text += " "  # to indicate end of text else the last word will not apend
    word = ""
    for letter in text:
        if letter != " ":
            # if letter is not a space add it to the word
            word += letter
        else:
            # if letter is a space add it to th args list
            if word != "":
                # if not the args list will have empty strings in list
                out.append(word)
                word = ""

    return out