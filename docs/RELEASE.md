# Release And Publication Checklist

Before making the repository public:

1. Choose an open-source license and add a root `LICENSE` file.
2. Replace placeholder fields in `work/moneybench/CITATION.cff`.
3. Verify the repository links in `pyproject.toml`, `README.md`, and `CITATION.cff`.
4. Run `python -m moneybench.release validate`.
5. Run `python -m moneybench.release bundle`.
6. Run a secret scan over `work/moneybench`, `outputs`, and `release`.
7. Review `outputs/acceleratorbench-submission-gate-v0.3.md` and `outputs/acceleratorbench-publication-audit-v0.3.md`.

Current v0.3.0 limitation: hosted LLM provider comparisons and real private hidden-holdout results must not be claimed until completed and validated.
