"""
Test file cleanup utility for removing generated test files.
"""

from pathlib import Path


def cleanup_test_files(extensions: list[str] | None = None, preserve_set: set[str] | None = None) -> int:
    """
    Clean up test files with specified extensions from the current directory.

    Args:
        extensions: List of file extensions to delete (default: ['.k', '.dat']).
        preserve_set: Set of filenames to preserve even if they match extensions (default: []).

    Returns:
        Number of files deleted.
    """
    if extensions is None:
        extensions = ['.k', '.dat']

    if preserve_set is None:
        preserve_set = set()

    # Get the current directory
    current_path = Path(".")

    deleted_count = 0

    # Find and delete files with matching extensions
    for ext in extensions:
        # Use glob to find files with the current extension (no recursion)
        pattern = f"*{ext}"
        matching_files = current_path.glob(pattern)

        for file_path in matching_files:
            # Skip if file is in preserve list
            if file_path.name in preserve_set:
                print(f"Preserving: {file_path}")
                continue

            try:
                file_path.unlink()
                print(f"Deleted: {file_path}")
                deleted_count += 1
            except OSError as e:
                print(f"Error deleting {file_path}: {e}")

    return deleted_count


def main():
    """Main function for command-line usage."""
    import argparse

    parser = argparse.ArgumentParser(description="Clean up test files")
    parser.add_argument(
        "--extensions",
        nargs="+",
        default=['.k', '.dat'],
        help="File extensions to delete (default: .k .dat)"
    )
    parser.add_argument(
        "--preserve",
        nargs="*",
        default=[],
        help="Filenames to preserve"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be deleted without actually deleting"
    )

    args = parser.parse_args()

    deleted = cleanup_test_files(
        extensions=args.extensions,
        preserve_set=args.preserve
    )

    print(f"\nCleanup complete. {deleted} files deleted.")


if __name__ == "__main__":
    main()
