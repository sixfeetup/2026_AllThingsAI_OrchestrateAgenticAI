#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "chromadb",
#   "sentence-transformers",
# ]
# ///
"""Pre-download and warm the sentence-transformers embedding model for offline use."""

import sys

from chromadb.utils.embedding_functions import DefaultEmbeddingFunction


def main():
    ef = DefaultEmbeddingFunction()
    ef(["warmup test"])
    print("  Model cache warmed")


if __name__ == "__main__":
    main()
