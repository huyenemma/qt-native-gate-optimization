"""Export all saved run results (raw-count JSON files) to one CSV, without touching the QPU.

One row per (run, optimization level, n), largest n first, so each block reads like the heatmap:
  fresh_1 .. fresh_N  P(ancilla y = 1) of the FRESH circuit with n repetitions (empty where y > n)
  recycle             P(ancilla = 1) of the RECYCLE circuit with n repetitions
followed by metadata read from the saved files:
  backend, shots, seed_transpiler, data_qubits (Qiskit indices; empty = chosen by the transpiler),
  {fresh,recycle}_time    time the result was saved (UTC), right after the job finished
  {fresh,recycle}_job_id  IQM job id
  {fresh,recycle}_cz, {fresh,recycle}_depth  two-qubit gate count / depth of the executed circuit (if recorded)
  note                    setup derived from the metadata + free text from RUN_NOTES
A (run, optimization level) is exported only if both FRESH and RECYCLE have exactly n = 1..N;
other depths and unfinished runs are skipped.

Usage:
  python export_csv.py                    # all runs in data/q20 -> data/q20/results.csv
  python export_csv.py data/q20/run6 ...  # selected run folders
"""
import glob
import json
import os
import re
import sys

import pandas as pd

import fresh
import recycle
from utils import load_counts

DATA_ROOT = "data/q20"
OUT_FILE = os.path.join(DATA_ROOT, "results.csv")
N = 7  # number of plaquette repetitions a complete result set must have
FILE_RE = re.compile(r"(fresh|recycle)_opt(\d+)_n(\d+)\.json$")

# free-text notes per run, added to the "note" column
RUN_NOTES = {
    "run1": "qubits chosen by the transpiler for every circuit, so FRESH and RECYCLE ran on different data qubits",
    "run2": "first FRESH job (opt 0, n = 1) failed with an IQM internal server error and was resubmitted",
}


def find_results(run_dir):
    # {opt: {strategy: {n: path}}}
    found = {}
    for path in glob.glob(os.path.join(run_dir, "*.json")):
        m = FILE_RE.search(os.path.basename(path))
        if m:
            kind, opt, n = m.group(1), int(m.group(2)), int(m.group(3))
            found.setdefault(opt, {}).setdefault(kind, {})[n] = path
    return found


def read_meta(path):
    with open(path) as f:
        record = json.load(f)
    record.pop("counts")
    return record


def setup_note(run, fresh_meta, recycle_meta):
    pinned = fresh_meta.get("initial_layout") is not None
    parts = ["data qubits pinned" if pinned else "qubits not pinned",
             f"routing seed {fresh_meta['seed_transpiler']}" if fresh_meta.get("seed_transpiler") is not None
             else "unseeded (random) routing"]
    if fresh_meta["shots"] != recycle_meta["shots"]:
        parts.append(f"RECYCLE shots = {recycle_meta['shots']}")
    if run in RUN_NOTES:
        parts.append(RUN_NOTES[run])
    return "; ".join(parts)


def rows_for(run, opt, fresh_paths, recycle_paths):
    rows = []
    for n in range(N, 0, -1):
        row = {"run": run, "opt_level": opt, "n": n}
        histogram = load_counts(fresh_paths[n])
        for y in range(1, N + 1):
            # same bit extraction as fresh.get_ancilla_probabilities: y = ancilla of the y-th plaquette
            row[f"fresh_{y}"] = fresh.calculate_ancilla(histogram, n, n - y + 1) if y <= n else None
        row["recycle"] = recycle.calculate_ancilla(load_counts(recycle_paths[n]))

        meta = {"fresh": read_meta(fresh_paths[n]), "recycle": read_meta(recycle_paths[n])}
        layout = meta["fresh"].get("initial_layout")
        row.update({
            "backend": meta["fresh"]["backend"],
            "shots": meta["fresh"]["shots"],
            "seed_transpiler": meta["fresh"].get("seed_transpiler"),
            "data_qubits": " ".join(map(str, layout[:4])) if layout else None,
        })
        for kind in ("fresh", "recycle"):
            compiled = meta[kind].get("compiled") or {}
            row[f"{kind}_time"] = meta[kind]["timestamp"][:19].replace("T", " ")
            row[f"{kind}_job_id"] = meta[kind]["job_id"]
            row[f"{kind}_cz"] = compiled.get("num_2q_gates")
            row[f"{kind}_depth"] = compiled.get("depth")
        row["note"] = setup_note(run, meta["fresh"], meta["recycle"])
        rows.append(row)
    return rows


if __name__ == "__main__":
    run_dirs = sys.argv[1:] or sorted(d for d in glob.glob(os.path.join(DATA_ROOT, "*")) if os.path.isdir(d))
    complete = set(range(1, N + 1))
    rows = []
    for run_dir in run_dirs:
        run = os.path.basename(os.path.normpath(run_dir))
        for opt, by_kind in sorted(find_results(run_dir).items()):
            fresh_paths, recycle_paths = by_kind.get("fresh", {}), by_kind.get("recycle", {})
            if set(fresh_paths) != complete or set(recycle_paths) != complete:
                print(f"skipped {run} opt{opt}: FRESH n = {sorted(fresh_paths)}, RECYCLE n = {sorted(recycle_paths)}")
                continue
            rows += rows_for(run, opt, fresh_paths, recycle_paths)

    df = pd.DataFrame(rows)
    # whole numbers stay whole even where older runs have no value
    int_cols = ["seed_transpiler"] + [f"{k}_{c}" for k in ("fresh", "recycle") for c in ("cz", "depth")]
    df[int_cols] = df[int_cols].astype("Int64")
    df.to_csv(OUT_FILE, index=False)
    print(f"{OUT_FILE}: {len(rows) // N} (run, opt_level) blocks")
