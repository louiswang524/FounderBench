# FounderBench Prompt Protocol

Version: 0.3.0
Prompt version: `founderbench-task-agent`
Prompt template SHA-256: `21cfb19c6ce46b4f74d6d92dc994fca10237b86e166e5b886b5220bb4da15e8b`
Protocol SHA-256: `67b5335c955d256ed530cb39928eef1c583a78604cbcfa906c97d1f05ea2cae5`

## Contract

- Task count: 50
- Maximum actions per week: 4
- Response format: JSON object only with required keys `rationale` and `actions`.
- Parser: `founderbench.provider_adapter.parse_provider_response`.

## Action Vocabulary

`research_market`, `build_offer`, `run_campaign`, `improve_offer`, `hire_agent`, `support_customers`, `change_price`, `interview_customers`, `cut_cost`, `pivot_market`, `raise_funding`, `partner_channel`, `do_nothing`

## Prompt Rules

- Return only JSON with keys rationale and actions.
- Use at most 4 actions per week.
- Do not spend more cash than available.
- If an action needs market_id or offer_id, use one from the observation.
- Use do_nothing only when no useful action remains.
- Do not make unsupported claims; the simulator only executes structured actions.

## Provider Message Wrappers

| Provider | Policy | Default Model | Temperature | System Prompt Hash |
| --- | --- | --- | --- | --- |
| OpenAI GPT | `openai` | `gpt-4.1-mini` | 0.2 | `f6c7d18e41cb6b313f5951290d1d7aad5220334d073e1f4b54089ff5246ddf91` |
| DeepSeek | `deepseek` | `deepseek-chat` | 0.2 | `4464f7e398df3b5cc605ce515c39babc9e643706adc3a1e47df256134a55a37a` |
| Anthropic Claude | `anthropic` | `claude-sonnet-4-5` | 0.2 | `f6c7d18e41cb6b313f5951290d1d7aad5220334d073e1f4b54089ff5246ddf91` |
| Google Gemini | `gemini` | `gemini-2.5-flash` | 0.2 | `f6c7d18e41cb6b313f5951290d1d7aad5220334d073e1f4b54089ff5246ddf91` |
| Moonshot Kimi | `kimi` | `kimi-latest` | 0.2 | `f6c7d18e41cb6b313f5951290d1d7aad5220334d073e1f4b54089ff5246ddf91` |
| Alibaba Qwen | `qwen` | `qwen-plus` | 0.2 | `f6c7d18e41cb6b313f5951290d1d7aad5220334d073e1f4b54089ff5246ddf91` |
| Mistral | `mistral` | `mistral-large-latest` | 0.2 | `f6c7d18e41cb6b313f5951290d1d7aad5220334d073e1f4b54089ff5246ddf91` |
| Z.ai GLM | `glm` | `glm-4-plus` | 0.2 | `f6c7d18e41cb6b313f5951290d1d7aad5220334d073e1f4b54089ff5246ddf91` |
| xAI Grok | `xai` | `grok-3-mini` | 0.2 | `f6c7d18e41cb6b313f5951290d1d7aad5220334d073e1f4b54089ff5246ddf91` |
| Llama/Open-weight endpoint | `llama` | `meta-llama/Llama-3.1-70B-Instruct` | 0.2 | `f6c7d18e41cb6b313f5951290d1d7aad5220334d073e1f4b54089ff5246ddf91` |
| Local/OpenAI-compatible | `llm` | `Qwen/Qwen2.5-7B-Instruct` | 0.2 | `f6c7d18e41cb6b313f5951290d1d7aad5220334d073e1f4b54089ff5246ddf91` |

## Run Trace Requirements

- Record prompt_sha256 for every provider call.
- Record raw_response_redacted, parse/error category, token usage, estimated cost, and latency when available.
- Validate each complete suite with python -m founderbench.submission before comparing scores.

## Anti-Gaming Controls

- Models receive only the current task observation and allowed actions.
- The simulator executes structured actions only; natural-language business claims do not affect score.
- Public runs report prompt hashes, while hidden-holdout evaluation withholds private task definitions.

## Canonical Prompt Template

```json
{
  "benchmark": "FounderBench",
  "prompt_version": "founderbench-task-agent",
  "task": {
    "task_id": "<FND-###>",
    "name": "<task name>",
    "description": "<task objective and startup situation>",
    "weeks_remaining": "<integer>",
    "pass_threshold": 70
  },
  "objective": "Choose actions that maximize the bounded 0-100 task score. Preserve runway, avoid unsafe/spammy behavior, and satisfy the task objective.",
  "allowed_actions": "<sorted subset of action_types allowed by this task>",
  "observation": {
    "week": "<integer>",
    "cash": "<float>",
    "reputation": "<float>",
    "agent_capacity": "<float>",
    "markets": "<list of visible market records>",
    "offers": "<list of active offer records>",
    "memory": "<simulator notes from prior weeks>"
  },
  "response_schema": {
    "rationale": "brief reason",
    "actions": [
      {
        "type": "research_market | build_offer | run_campaign | improve_offer | hire_agent | support_customers | change_price | interview_customers | cut_cost | pivot_market | raise_funding | partner_channel | do_nothing",
        "market_id": "required for research_market/build_offer/pivot_market; optional for interview_customers",
        "offer_id": "required for run_campaign/improve_offer/change_price/pivot_market/partner_channel; optional for interview_customers",
        "budget": 0,
        "price": "used for build_offer/change_price; used as funding ask for raise_funding",
        "message_quality": 0.8
      }
    ]
  },
  "rules": [
    "Return only JSON with keys rationale and actions.",
    "Use at most 4 actions per week.",
    "Do not spend more cash than available.",
    "If an action needs market_id or offer_id, use one from the observation.",
    "Use do_nothing only when no useful action remains.",
    "Do not make unsupported claims; the simulator only executes structured actions."
  ]
}
```
