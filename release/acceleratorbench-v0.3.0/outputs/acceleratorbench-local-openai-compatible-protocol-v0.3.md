# FounderBench Local/Open-Source Model Protocol

This protocol runs a local or open-source model through an OpenAI-compatible `/v1/chat/completions` endpoint.

## Environment

- `OPENAI_COMPAT_BASE_URL`: `http://localhost:8000/v1`
- `OPENAI_COMPAT_MODEL`: `Qwen/Qwen2.5-7B-Instruct`
- `OPENAI_COMPAT_API_KEY`: `optional for local servers; do not commit real keys`

## Commands

```powershell
python -m moneybench.local_model protocol --output outputs/acceleratorbench-local-openai-compatible-protocol-v0.3.json
```
```powershell
python -m moneybench.local_model health --output outputs/local-health.json
```
```powershell
python -m moneybench.resumable_runner --policy llm --output outputs/acceleratorbench-local-open-model-v0.3.json --resume --audit
```
```powershell
python -m moneybench.submission --input outputs/acceleratorbench-local-open-model-v0.3.json --report outputs/acceleratorbench-local-open-model-submission-report.md
```

## Reporting Requirements

- model id and exact checkpoint or quantization
- inference server and version
- hardware
- decoding settings
- raw run JSON
- submission validation report
- representative redacted audit traces
