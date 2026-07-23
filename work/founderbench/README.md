# FounderBench (package README)

The public GitHub landing page is the repository root [`README.md`](../../README.md).

This directory contains the installable Python package (`founderbench`), tests, and the technical `SPEC.md`.

```bash
# from repository root
python -m pip install -e .
python -m unittest discover -s work/founderbench/tests -v
python -m founderbench.task_cli --policy task_heuristic --task FND-001 --trace
```

License: MIT (see [`LICENSE`](LICENSE) and the repository root [`LICENSE`](../../LICENSE)).
Citation: see [`CITATION.cff`](CITATION.cff).
