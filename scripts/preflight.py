from __future__ import annotations

import json
import pathlib
import py_compile
import sys
import ast

ROOT = pathlib.Path(__file__).resolve().parents[1]

REQUIRED = [
    "contracts/minima.py",
    "tests/direct/test_minima.py",
    "README.md",
    "NETWORK.md",
    "DEPLOYMENT.md",
    "gltest.config.yaml",
    "package.json",
    "package-lock.json",
    "requirements.txt",
    "docs/ARCHITECTURE.md",
    "docs/THREAT_MODEL.md",
    "docs/REVIEWER_DEMO.md",
    "docs/SUBMISSION_NOTES_DRAFT.md",
]

errors: list[str] = []

for rel in REQUIRED:
    if not (ROOT / rel).exists():
        errors.append(f"missing required file: {rel}")

if (ROOT / "frontend").exists():
    errors.append("frontend directory must not exist for the standalone contract submission")

contract = (ROOT / "contracts/minima.py").read_text(encoding="utf-8")
for needle in (
    'py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6',
    'gl.vm.run_nondet_unsafe',
    'permit.field_mask = u32(necessary)',
    'REQUEST_AMBIGUOUS',
    'if ambiguous != 0:',
    'is_permit_valid',
):
    if needle not in contract:
        errors.append(f"contract invariant marker missing: {needle}")

package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
if package.get("devDependencies", {}).get("genlayer") != "0.39.1":
    errors.append("package.json must pin repository-local genlayer CLI 0.39.1")

network = (ROOT / "NETWORK.md").read_text(encoding="utf-8")
for required in (
    "61999",
    "https://studio.genlayer.com/api",
    "https://explorer-studio.genlayer.com",
    "0.39.1",
):
    if required not in network:
        errors.append(f"network manifest missing {required}")

# Build forbidden preview tokens by concatenation so this guard does not trigger on itself.
forbidden = [
    "619" + "97",
    "studio" + "-dev",
    "studio" + "_dev",
    "explorer-studio" + "-dev",
]
scan_exts = {".md", ".txt", ".yaml", ".yml", ".json", ".py"}
ignored_parts = {".git", ".venv", "node_modules", "artifacts", "__pycache__"}
for path in ROOT.rglob("*"):
    if not path.is_file() or path.suffix.lower() not in scan_exts:
        continue
    if any(part in ignored_parts for part in path.relative_to(ROOT).parts):
        continue
    if path.resolve() == pathlib.Path(__file__).resolve():
        continue
    text = path.read_text(encoding="utf-8", errors="ignore").lower()
    for token in forbidden:
        if token.lower() in text:
            errors.append(f"forbidden preview-network token {token!r} in {path.relative_to(ROOT)}")

try:
    py_compile.compile(str(ROOT / "contracts/minima.py"), doraise=True)
    py_compile.compile(str(ROOT / "tests/direct/test_minima.py"), doraise=True)
except Exception as exc:
    errors.append(f"python syntax check failed: {exc}")

try:
    test_tree = ast.parse((ROOT / "tests/direct/test_minima.py").read_text(encoding="utf-8"))
    direct_tests = sum(
        1 for node in test_tree.body
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")
    )
    if direct_tests < 30:
        errors.append(f"adversarial Direct Mode suite is too small: {direct_tests} tests")
except Exception as exc:
    errors.append(f"could not count Direct Mode tests: {exc}")

if "PENDING" not in (ROOT / "DEPLOYMENT.md").read_text(encoding="utf-8"):
    print("NOTE: DEPLOYMENT.md has no PENDING markers; verify every value is real finalized evidence.")

if errors:
    print("MINIMA PREFLIGHT: FAIL")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)

print("MINIMA PREFLIGHT: PASS")
print(" - standalone contract only (no frontend)")
print(" - stable Studionet network manifest present")
print(" - repository-local CLI pin: 0.39.1")
print(" - preview-network contamination guard: clean")
print(" - core least-privilege invariant markers: present")
print(" - Python syntax checks: pass")
print(f" - adversarial Direct Mode test inventory: {direct_tests}")
