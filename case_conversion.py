import pywrapfst as fst

def build_lower_to_upper_fst():
    f = fst.Fst()

    start = f.add_state()
    f.set_start(start)

    accept = f.add_state()
    f.set_final(accept)

    # Lowercase -> Uppercase
    for c in range(ord('a'), ord('z') + 1):
        upper = c - ord('a') + ord('A')
        f.add_arc(start, fst.Arc(c, upper, fst.Weight.One(f.weight_type()), accept))

    # Identity arcs for uppercase
    for c in range(ord('A'), ord('Z') + 1):
        f.add_arc(start, fst.Arc(c, c, fst.Weight.One(f.weight_type()), accept))

    # Identity arcs for digits
    for c in range(ord('0'), ord('9') + 1):
        f.add_arc(start, fst.Arc(c, c, fst.Weight.One(f.weight_type()), accept))

    # Space
    f.add_arc(start, fst.Arc(ord(' '), ord(' '), fst.Weight.One(f.weight_type()), accept))

    return f


def apply_fst(f, input_str):
    output = ""

    start = f.start()
    for c in input_str:
        matched = False
        for arc in f.arcs(start):
            if arc.ilabel == ord(c):
                output += chr(arc.olabel)
                matched = True
                break
        if not matched:
            # Keep unchanged if no arc matches
            output += c
    return output


if __name__ == "__main__":
    f = build_lower_to_upper_fst()

    inp = input("Enter a string: ")
    out = apply_fst(f, inp)

    print("Converted string:", out)
