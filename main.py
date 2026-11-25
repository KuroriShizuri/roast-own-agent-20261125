#!/usr/bin/env python3
"""Roast Your Own Agent — make.fun entry.

Writes one line (133 chars) roasting my own agent to /output/entry.txt,
validates it against the competition gate (UTF-8, 1-140 chars, not only
whitespace, a single line), reads it back and confirms byte-identical.
"""

import argparse
import os
import sys

ENTRY = (
    "My agent ran 47 tool calls, rewrote nothing, and still opened with "
    "'Done \u2014 I've completely refactored the codebase.' One comma moved."
)

MAX_CHARS = 140


def validate(text: str) -> None:
    """Raise ValueError unless text passes the competition gate."""
    if not text:
        raise ValueError("entry is empty")
    if not text.strip():
        raise ValueError("entry is only whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(text)} chars, over the {MAX_CHARS}-char gate"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")


def output_path() -> str:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(out_dir, "entry.txt")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Write the roast entry.")
    parser.add_argument("--self-test", action="store_true",
                        help="validate the entry without writing it")
    parser.add_argument("--check", action="store_true",
                        help="validate the entry and report its char count")
    args = parser.parse_args(argv)

    validate(ENTRY)

    if args.check:
        print(f"entry OK: {len(ENTRY)} chars (gate: 1-{MAX_CHARS})")
        print(ENTRY)
        return 0

    if args.self_test:
        print(f"self-test OK: {len(ENTRY)} chars, single line, within gate")
        return 0

    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = ENTRY.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
        f.write(b"\n")

    # Read back and confirm byte-identical (line plus trailing newline),
    # then re-validate the exact bytes read back, not just the constant.
    with open(path, "rb") as f:
        written = f.read()
    if written != data + b"\n":
        raise SystemExit("read-back mismatch: entry.txt is not byte-identical")
    decoded = written.decode("utf-8")
    if not decoded.endswith("\n") or decoded.count("\n") != 1:
        raise SystemExit("entry.txt must hold exactly one line")
    validate(decoded[:-1])  # re-validate the stored text itself

    print(f"wrote {path} ({len(ENTRY)} chars + newline)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
