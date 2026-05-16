# dupdetect-cli

A tiny Python command‑line tool that finds duplicate files in a given directory (recursively) by comparing SHA‑256 hashes.

- **Idempotent** – running multiple times yields the same output.
- **Clear naming** – duplicate groups are numbered and listed.
- **No silent failures** – all errors are reported.

## Usage
```sh
python dupdetect.py /path/to/dir
```
The script prints one line per duplicate group, e.g.:
```
Duplicate group #1: /path/to/fileA.txt, /path/to/other/fileB.txt
```
If no duplicates are found it prints `No duplicates found.` and exits with code 0; otherwise it exits with code 1.

## Requirements
- Python 3.8+

## License
MIT
