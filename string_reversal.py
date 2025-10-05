import sys
import pywrapfst as fst

def build_fst_from_string(input_str):
    f = fst.Fst()

    start = f.add_state()
    f.set_start(start)

    current = start
    for c in input_str:
        next_state = f.add_state()
        f.add_arc(current, fst.Arc(ord(c), ord(c), fst.Weight.One(f.weight_type()), next_state))
        current = next_state

    f.set_final(current, fst.Weight.One(f.weight_type()))
    return f

def traverse_fst(f):
    """Traverse deterministically along first arc path and collect labels"""
    output = []
    state = f.start()

    # While not in a final state, follow the first arc
    while f.final(state) == fst.Weight.Zero(f.weight_type()) and f.num_arcs(state) > 0:
        arcs = list(f.arcs(state))
        if not arcs:
            break
        arc = arcs[0]  # follow the first arc
        output.append(chr(arc.ilabel))
        state = arc.nextstate

    return "".join(output)

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <string>")
        sys.exit(1)

    input_str = sys.argv[1]

    # Build FST
    f = build_fst_from_string(input_str)

    # Reverse FST
    reversed_fst = fst.Fst()
    fst.reverse(f, reversed_fst)

    # Collect reversed string
    output_str = traverse_fst(reversed_fst)

    print("Input:", input_str)
    print("Reversed:", output_str)

if __name__ == "__main__":
    main()
