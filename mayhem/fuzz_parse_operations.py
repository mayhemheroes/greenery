#! /usr/bin/env python3
import atheris
import sys
import fuzz_helpers

with atheris.instrument_imports(include=["greenery"]):
    import greenery

def TestOneInput(data):
    fdp = fuzz_helpers.EnhancedFuzzedDataProvider(data)
    try:
        regex_combination = (greenery.parse(fdp.ConsumeRandomString()) for _ in range(fdp.ConsumeIntInRange(0, 10)))
        regex_combo = greenery.parse(fdp.ConsumeRandomString())
        regex_combo.reduce()

        for regex in regex_combination:
            binary_op = fdp.ConsumeIntInRange(0, 6)
            if binary_op == 0:
                regex_combo &= regex
            elif binary_op == 1:
                regex_combo |= regex
            elif binary_op == 2:
                regex_combo -= regex
            elif binary_op == 3:
                regex_combo ^= regex
            elif binary_op == 4:
                regex_combo *= regex
            elif binary_op == 5:
                regex_combo * greenery.Multiplier(greenery.Bound(fdp.ConsumeInt(1)), greenery.INF)
            else:
                regex_combo -= regex
    except IndexError as e:
        return -1
    except Exception as e:
        if 'Could not parse' in str(e):
            return -1
        raise


def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
