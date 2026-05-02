"""
Codveda Internship — Level 3, Task 2
File Encryption / Decryption
------------------------------
Supports TWO encryption modes:

  1. Caesar Cipher  — classic shift cipher (letters only, key = shift amount)
  2. Fernet (AES)   — modern symmetric encryption via the `cryptography` library

Usage (interactive):
    python task2_encryption.py

Usage (CLI flags):
    python task2_encryption.py --mode fernet --action encrypt --input plain.txt --output enc.bin
    python task2_encryption.py --mode fernet --action decrypt --input enc.bin  --output plain.txt --key <base64key>

Dependencies for Fernet:
    pip install cryptography
"""

import os
import sys
import argparse
import string
from pathlib import Path


# ─────────────────────────────────────────
#  Caesar Cipher
# ─────────────────────────────────────────

PRINTABLE_NO_NEWLINE = [c for c in string.printable if c not in ('\n', '\r')]
PRINTABLE_SIZE = len(PRINTABLE_NO_NEWLINE)
CHAR_INDEX = {c: i for i, c in enumerate(PRINTABLE_NO_NEWLINE)}


def caesar_encrypt(text: str, shift: int) -> str:
    """Encrypt text with a Caesar-style shift over all printable ASCII chars."""
    shift = shift % PRINTABLE_SIZE
    result = []
    for ch in text:
        if ch in CHAR_INDEX:
            result.append(PRINTABLE_NO_NEWLINE[(CHAR_INDEX[ch] + shift) % PRINTABLE_SIZE])
        else:
            result.append(ch)     # preserve newlines etc.
    return "".join(result)


def caesar_decrypt(text: str, shift: int) -> str:
    """Reverse a Caesar encryption."""
    return caesar_encrypt(text, -shift)


# ─────────────────────────────────────────
#  Fernet (AES-128-CBC) Encryption
# ─────────────────────────────────────────

def _import_fernet():
    try:
        from cryptography.fernet import Fernet, InvalidToken
        return Fernet, InvalidToken
    except ImportError:
        sys.exit(
            "\n  ✗ The 'cryptography' package is required for Fernet mode.\n"
            "  Run:  pip install cryptography\n"
        )


def fernet_generate_key() -> bytes:
    Fernet, _ = _import_fernet()
    return Fernet.generate_key()


def fernet_encrypt(data: bytes, key: bytes) -> bytes:
    Fernet, _ = _import_fernet()
    return Fernet(key).encrypt(data)


def fernet_decrypt(token: bytes, key: bytes) -> bytes:
    Fernet, InvalidToken = _import_fernet()
    try:
        return Fernet(key).decrypt(token)
    except InvalidToken:
        raise ValueError(
            "Decryption failed. The key is incorrect or the file is corrupted."
        )


# ─────────────────────────────────────────
#  File helpers
# ─────────────────────────────────────────

def read_text(path: str) -> str:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: '{path}'")
    with open(p, "r", encoding="utf-8") as f:
        return f.read()


def read_bytes(path: str) -> bytes:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: '{path}'")
    with open(p, "rb") as f:
        return f.read()


