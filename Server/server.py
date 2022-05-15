import game, tools, users

g = game.Game()

def display_stats():
    if g.dead == True:
        print
        print(f"\nThe game has ended\nYour final Score is {g.score}")
        print(f"Word was {g.random_word}")
        print(f"\nProgress = {g.progress}")
    else:
        print(f"\nProgress = {g.progress}")
        print(f"Letters used = {g.used_letters}")
        print(f"Tries used: {g.count}/7")
        print(f"Score = {g.score}")

def input_strings(args):
    string = args[0]
    return g.event(string)

def change_level(args):
    level = args[0]
    return g.update_level(level)


def levelled(args):
    level = args[1]
    print("Your level will change to " + level + " after this word!")

def next_word(args):
    word = args[1]
    score = args[2]

    print(f"Word '{word}'' COMPLETE! Score: {score}")

display_stats()

def input_stream():
    functions = {
        "submit": input_strings,
        "level": change_level
    }

    output_functions = {
        "levelled": levelled,
        "nextword": next_word
    }

    while True:
        inp = input("Enter inputs: ")
        separated = tools.separator(inp)
        
        try:
            func = separated[0]
            args = separated[1:]
        except IndexError:
            print("IndexError: isufficent number of args")
            print("Inputs not entered")
            continue

        try:
            function = functions[func]
        except KeyError:
            print("Key not in dict")
            print("Inputs not entered")
            continue

        out = function(args)

        try:
            out = tools.separator(out)
        except TypeError:
            pass
        else:
            output_function_string = out[0]
            output_function = output_functions[output_function_string]
            output_function(out)

        display_stats()

        if g.dead == True:
            break
        print(g.random_word)

input_stream()