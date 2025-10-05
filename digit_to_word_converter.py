import pywrapfst as fst

def build_digit_to_word_fst():
    f = fst.Fst()

    start = f.add_state()
    f.set_start(start)

    accept = f.add_state()
    f.set_final(accept)

    # Digit → Word map
    digit_words = {
        '0': "ZERO", '1': "ONE", '2': "TWO", '3': "THREE", '4': "FOUR",
        '5': "FIVE", '6': "SIX", '7': "SEVEN", '8': "EIGHT", '9': "NINE"
    }

    # Arcs: digit → first letter of word
    for d, word in digit_words.items():
        f.add_arc(start, fst.Arc(ord(d), ord(word[0]), fst.Weight.One(f.weight_type()), accept))

    # Identity arcs for non-digits
    for c in range(ord('A'), ord('Z') + 1):
        f.add_arc(start, fst.Arc(c, c, fst.Weight.One(f.weight_type()), accept))
    for c in range(ord('a'), ord('z') + 1):
        f.add_arc(start, fst.Arc(c, c, fst.Weight.One(f.weight_type()), accept))
    f.add_arc(start, fst.Arc(ord(' '), ord(' '), fst.Weight.One(f.weight_type()), accept))

    return f, digit_words


def apply_fst(f, digit_words, input_str):
    output = ""

    start = f.start()
    for c in input_str:
        matched = False
        for arc in f.arcs(start):
            if arc.ilabel == ord(c):
                if c in digit_words:
                    output += digit_words[c]   # expand full word
                else:
                    output += chr(arc.olabel) # normal identity mapping
                matched = True
                break
        if not matched:
            # No arc found → keep char unchanged
            output += c
    return output


if __name__ == "__main__":
    f, digit_words = build_digit_to_word_fst()

    inp = input("Enter a string with digits: ")
    out = apply_fst(f, digit_words, inp)

    print("Converted string:", out)
