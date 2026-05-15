"""Launch script for obfuscated-argument debate eval.

Sets API keys from the Windows process environment before calling inspect.
Run with: python examples/debate/run_obfuscated.py
"""
import os
import subprocess
import sys


def get_win_env(var: str) -> str:
    result = subprocess.run(
        ["powershell.exe", "-NonInteractive", "-NoProfile", "-Command",
         f"Get-ChildItem Env:{var} -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Value"],
        capture_output=True, text=True, timeout=10,
    )
    return result.stdout.strip()


# Pull keys from the Windows process environment (where Claude Code stores them)
for var in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY"):
    val = get_win_env(var)
    if val:
        os.environ[var] = val

QIDS = [
    "recommendation_ranking",
    "round_robin_tournament",
    "graph_hamiltonian_cycle",
    "medical_decision_tree",
    "rsa_ciphertext_valid",
    "telecom_steiner_tree",
    "parrondo_games",
]

qids_arg = str(QIDS).replace("'", '"')  # JSON-style list

cmd = [
    sys.executable, "-m", "inspect_ai", "eval",
    "examples/debate/tasks.py@obfuscated_sample",
    "--model", "openai/gpt-4o-mini",
    "-T", f"qids={qids_arg}",
    "--max-connections", "3",
]

print("Running:", " ".join(cmd))
result = subprocess.run(cmd, cwd=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.exit(result.returncode)
