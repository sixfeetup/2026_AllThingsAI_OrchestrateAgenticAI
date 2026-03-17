#!/usr/bin/env python3
"""
Rename all "contract" references to "document" across the demo project.

Phase 1: File/directory renames (git mv where possible)
Phase 2: Content replacements (sed-style)
Phase 3: Summary and residual scan
"""

import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# --- helpers ---

def run(cmd, **kw):
    """Run a shell command from repo root, return (returncode, stdout)."""
    r = subprocess.run(cmd, shell=True, cwd=REPO, capture_output=True, text=True, **kw)
    return r.returncode, r.stdout.strip()

def is_git_tracked(path):
    """Check whether a path is tracked by git."""
    rc, _ = run(f"git ls-files --error-unmatch {shquote(path)}")
    return rc == 0

def shquote(s):
    import shlex
    return shlex.quote(s)

def git_mv(src, dst):
    """git mv, creating parent dirs as needed."""
    dst_parent = os.path.dirname(os.path.join(REPO, dst))
    os.makedirs(dst_parent, exist_ok=True)
    rc, out = run(f"git mv {shquote(src)} {shquote(dst)}")
    if rc != 0:
        # Fallback: plain rename
        os.makedirs(dst_parent, exist_ok=True)
        os.rename(os.path.join(REPO, src), os.path.join(REPO, dst))
        print(f"  os.rename {src} -> {dst}")
    else:
        print(f"  git mv {src} -> {dst}")

def plain_rename(src, dst):
    """os.rename with parent dir creation."""
    dst_abs = os.path.join(REPO, dst)
    os.makedirs(os.path.dirname(dst_abs), exist_ok=True)
    os.rename(os.path.join(REPO, src), dst_abs)
    print(f"  os.rename {src} -> {dst}")

# --- Phase 1: file/directory renames ---

BINARY_EXTS = {'.pdf', '.zip', '.png', '.jpg', '.jpeg', '.gif', '.db', '.bin',
               '.sqlite3', '.whl', '.pyc', '.pyo', '.so', '.dylib', '.tag'}
SKIP_DIRS = {'.git', 'node_modules', '.venv', 'dist', '__pycache__'}

# Order matters: rename files inside directories BEFORE renaming directories.
# Do directories deepest-first.

FILE_RENAMES = [
    # Scripts in .agents/bin/
    (".agents/bin/document-parse.py", ".agents/bin/document-parse.py"),
    (".agents/bin/document-load.py", ".agents/bin/document-load.py"),
    (".agents/bin/document-search.py", ".agents/bin/document-search.py"),
    (".agents/bin/document-mcp-server.py", ".agents/bin/document-mcp-server.py"),
    # Agent files
    ("demo/.agents/document-eval-agent.md", "demo/.agents/document-eval-agent.md"),
    # Prebaked asset
    ("demo/assets/prebaked/document-review-checklist.md", "demo/assets/prebaked/document-review-checklist.md"),
    # Asset in contracts/ dir — rename file first, then dir
    ("demo/assets/documents/sample-consulting-agreement.md", "demo/assets/documents/sample-consulting-agreement.md"),
]

DIR_RENAMES = [
    # Skill directories (files inside already moved by git mv of whole dir)
    ("demo/.claude/skills/document-loader", "demo/.claude/skills/document-loader"),
    ("demo/.claude/skills/document-search", "demo/.claude/skills/document-search"),
    ("demo/.claude/skills/document-eval", "demo/.claude/skills/document-eval"),
    ("demo/.claude/skills/document-audit", "demo/.claude/skills/document-audit"),
    # Root-level symlinked/copied skill
    (".claude/skills/document-audit", ".claude/skills/document-audit"),
    # Asset directory (after file inside is moved)
    ("demo/assets/contracts", "demo/assets/documents"),
]


def phase1():
    print("=" * 60)
    print("PHASE 1: File and directory renames")
    print("=" * 60)
    renamed = []

    # File renames
    for src, dst in FILE_RENAMES:
        src_abs = os.path.join(REPO, src)
        if not os.path.exists(src_abs):
            print(f"  SKIP (not found): {src}")
            continue
        if is_git_tracked(src):
            # For files moving to a new directory, ensure parent exists
            dst_parent = os.path.dirname(os.path.join(REPO, dst))
            os.makedirs(dst_parent, exist_ok=True)
            git_mv(src, dst)
        else:
            plain_rename(src, dst)
        renamed.append((src, dst))

    # Directory renames
    for src, dst in DIR_RENAMES:
        src_abs = os.path.join(REPO, src)
        if not os.path.exists(src_abs):
            print(f"  SKIP (not found): {src}")
            continue
        if os.path.islink(src_abs):
            # It's a symlink — read target, remove, recreate
            target = os.readlink(src_abs)
            new_target = target.replace("contract-", "document-")
            os.unlink(src_abs)
            dst_abs = os.path.join(REPO, dst)
            os.makedirs(os.path.dirname(dst_abs), exist_ok=True)
            os.symlink(new_target, dst_abs)
            print(f"  symlink recreated: {dst} -> {new_target}")
            renamed.append((src, dst))
        else:
            # Real directory — use git mv
            git_mv(src, dst)
            renamed.append((src, dst))

    # Clean up empty contracts dir if it still exists
    contracts_dir = os.path.join(REPO, "demo/assets/contracts")
    if os.path.isdir(contracts_dir) and not os.listdir(contracts_dir):
        os.rmdir(contracts_dir)
        print(f"  removed empty dir: demo/assets/contracts")

    print(f"\n  Total renames: {len(renamed)}")
    return renamed