def write_text(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def write_bytes(path: str, data: bytes) -> None:
    with open(path, "wb") as f:
        f.write(data)


def default_output_path(input_path: str, action: str, mode: str) -> str:
    """Generate a sensible output filename."""
    p    = Path(input_path)
    stem = p.stem
    ext  = p.suffix
    if action == "encrypt":
        suffix = ".enc.txt" if mode == "caesar" else ".enc.bin"
    else:
        suffix = "_decrypted" + (ext or ".txt")
    return str(p.parent / (stem + suffix))


# ─────────────────────────────────────────
#  High-level operations
# ─────────────────────────────────────────

def run_caesar_encrypt(input_path: str, output_path: str, shift: int) -> None:
    content = read_text(input_path)
    encrypted = caesar_encrypt(content, shift)
    # Prepend a header with the shift so decryption can detect it
    header = f"[CAESAR|SHIFT={shift}]\n"
    write_text(output_path, header + encrypted)
    print(f"\n  ✔ Caesar-encrypted → '{output_path}'")
    print(f"     Key (shift): {shift}  — remember this to decrypt!")


def run_caesar_decrypt(input_path: str, output_path: str, shift: int | None) -> None:
    content = read_text(input_path)
    lines = content.split("\n", 1)

    # Try to auto-read shift from header
    if lines[0].startswith("[CAESAR|SHIFT="):
        auto_shift = int(lines[0].split("=")[1].rstrip("]"))
        body = lines[1] if len(lines) > 1 else ""
        if shift is None:
            shift = auto_shift
            print(f"  ℹ  Auto-detected shift = {shift} from file header.")
    else:
        body = content
        if shift is None:
            raise ValueError("No shift value found in file header. Please supply the key (shift).")

    decrypted = caesar_decrypt(body, shift)
    write_text(output_path, decrypted)
    print(f"\n  ✔ Caesar-decrypted → '{output_path}'")


def run_fernet_encrypt(input_path: str, output_path: str, key: bytes | None) -> bytes:
    if key is None:
        key = fernet_generate_key()
        print(f"\n  ✔ New Fernet key generated.")
    data      = read_bytes(input_path)
    encrypted = fernet_encrypt(data, key)
    write_bytes(output_path, encrypted)
    print(f"  ✔ Fernet-encrypted → '{output_path}'")
    print(f"\n  ⚠  SAVE THIS KEY — you need it to decrypt:\n")
    print(f"     {key.decode()}\n")
    return key


def run_fernet_decrypt(input_path: str, output_path: str, key: bytes) -> None:
    token     = read_bytes(input_path)
    decrypted = fernet_decrypt(token, key)
    write_bytes(output_path, decrypted)
    print(f"\n  ✔ Fernet-decrypted → '{output_path}'")


# ─────────────────────────────────────────
#  Interactive UI
# ─────────────────────────────────────────

def choose(prompt: str, options: list[str]) -> str:
    while True:
        val = input(prompt).strip().lower()
        if val in options:
            return val
        print(f"  ✗ Choose from: {', '.join(options)}")


def get_int(prompt: str, lo: int, hi: int) -> int:
    while True:
        try:
            v = int(input(prompt).strip())
            if lo <= v <= hi:
                return v
            print(f"  ✗ Enter a number between {lo} and {hi}.")
        except ValueError:
            print("  ✗ Not a valid integer.")


def get_path(prompt: str, must_exist: bool = True) -> str:
    while True:
        p = input(prompt).strip().strip("'\"")
        if must_exist and not Path(p).exists():
            print(f"  ✗ File not found: '{p}'")
        else:
            return p


def interactive_mode() -> None:
    print("\n" + "=" * 52)
    print("     FILE ENCRYPTION / DECRYPTION TOOL")
    print("=" * 52)

    while True:
        print("\n  ─── Cipher Mode ───")
        print("  [1]  Caesar Cipher  (text files, simple key)")
        print("  [2]  Fernet / AES   (any file, strong encryption)")
        print("  [0]  Exit")

        cipher = input("\n  Choose mode: ").strip()
        if cipher == "0":
            print("\n  Goodbye!\n")
            break
        if cipher not in ("1", "2"):
            print("  ✗ Invalid choice.")
            continue

        action = choose("\n  [e]ncrypt or [d]ecrypt? ", ["e", "d", "encrypt", "decrypt"])
        action = "encrypt" if action.startswith("e") else "decrypt"
        mode   = "caesar" if cipher == "1" else "fernet"

        input_path = get_path(f"\n  Input file path: ", must_exist=True)
        default_out = default_output_path(input_path, action, mode)
        out_prompt  = f"  Output file path [default: {default_out}]: "
        output_path = input(out_prompt).strip().strip("'\"") or default_out

        try:
            if mode == "caesar":
                shift = get_int("  Shift key (1-94): ", 1, 94)
                if action == "encrypt":
                    run_caesar_encrypt(input_path, output_path, shift)
                else:
                    run_caesar_decrypt(input_path, output_path, shift)

            else:  # fernet
                if action == "encrypt":
                    key_input = input("  Paste existing key (or press Enter to generate new): ").strip()
                    key = key_input.encode() if key_input else None
                    run_fernet_encrypt(input_path, output_path, key)
                else:
                    key_input = input("  Paste your Fernet key: ").strip()
                    if not key_input:
                        print("  ✗ A key is required for decryption.")
                        continue
                    run_fernet_decrypt(input_path, output_path, key_input.encode())

        except FileNotFoundError as e:
            print(f"\n  ✗ {e}")
        except ValueError as e:
            print(f"\n  ✗ {e}")
        except Exception as e:
            print(f"\n  ✗ Unexpected error: {e}")

        again = input("\n  Another operation? (y/n): ").strip().lower()
        if again != "y":
            print("\n  Goodbye!\n")
            break


# ─────────────────────────────────────────
#  CLI entry point
# ─────────────────────────────────────────

def cli_mode() -> None:
    parser = argparse.ArgumentParser(description="File Encryption / Decryption Tool")
    parser.add_argument("--mode",   choices=["caesar", "fernet"], required=True)
    parser.add_argument("--action", choices=["encrypt", "decrypt"], required=True)
    parser.add_argument("--input",  required=True, help="Input file path")
    parser.add_argument("--output", help="Output file path (auto-generated if omitted)")
    parser.add_argument("--key",    help="Shift (Caesar) or base64 key (Fernet)")
    args = parser.parse_args()

    output = args.output or default_output_path(args.input, args.action, args.mode)

    if args.mode == "caesar":
        if args.key is None:
            parser.error("--key (shift value) is required for Caesar cipher.")
        shift = int(args.key)
        if args.action == "encrypt":
            run_caesar_encrypt(args.input, output, shift)
        else:
            run_caesar_decrypt(args.input, output, shift)
    else:
        if args.action == "encrypt":
            key = args.key.encode() if args.key else None
            run_fernet_encrypt(args.input, output, key)
        else:
            if not args.key:
                parser.error("--key is required for Fernet decryption.")
            run_fernet_decrypt(args.input, output, args.key.encode())


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cli_mode()
    else:
        interactive_mode()
