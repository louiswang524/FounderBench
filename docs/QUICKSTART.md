# FounderBench Quickstart

## Install

Linux/macOS:

```bash
git clone https://github.com/louiswang524/FounderBench.git
cd FounderBench
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

Windows PowerShell:

```powershell
git clone https://github.com/louiswang524/FounderBench.git
cd FounderBench
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
```

## Validate The Benchmark

Linux/macOS:

```bash
python -m unittest discover -s work/founderbench/tests -v
python -m founderbench.release validate
```

Windows PowerShell:

```powershell
python -m unittest discover -s work\founderbench\tests -v
python -m founderbench.release validate
```

## Inspect Tasks

Linux/macOS:

```bash
python -m founderbench.export_tasks --output outputs/founderbench-task-manifest.json
python -m founderbench.task_cards --json-output outputs/founderbench-task-cards.json --markdown-output outputs/founderbench-task-cards.md
```

Windows PowerShell:

```powershell
python -m founderbench.export_tasks --output outputs\founderbench-task-manifest.json
python -m founderbench.task_cards --json-output outputs\founderbench-task-cards.json --markdown-output outputs\founderbench-task-cards.md
```

## Run A Single Task

Linux/macOS:

```bash
python -m founderbench.task_cli --policy task_heuristic --task FND-001 --trace
```

Windows PowerShell:

```powershell
python -m founderbench.task_cli --policy task_heuristic --task FND-001 --trace
```

## Run All Public Tasks

Linux/macOS:

```bash
python -m founderbench.task_cli --policy heuristic
```

Windows PowerShell:

```powershell
python -m founderbench.task_cli --policy heuristic
```

## Regenerate The Release Artifacts

Linux/macOS:

```bash
python -m founderbench.release regenerate
python -m founderbench.release validate
python -m founderbench.release bundle
```

Windows PowerShell:

```powershell
python -m founderbench.release regenerate
python -m founderbench.release validate
python -m founderbench.release bundle
```