# --- Phase 2: content replacements ---

REPLACEMENTS = [
    # File paths and references
    ("document-parse.py", "document-parse.py"),
    ("document-load.py", "document-load.py"),
    ("document-search.py", "document-search.py"),
    ("document-mcp-server.py", "document-mcp-server.py"),
    ("document-eval-agent", "document-eval-agent"),
    ("document-loader", "document-loader"),
    ("document-search", "document-search"),
    ("document-eval", "document-eval"),
    ("document-audit", "document-audit"),
    ("document-review", "document-review"),

    # DB and collection names
    ("documents.db", "documents.db"),
    ("document_clauses", "document_clauses"),

    # Trigger commands
    ("/load-document", "/load-document"),
    ("/search-document", "/search-document"),
    ("/eval-document", "/eval-document"),
    ("/audit-document", "/audit-document"),

    # MCP tool names
    ("load_document", "load_document"),
    ("search_document", "search_document"),
    ("audit_document", "audit_document"),
    ("get_document_stats", "get_document_stats"),

    # Makefile variables
    ("DOCUMENT_SOURCE", "DOCUMENT_SOURCE"),

    # Asset paths
    ("assets/documents/", "assets/documents/"),

    # Prose (case-sensitive, order matters - do specific first)
    ("Document Review", "Document Review"),
    ("Document Eval", "Document Eval"),
    ("document analyst", "document analyst"),
    ("document review", "document review"),
    ("document clauses", "document clauses"),
    ("document counterparty", "document counterparty"),
    ("document-load", "document-load"),
    ("document-search", "document-search"),

    # Headers
    ("# document-", "# document-"),
    ("# Document", "# Document"),
]

SEARCH_DIRS = ["demo/", ".agents/", ".claude/"]
TEXT_EXTS = {'.py', '.md', '.json', '.toml', '.yaml', '.yml', '.sh', '.txt', ''}
# Also handle Makefile (no extension)


def should_process(filepath):
    """Decide if a file should have content replacements."""
    rel = os.path.relpath(filepath, REPO)

    # Must be under one of the search dirs
    if not any(rel.startswith(d) for d in SEARCH_DIRS):
        return False

    # Skip directories
    for skip in SKIP_DIRS:
        if f"/{skip}/" in f"/{rel}/" or rel.startswith(f"{skip}/"):
            return False

    # Skip presentation/ files
    if rel.startswith("presentation/"):
        return False

    # Skip binary files
    _, ext = os.path.splitext(filepath)
    if ext.lower() in BINARY_EXTS:
        return False

    # Must be text-like
    basename = os.path.basename(filepath)
    if basename == "Makefile":
        return True
    if ext.lower() in TEXT_EXTS:
        return True
    return False


def phase2():
    print("\n" + "=" * 60)
    print("PHASE 2: Content replacements")
    print("=" * 60)
    modified_files = {}

    for search_dir in SEARCH_DIRS:
        abs_dir = os.path.join(REPO, search_dir)
        if not os.path.isdir(abs_dir):
            continue
        for dirpath, dirnames, filenames in os.walk(abs_dir):
            # Prune skip dirs
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for fname in filenames:
                filepath = os.path.join(dirpath, fname)
                if not should_process(filepath):
                    continue
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                except (IOError, UnicodeDecodeError):
                    continue

                original = content
                count = 0
                for old, new in REPLACEMENTS:
                    if old in content:
                        n = content.count(old)
                        content = content.replace(old, new)
                        count += n

                if count > 0:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    rel = os.path.relpath(filepath, REPO)
                    modified_files[rel] = count
                    print(f"  {rel}: {count} replacement(s)")

    print(f"\n  Total files modified: {len(modified_files)}")
    return modified_files


# --- Phase 3: summary + residual scan ---

def phase3(renamed, modified):
    print("\n" + "=" * 60)
    print("PHASE 3: Summary")
    print("=" * 60)

    print(f"\nFiles/dirs renamed: {len(renamed)}")
    for src, dst in renamed:
        print(f"  {src} -> {dst}")

    print(f"\nFiles modified: {len(modified)}")
    for fpath, count in sorted(modified.items()):
        print(f"  {fpath}: {count} replacement(s)")

    # Residual scan — find remaining "contract" references
    print("\n" + "-" * 60)
    print("Residual 'contract' references (for manual review):")
    print("-" * 60)
    residuals = []
    for search_dir in SEARCH_DIRS:
        abs_dir = os.path.join(REPO, search_dir)
        if not os.path.isdir(abs_dir):
            continue
        for dirpath, dirnames, filenames in os.walk(abs_dir):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for fname in filenames:
                filepath = os.path.join(dirpath, fname)
                _, ext = os.path.splitext(filepath)
                if ext.lower() in BINARY_EXTS:
                    continue
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        for lineno, line in enumerate(f, 1):
                            if 'contract' in line.lower():
                                rel = os.path.relpath(filepath, REPO)
                                residuals.append((rel, lineno, line.rstrip()))
                except (IOError, UnicodeDecodeError):
                    continue

    if residuals:
        for rel, lineno, line in residuals:
            print(f"  {rel}:{lineno}: {line}")
    else:
        print("  None found.")
    print(f"\n  Total residual lines: {len(residuals)}")


if __name__ == "__main__":
    os.chdir(REPO)
    renamed = phase1()
    modified = phase2()
    phase3(renamed, modified)
    print("\nDone.")
