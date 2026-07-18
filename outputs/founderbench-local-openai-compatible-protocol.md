# FounderBench Local/Open-Source Model Protocol

This protocol runs a local or open-source model through an OpenAI-compatible `/v1/chat/completions` endpoint.

## Environment

- `FOUNDERBENCH_COMPAT_BASE_URL`: `http://localhost:8000/v1`
- `FOUNDERBENCH_COMPAT_MODEL`: `Qwen/Qwen2.5-7B-Instruct`
- `FOUNDERBENCH_COMPAT_API_KEY`: `optional for local servers; do not commit real keys`

Legacy `OPENAI_COMPAT_*` names are still accepted as aliases, but `FOUNDERBENCH_COMPAT_*` is preferred.

## URL Usage

- Base URL: `http://localhost:8000/v1`
- Chat completions: `http://localhost:8000/v1/chat/completions`
- Models health check: `http://localhost:8000/v1/models`

## Commands

```powershell
python -m founderbench.local_model protocol --output outputs/founderbench-local-openai-compatible-protocol.json
```
```powershell
python -m founderbench.local_model health --output outputs/local-health.json
```
```powershell
python -m founderbench.resumable_runner --policy llm --output outputs/founderbench-local-open-model.json --resume --audit
```
```powershell
python -m founderbench.submission --input outputs/founderbench-local-open-model.json --report outputs/founderbench-local-open-model-submission-report.md
```

## Reporting Requirements

- model id and exact checkpoint or quantization
- inference server and version
- hardware
- decoding settings
- raw run JSON
- submission validation report
- representative redacted audit traces
