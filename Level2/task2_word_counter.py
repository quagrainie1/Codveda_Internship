"""
Codveda Internship — Level 1, Task 3
Word Counter
------------
Reads a text file and reports detailed word statistics.
"""

import os
import re
from collections import Counter


def read_file(filepath: str) -> str:
    """Read and return the full content of a text file.

    Raises:
        FileNotFoundError: If the file does not exist.
        PermissionError:   If the file cannot be read.
        UnicodeDecodeError: If the file encoding is unsupported.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: '{filepath}'")
    if not os.path.isfile(filepath):
        raise ValueError(f"'{filepath}' is not a file.")

    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def count_words(text: str) -> list[str]:
    """Split text into words (strips punctuation, lowercased)."""
    # Match sequences of word characters (letters, digits, apostrophes)
    return re.findall(r"\b[a-zA-Z']+\b", text.lower())


def count_sentences(text: str) -> int:
    """Count sentences by splitting on sentence-ending punctuation."""
    return len(re.findall(r'[.!?]+', text))


def count_paragraphs(text: str) -> int:
    """Count paragraphs (blocks separated by blank lines)."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    return len(paragraphs)


def analyse_text(text: str) -> dict:
    """Return a dictionary of text statistics."""
    words = count_words(text)
    lines = text.splitlines()
    freq = Counter(words)

    # Exclude very common stop words from "top words"
    stop_words = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to",
        "for", "of", "with", "is", "it", "this", "that", "was", "are",
        "be", "as", "by", "from", "i", "you", "he", "she", "we", "they",
    }
    meaningful = {w: c for w, c in freq.items() if w not in stop_words}

    return {
        "total_words":       len(words),
        "unique_words":      len(freq),
        "total_characters":  len(text),
        "characters_no_spaces": len(text.replace(" ", "").replace("\n", "")),
        "total_lines":       len(lines),
        "non_empty_lines":   sum(1 for l in lines if l.strip()),
        "sentences":         count_sentences(text),
        "paragraphs":        count_paragraphs(text),
        "top_10_words":      Counter(meaningful).most_common(10),
        "avg_word_length":   round(sum(len(w) for w in words) / len(words), 2) if words else 0,
    }


def display_results(filepath: str, stats: dict) -> None:
    """Pretty-print the analysis results."""
    print("\n" + "=" * 50)
    print(f"  WORD COUNT REPORT")
    print(f"  File: {os.path.basename(filepath)}")
    print("=" * 50)
    print(f"  Total words          : {stats['total_words']:,}")
    print(f"  Unique words         : {stats['unique_words']:,}")
    print(f"  Total characters     : {stats['total_characters']:,}")
    print(f"  Chars (no spaces)    : {stats['characters_no_spaces']:,}")
    print(f"  Total lines          : {stats['total_lines']:,}")
    print(f"  Non-empty lines      : {stats['non_empty_lines']:,}")
    print(f"  Sentences (approx.)  : {stats['sentences']:,}")
    print(f"  Paragraphs           : {stats['paragraphs']:,}")
    print(f"  Avg. word length     : {stats['avg_word_length']} chars")

    if stats["top_10_words"]:
        print("\n  Top 10 meaningful words:")
        for rank, (word, count) in enumerate(stats["top_10_words"], 1):
            bar = "█" * min(count, 30)
            print(f"    {rank:2}. {word:<20} {count:>4}×  {bar}")
    print("=" * 50)


def main() -> None:
    print("\n" + "=" * 50)
    print("           TEXT FILE WORD COUNTER")
    print("=" * 50)

    while True:
        filepath = input("\n  Enter the path to your text file\n  (or 'q' to quit): ").strip()

        if filepath.lower() == "q":
            print("\n  Goodbye!\n")
            break

        # Strip surrounding quotes the user may have copy-pasted
        filepath = filepath.strip("'\"")

        try:
            print(f"\n  Reading '{filepath}' …")
            content = read_file(filepath)

            if not content.strip():
                print("  ⚠  The file is empty. Nothing to count.")
                continue

            stats = analyse_text(content)
            display_results(filepath, stats)

        except FileNotFoundError as e:
            print(f"\n  ✗ {e}")
            print("  Please check the path and try again.")
        except PermissionError:
            print(f"\n  ✗ Permission denied: cannot read '{filepath}'.")
        except UnicodeDecodeError:
            print(f"\n  ✗ Could not decode '{filepath}'. Make sure it is a UTF-8 text file.")
        except Exception as e:
            print(f"\n  ✗ Unexpected error: {e}")

        again = input("\n  Analyse another file? (y/n): ").strip().lower()
        if again != "y":
            print("\n  Goodbye!\n")
            break


if __name__ == "__main__":
    main()
