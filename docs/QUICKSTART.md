# FounderBench Quickstart

## Install

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
```

## Validate The Benchmark

```bash
python -m unittest discover -s work/moneybench/tests -v
python -m moneybench.release validate
```

## Inspect Tasks

```bash
python -m moneybench.export_tasks --output outputs/founderbench-task-manifest.json
python -m moneybench.task_cards --json-output outputs/founderbench-task-cards.json --markdown-output outputs/founderbench-task-cards.md
```

## Run A Single Task

```bash
python -m moneybench.task_cli --policy task_heuristic --task FND-001 --trace
```

## Run All Public Tasks

```bash
python -m moneybench.task_cli --policy heuristic
```

## Regenerate The Release Artifacts

```bash
python -m moneybench.release regenerate
python -m moneybench.release validate
python -m moneybench.release bundle
```

