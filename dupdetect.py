#!/usr/bin/env python3
"""dupdetect-cli – find duplicate files by SHA‑256 hash.

Features:
* Recursive scan of a target directory.
* Deterministic, concise output.
* Proper error handling – never fails silently.
"""

import argparse
import hashlib
import os
import sys
from collections import defaultdict

def hash_file(path, block_size=65536):
    """Return SHA‑256 hex digest of *path*.
    Reads the file in blocks to avoid loading large files into memory.
    """
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for block in iter(lambda: f.read(block_size), b""):
                h.update(block)
    except (IOError, OSError) as e:
        print(f"Error reading '{path}': {e}", file=sys.stderr)
        return None
    return h.hexdigest()

def find_duplicates(root):
    """Walk *root* and return a dict {hash: [files...] } for hashes with >1 file."""
    hash_map = defaultdict(list)
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            full_path = os.path.join(dirpath, name)
            file_hash = hash_file(full_path)
            if file_hash is not None:
                hash_map[file_hash].append(full_path)
    # Keep only entries with actual duplicates
    return {h: paths for h, paths in hash_map.items() if len(paths) > 1}

def main():
    parser = argparse.ArgumentParser(description="Detect duplicate files by content.")
    parser.add_argument("directory", help="Path to the directory to scan")
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: '{args.directory}' is not a directory or cannot be accessed.", file=sys.stderr)
        sys.exit(2)

    dupes = find_duplicates(args.directory)

    if not dupes:
        print("No duplicates found.")
        sys.exit(0)

    for idx, (h, files) in enumerate(sorted(dupes.items()), start=1):
        # Sort file paths for deterministic output
        files_sorted = sorted(files)
        print(f"Duplicate group #{idx}: {', '.join(files_sorted)}")
    sys.exit(1)

if __name__ == "__main__":
    main()
