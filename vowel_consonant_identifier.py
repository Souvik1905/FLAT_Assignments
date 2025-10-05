import pywrapfst as fst

def build_vowel_consonant_fst():
    f = fst.Fst()

    start = f.add_state()
    f.set_start(start)

    accept = f.add_state()
    f.set_final(accept)

    vowels = set("AEIOUaeiou")

    # Vowels → 'V', Consonants → 'C'
    for c in range(ord('A'), ord('Z') + 1):
        if chr(c) in vowels:
            f.add_arc(start, fst.Arc(c, ord('V'), fst.Weight.One(f.weight_type()), accept))
        else:
            f.add_arc(start, fst.Arc(c, ord('C'), fst.Weight.One(f.weight_type()), accept))

    for c in range(ord('a'), ord('z') + 1):
        if chr(c) in vowels:
            f.add_arc(start, fst.Arc(c, ord('V'), fst.Weight.One(f.weight_type()), accept))
        else:
            f.add_arc(start, fst.Arc(c, ord('C'), fst.Weight.One(f.weight_type()), accept))

    # Identity for non-alphabet (digits and space)
    for c in range(ord('0'), ord('9') + 1):
        f.add_arc(start, fst.Arc(c, c, fst.Weight.One(f.weight_type()), accept))
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
            output += c
    return output


if __name__ == "__main__":
    f = build_vowel_consonant_fst()

    inp = input("Enter a string: ")
    out = apply_fst(f, inp)

    print("Vowel/Consonant string:", out)
