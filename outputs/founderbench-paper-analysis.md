# FounderBench KDD Paper Analysis

Validated single-run model rows: **11**.

Bootstrap intervals below estimate sensitivity to the 50-task mix. They are not repeated-run or model-sampling uncertainty.

## Frozen model registry

| Model | Score | Solved | Errors | Evidence | SHA-256 |
|---|---:|---:|---:|---|---|
| Gemini 3.5 Flash | 67.69 | 32/50 | 59 | `outputs/founderbench-gemini-3.5-flash.json` | `1d6f9c81af404cd81d46fe8c1483b435ff6b763f7d763fd6e735545b46abce78` |
| Grok 4.5 | 66.53 | 33/50 | 0 | `outputs/founderbench-xai.json` | `3ed7e30582bfb6413e4dce39067feb288c3a6a92a19be9f654a39afa14fe6684` |
| GPT-5.6 Sol | 66.39 | 32/50 | 0 | `outputs/founderbench-openai.json` | `55a021a120a83c27ec2c4621c2e4a3030e3746844e92499498b2ecc190aea04d` |
| Kimi K3 | 65.63 | 28/50 | 70 | `outputs/founderbench-kimi.json` | `4bb2850b393aa9af8cca301e18b85d1ed6af4575f8ade57e855ee0983ccbc36d` |
| Claude Sonnet 5 | 63.90 | 25/50 | 0 | `outputs/founderbench-anthropic-sonnet-5.json` | `e2b9843ece2a45c8020e52bcfc803b3457978083ebd318b46c3020089a837fb0` |
| DeepSeek V4 Reasoner | 62.43 | 27/50 | 3 | `outputs/founderbench-deepseek-v4-reasoner.json` | `212f7ef5324b210c0da7294eefd0b45443136d7c98d0781360b1a9e785877167` |
| Claude Sonnet 4.5 | 61.09 | 24/50 | 0 | `outputs/founderbench-anthropic.json` | `bdf9090c454a0a2cb42be936d52717add3df18375b9823b5bd7b0a536a06f364` |
| DeepSeek Chat | 56.59 | 23/50 | 0 | `outputs/founderbench-deepseek.json` | `2c8e50c654e3dfec4c6c4b5c5e8b22c33db15af3f7dcb7027c14c8bd15ced252` |
| GLM 4.5 Air | 54.78 | 23/50 | 0 | `outputs/founderbench-glm-4.5-air.json` | `9d9cd78bd67bf965db6a10f0bf591fd2c05f9df2bb746200cf08d642898f6a9c` |
| Gemini 2.5 Flash | 52.69 | 13/50 | 340 | `outputs/founderbench-gemini.json` | `e3ed80cf922e8a89f6764a11409440f3139b2d2fc7834f067b25061620d77a9e` |
| Grok 4.3 | 52.59 | 16/50 | 3 | `outputs/founderbench-xai-grok-4.3.json` | `9dd14b5699c7cb158defd59f145e177f32a1b371f27ce15a8c99d15267248f57` |

## Provider-error sensitivity

This is a diagnostic stratification, not a counterfactual corrected leaderboard. Error-free and errored task subsets differ in composition.

| Model | Error decisions | Affected tasks | Mean on affected tasks | Mean on unaffected tasks |
|---|---:|---:|---:|---:|
| Gemini 3.5 Flash | 59 | 25 | 73.57 | 61.80 |
| Grok 4.5 | 0 | 0 | — | 66.53 |
| GPT-5.6 Sol | 0 | 0 | — | 66.39 |
| Kimi K3 | 70 | 11 | 46.47 | 71.04 |
| Claude Sonnet 5 | 0 | 0 | — | 63.90 |
| DeepSeek V4 Reasoner | 3 | 3 | 60.66 | 62.55 |
| Claude Sonnet 4.5 | 0 | 0 | — | 61.09 |
| DeepSeek Chat | 0 | 0 | — | 56.59 |
| GLM 4.5 Air | 0 | 0 | — | 54.78 |
| Gemini 2.5 Flash | 340 | 44 | 50.33 | 70.03 |
| Grok 4.3 | 3 | 3 | 44.23 | 53.12 |

## Solved-versus-average rank reversals

These reversals occur because solved count thresholds each task at 70, while average score preserves distances above and below that threshold.

| Higher average-score model | Higher solved-count model | Average gap | Solved gap |
|---|---|---:|---:|
| Gemini 3.5 Flash | Grok 4.5 | 1.16 | 1 |
| Claude Sonnet 5 | DeepSeek V4 Reasoner | 1.47 | 2 |
| Gemini 2.5 Flash | Grok 4.3 | 0.10 | 3 |

## Task-aware family comparison

| Family | Task-aware score | Best hosted model | Best hosted score | Task-aware leads |
|---|---:|---|---:|---|
| Market selection | 59.77 | GPT-5.6 Sol | 59.38 | yes |
| First revenue | 69.25 | Claude Sonnet 5 | 68.93 | yes |
| Retention improvement | 95.78 | Grok 4.5 | 96.67 | no |
| Churn shock recovery | 91.18 | GPT-5.6 Sol | 95.20 | no |
| Demo Day traction | 88.82 | Claude Sonnet 4.5 | 68.00 | yes |
| Pricing | 85.59 | Gemini 3.5 Flash | 76.13 | yes |
| Runway preservation | 95.58 | Grok 4.3 | 94.36 | yes |
| Pivot decision | 65.48 | Claude Sonnet 5 | 47.05 | yes |
| Fundraising | 99.61 | Grok 4.5 | 86.54 | yes |
| Channel expansion | 57.97 | GPT-5.6 Sol | 57.77 | yes |
