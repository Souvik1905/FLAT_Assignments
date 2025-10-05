import pywrapfst as fst

# Function to build FST for binary complement
def build_binary_complement_fst():
    f = fst.Fst()

    start = f.add_state()
    f.set_start(start)

    accept = f.add_state()
    f.set_final(accept)

    # Complement rules: 0 -> 1, 1 -> 0
    f.add_arc(start, fst.Arc(ord('0'), ord('1'), fst.Weight.One(f.weight_type()), accept))
    f.add_arc(start, fst.Arc(ord('1'), ord('0'), fst.Weight.One(f.weight_type()), accept))

    # Identity arcs for other characters
    for c in range(ord('a'), ord('z') + 1):
        f.add_arc(start, fst.Arc(c, c, fst.Weight.One(f.weight_type()), accept))
    for c in range(ord('A'), ord('Z') + 1):
        f.add_arc(start, fst.Arc(c, c, fst.Weight.One(f.weight_type()), accept))

    f.add_arc(start, fst.Arc(ord(' '), ord(' '), fst.Weight.One(f.weight_type()), accept))

    return f


# Apply FST to a string
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
            # If no rule found, keep as-is
            output += c
    return output


if __name__ == "__main__":
    f = build_binary_complement_fst()

    inp = input("Enter a binary string: ")
    out = apply_fst(f, inp)

    print("Binary complement:", out)
