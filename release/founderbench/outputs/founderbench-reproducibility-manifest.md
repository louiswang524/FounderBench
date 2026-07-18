# FounderBench Reproducibility Manifest

This generated manifest records the source/output hashes and reproduction commands for the current workspace. It records only secret variable names, never secret values.

## Environment

| Field | Value |
| --- | --- |
| Python | 3.12.10 |
| Python executable | C:\Users\louis\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\python.exe |
| Platform | Windows-11-10.0.26200-SP0 |
| Machine | AMD64 |
| Working directory | C:\Users\louis\Documents\Codex\2026-07-14\use\work\founderbench |
| Git commit | b7cd217866bda332762a940f2abc9ecef2e0a038 |
| Secret values recorded | False |

## Commands

| Purpose | Working Directory | Command |
| --- | --- | --- |
| Regenerate all generated current release artifacts | work/founderbench | `python -m founderbench.release regenerate` |
| Run tests and validate required outputs | work/founderbench | `python -m founderbench.release validate` |
| Build supplementary release bundle | work/founderbench | `python -m founderbench.release bundle` |

## Core Source Files

| Path | Exists | Bytes | SHA-256 |
| --- | --- | --- | --- |
| work/founderbench/founderbench/action_ablation.py | True | 11627 | 54c3d06edc79d45c67a6ca7311d9e3bd65b3d902abacb731530e08cb0dac68d1 |
| work/founderbench/founderbench/action_semantics.py | True | 12872 | 666c494e8916fb4fe65dfdd145012b8b4c64edd7e9e1086a3d869c94427fdb68 |
| work/founderbench/founderbench/baseline_execution_plan.py | True | 16257 | 92caef065f31b3171d867ba3e65e3e902d4c70a2a4591d4a7b80f1d0a9095829 |
| work/founderbench/founderbench/benchmark_datasheet.py | True | 11702 | 9f250c29419a6080458ba8c8f9e76874cecf2ca12e8da365de64d2907d7b95f1 |
| work/founderbench/founderbench/bundle_integrity.py | True | 6118 | 6bd26fbafcd84015b4eecf0ab902a33985f421b1ca2965bac2847bc4a9c55408 |
| work/founderbench/founderbench/citation_audit.py | True | 11027 | df083b1d0d9f1f70676250113d748f8c4e9a6b298ccb9fb3a0c6be7c32f69f5d |
| work/founderbench/founderbench/completion_audit.py | True | 16934 | 7041593517bbb5bed7435ef2e1a50423340d075dbd96b049645d89a9e79f84ec |
| work/founderbench/founderbench/contamination_leakage_audit.py | True | 11032 | d05532df97cc8a91f75fd4c21deebefe9b95d379a1f06e050c2d7548ce0bd8e8 |
| work/founderbench/founderbench/cost_accounting.py | True | 8483 | e4c266377447785ff952a44de5277df1c3c99efd5ef78e963365e74919c83f15 |
| work/founderbench/founderbench/determinism_audit.py | True | 6320 | 8dc6a065938e2a8446f8f1a8016337c2cb213c9b9f6859ff651932fd575ccf10 |
| work/founderbench/founderbench/environment_report.py | True | 7384 | 011ae101999f58f7cc76edd33159e1b7bb1097c5a21f6bf4fd841c079cecdd68 |
| work/founderbench/founderbench/env.py | True | 17665 | ba3a31f3f4655d6a7988b8cb30cbea0a4abc4d309250be8aeff4f1ecd72f3fcf |
| work/founderbench/founderbench/experiment_runbook.py | True | 14085 | b71aa9bef7a9815aca3ee27263802c846b7587bcb154f56f5541284a739f68f8 |
| work/founderbench/founderbench/failure_mode_audit.py | True | 14748 | 671d3c5f807a0e7977227b41b1a977716ae0d24836be288d550b9ca7df39204c |
| work/founderbench/founderbench/holdout_smoke.py | True | 5696 | 26ae665d5dccd80ad03d8f9fd3b5bb298385bd573ad1575be5d7cd21dbce9524 |
| work/founderbench/founderbench/human_calibration.py | True | 9513 | 4faec0573771743aa8e4cc2b0a5d1ed068d04dcc823373fc1f259c8477a56aff |
| work/founderbench/founderbench/human_calibration_analysis.py | True | 12171 | 3c9de21c3248a3980beb6eba265c9f534f7b787968ceed6ba78d38fce213ceed |
| work/founderbench/founderbench/human_calibration_packet.py | True | 12073 | 27300023239d31874e11caa213bc9d0e2d1d9539e282205cdc8b6085dde6ac84 |
| work/founderbench/founderbench/human_calibration_schema.py | True | 9720 | 70cda560e35391951f3adb2c3cf881c8b2549516b01afd9153e1955b9307b795 |
| work/founderbench/founderbench/leaderboard_policy.py | True | 9088 | 40023b483aa067918a42d103156273774f813ecfb592969539e90948fa8ebb1a |
| work/founderbench/founderbench/leaderboard_stability.py | True | 10450 | 8867bab6a72299de7a32a755719fa5971ccc65503985eb9fb271ad47ff911dbc |
| work/founderbench/founderbench/market_catalog.py | True | 8477 | a331819eb40a30cbe606206fb46f57aa207a03233b6a19eae98dc95afafb7be3 |
| work/founderbench/founderbench/tasks.py | True | 34135 | 620c586982ae3fe06899a3bb366e89c1d5cde57aec7f518b1156ba2e63ccec95 |
| work/founderbench/founderbench/task_cards.py | True | 7785 | 3c4ebe219310be0d4a66fc7428d6cdaab89f5d390f4aa5243a22cea710096967 |
| work/founderbench/founderbench/task_feasibility_audit.py | True | 10949 | 47a8afa7115ddc8de62d045edb0a90ac298faf662d1410e874c5bed9ae035e20 |
| work/founderbench/founderbench/task_runner.py | True | 9544 | 557f4b9c42738b06ae0cc146364c5692d8c6e5dd917598626e807693b831d858 |
| work/founderbench/founderbench/task_provenance.py | True | 12157 | 5aa249c7c8e9373f23545834133b1f5ac3eafea0a1b8c3ed2e735758ccf0c66f |
| work/founderbench/founderbench/task_revision_ledger.py | True | 10220 | feb20a522e90a8c685f4c82cfb2ace89bdc989afeb2d3b3a5ac7ec1c40dc21c1 |
| work/founderbench/founderbench/policies.py | True | 17055 | a3474fbf6de7c1b5da4d440ff90b1945504bf9a32148d80eea38ce6d9dfda223 |
| work/founderbench/founderbench/difficulty_calibration.py | True | 12235 | c136f65d8600085765bccc579bc42ea4179b68922a21cfb08f9e677a46539253 |
| work/founderbench/founderbench/llm_policy.py | True | 18353 | d833247cd20680a164eaf203fe8807d11e2cbcd2e695362cd42690fa3c1a56b5 |
| work/founderbench/founderbench/metric_sensitivity.py | True | 11162 | de915f79dade6336b27a90327871f1e62352cd0d6c5dbe6dc2386fde0ce3ef9e |
| work/founderbench/founderbench/model_comparison.py | True | 9212 | cfa33c2716e58daafe039f849486f26e4802efb1e2c57521d901e0d16e3e11dd |
| work/founderbench/founderbench/model_result_cards.py | True | 11102 | 02608a7c5df3c7924db2ee6f1f99924399c06c2f49ba11e8a1a8df91663e90ed |
| work/founderbench/founderbench/paper_claim_lint.py | True | 8991 | 8ae9619d0409386b9449a50b17bc99d88681569e0bc280e7cfb409d2588cda66 |
| work/founderbench/founderbench/paper_evidence_map.py | True | 13775 | 7a83027ecfe7f96fcca5876ebd6208eb5fc2f04747d113ac037d3cd4232106d3 |
| work/founderbench/founderbench/paper_figures.py | True | 8902 | 8b5d23f91c3c9e67f58a2d8686a00e1e566c751d39f44575442560e92e8e9c30 |
| work/founderbench/founderbench/paired_statistics.py | True | 11014 | 3dbe752b2b3f521523e88654b253490ff80a87fa6140573fa52202739fc7a25f |
| work/founderbench/founderbench/power_analysis.py | True | 9117 | 3aad5932c9356034949573ceac58529496cc96bb63d40063eb9c2d39fc57cbef |
| work/founderbench/founderbench/prompt_protocol.py | True | 8150 | 0d891d5febf59ed0cbddb0cf6866e78696d431aa02f325db01aa2ef0415981e9 |
| work/founderbench/founderbench/private_holdout_evaluator.py | True | 7766 | 24a1c1579cd8d992545031140ef3352945afa3377f3e15d7fbbc4c63384f3f5b |
| work/founderbench/founderbench/provider_comparability_audit.py | True | 10173 | bff126997e913c951ce6f400d521e3a8c037c8a010b2204eddef772651b09280 |
| work/founderbench/founderbench/provider_contract_audit.py | True | 9134 | d3450247b5bee0c79a12bd9265666bf138e8c3bd6d2843575316cf19fda18de0 |
| work/founderbench/founderbench/provider_run_status.py | True | 11070 | 495dc70ba9c70e7e66b2c830a4bc4f301dccf7a725509fc4ae8f3cd784997d94 |
| work/founderbench/founderbench/release_metadata.py | True | 7649 | 53981e59728c5a20e3ba428609c2df07cb94b3bb3b52758ed635ca988d12dc69 |
| work/founderbench/founderbench/responsible_use.py | True | 9411 | a8a93fc55711924dbab436b8f5c6f407eae603bd5f1aabb65516358ac93a3865 |
| work/founderbench/founderbench/result_integrity_audit.py | True | 10087 | f124e7af05e8d03f75ba6cb28a3b8a2b9a34ab0aeed09079bdb9da66ae689912 |
| work/founderbench/founderbench/reviewer_risk_audit.py | True | 16237 | 19b688040a0e795aa640274b861eb0ecebd13e35c3646991c26179e0969adf2f |
| work/founderbench/founderbench/reviewer_smoke.py | True | 5965 | 28a558a1f7e34de455a08ff0129a3e9f7158412f9f464db43c6ea07e9e02a43a |
| work/founderbench/founderbench/simulator_invariant_audit.py | True | 12749 | f520fc2d1fd4024c18df132306fc0f32be5f79f86b00a177e3e8523f1ceba4a1 |
| work/founderbench/founderbench/scoring_consistency_audit.py | True | 11197 | f0ee2f307355f845bdc4a40b83f6a098992a491aefe9fcf06827dfc33b37d507 |
| work/founderbench/founderbench/statistical_protocol.py | True | 8731 | ae5e9eb463734e8d699fc5bbe94183f46d7f585e1055e113c11a5a0e888a91dd |
| work/founderbench/founderbench/submission.py | True | 8913 | db3c30122c5b906fb57062af409b2e8e80f3bc2d30168c7166f94af9d1e145f6 |
| work/founderbench/founderbench/submission_action_plan.py | True | 9838 | 8ad83f33fa091a708a5a5a863ae5892e480f92857ab3ead4b70c1c7ec8810e3c |
| work/founderbench/founderbench/submission_bundle.py | True | 8809 | 8d44dab7e566026c9bceed78917c2be513c02d377df8ceaf8f11a97da72ac897 |
| work/founderbench/founderbench/submission_manifest.py | True | 10876 | 10ea0f8dc898234fad855a100b1ea43ab14aeea874e9d9658bd158c736464a37 |
| work/founderbench/founderbench/submission_schema.py | True | 9386 | 7b6c6c352a7ffe338594d51354554b18ad9f86adb2eacc6b0fe832fc681cf4fe |
| work/founderbench/founderbench/release.py | True | 30881 | b7cf6205e236017a273074dbde41fb42044b2a548cdf7ec707819abcb41b711f |
| work/founderbench/founderbench/resumable_runner.py | True | 4750 | 3f061139fe9c550345488586106c576fcafad6e6da291457beef93507db914e5 |
| work/founderbench/tests/test_founderbench.py | True | 69301 | e259b542649bf02202d98110d9a4f3c63dc4bd744201a1a906dacebf9ff29376 |
| work/founderbench/README.md | True | 20930 | e33581112e626d6d9ddbde84a0d16a7734cb8c867592888bbf484a3441480a9f |
| work/founderbench/SPEC.md | True | 9647 | e9c2bc9ac95a9dc05174bdb4cd63d7a955bb6eaa18d044d8d61d662eedfcf314 |
| work/founderbench/CITATION.cff | True | 554 | c89452bacf9e1273d9c4cb2fef691b1f6e95af6e9b96e3c316dcec398c44582c |
| work/founderbench/CITATION.cff.template | True | 582 | 0f537b4c02dece317c61dcb1ea1a49470049450e45eae7ffac1ae5958e2f452d |
| work/founderbench/LICENSE-TODO.md | True | 361 | c14a53909dd6844c3eb87cf091891b87354ab7f269178acd2a4b7ad46f66a718 |
| work/founderbench/LICENSE.template | True | 468 | 8cc06a02dd899e20296dee91cff7285024691f09ca39c16a63be34f134c853f6 |

## Core Output Files

| Path | Exists | Bytes | SHA-256 |
| --- | --- | --- | --- |
| outputs/founderbench-task-manifest.json | True | 33747 | 8b5a4abb4452d30a1fca05e626693c890561ecd67987cf2e691448e0bb95b07e |
| outputs/founderbench-task-coverage.md | True | 3566 | 245976e316d20abdb0691210a730f1ac72ba26645b6a86736718d4e8d9396a3f |
| outputs/founderbench-task-provenance.md | True | 3767 | f0b2376044e91a9b3055543ffcc0c18c31c3c08f0390118b53684b782ce6fced |
| outputs/founderbench-task-provenance.json | True | 33755 | 985fb77382af6527e5341e958a91df59751798b3be42d0da6aed30e5477aa4ba |
| outputs/founderbench-task-cards.md | True | 38555 | 4c19b815b7c0fba1c699792ca28e773df0298074d0886830f8e0f148ff7f745b |
| outputs/founderbench-task-cards.json | True | 66561 | b58e2347fb9c375f1b5ae51b7487cd412d9721099daab8240f3b1b2256fac608 |
| outputs/founderbench-action-semantics.md | True | 8403 | c5901daef43abe62c4b412985bdee4364dd3836495f6d9740a1f18cbfbc1019c |
| outputs/founderbench-action-semantics.json | True | 8747 | 819c5e3da1b488d480f3c5bb3416c28e77ecee9bcf2925ce3f454f63343b7b9b |
| outputs/founderbench-datasheet.md | True | 5208 | c30333e5db0ef57eb7708d9bd06e3bc1c1c79cf7d23800b321195316b38089d1 |
| outputs/founderbench-datasheet.json | True | 6665 | a8449c388a57df90ad919b197de4e72248131935d1e1671e9413a341dd56209e |
| outputs/founderbench-market-catalog.md | True | 5295 | c39ff61695e7bd41c272b690ad022a82c8415eeb92263d04de637347ae3fa7c7 |
| outputs/founderbench-market-catalog.json | True | 8028 | 7a8d132bf1e896d53bfc9f17d0b8d612831c9c37651acde2e687d6aacbe74b4f |
| outputs/founderbench-score-rubric.md | True | 7092 | e96e5291dc4fb63df751120f29de761e3dc6f81fc82f85df8b601b0452f40869 |
| outputs/founderbench-scoring-consistency-audit.md | True | 3807 | 4770e332fc1e116732d17ffa16be899dda2dc641bbbb03c9ef689de6b6945143 |
| outputs/founderbench-scoring-consistency-audit.json | True | 6412 | b35980d1b503ed4bc9cb28eb64408f13c89cd10edf3b163ede8d5945f0efbdec |
| outputs/founderbench-metric-sensitivity.md | True | 3113 | 8eccfaa7eb6d48d331e50540584969ed006e9a30ffb8559c21ebc98159004407 |
| outputs/founderbench-metric-sensitivity.json | True | 5830 | 00fe5135a0d2b82caa0d8b9f67d92dbb13641688155e5f691f953299552c5f66 |
| outputs/founderbench-baseline-raw.json | True | 342083 | c3cd633784859b1a96dfd894995edf677308653d6d4631b061462fc11b9bdf89 |
| outputs/founderbench-baseline-leaderboard.json | True | 2652 | b3ca327f9546ec5c7bcbd43e3547ab5e7001d397d52fe6efec1199cd33fd08ad |
| outputs/founderbench-leaderboard-policy.md | True | 3389 | 8b4e662acee660b0c8854735f14216e7e43ea200444a4da68c7bd8e798cb5341 |
| outputs/founderbench-leaderboard-policy.json | True | 4124 | 33eaf58ab0cf74f01b83e61a28c794e10fffa85d53e1aa53a1e2c64511a900d1 |
| outputs/founderbench-leaderboard-stability.md | True | 3181 | dc9a94adb6cd36d440c85720757fff8ea8a174a97f0c697d6b124db16b081f7a |
| outputs/founderbench-leaderboard-stability.json | True | 7593 | 401cd7098887e5618e693e57bbfbd9333a155a00e2d74d5703e3c1cb7dcc3b76 |
| outputs/founderbench-baseline-analysis.md | True | 4380 | ac32eeb85d6ef3d99ce300f6acf81fd66a4007120f22665864795512166045ae |
| outputs/founderbench-result-integrity-audit.md | True | 1582 | 5775845487070b74036712353911ec7f97efeb221601cc7afedd262fa818830c |
| outputs/founderbench-result-integrity-audit.json | True | 2081 | 5555e71699734b2144f4f45320332a224b1c5ce573e65dcfabc56ba6bc668d36 |
| outputs/founderbench-paper-tables.md | True | 5429 | 6ec602030fc3d9cb51c9e429df32bc14ee2d69d1601b4357df52817773d076f3 |
| outputs/founderbench-paper-figure-data.md | True | 1628 | 045386e39beec6bb40748ee699f81bdd780713ea7ce7d181f17cb722396fd130 |
| outputs/founderbench-paper-figure-data.json | True | 15206 | 315f479ff4babf5b4ba8e69977615ee9a5748fac84f090944419331ce5985fc0 |
| outputs/founderbench-paper-evidence-map.md | True | 8114 | 3b68f9a27005b150c26bd69d1a823ebeab26235e8e963fc454589168699403f0 |
| outputs/founderbench-paper-evidence-map.json | True | 17081 | 0ff354d6ac6941be01b3966338dd99e59dffa46a51ad8132fd10772a0004de97 |
| outputs/founderbench-paper-claim-lint.md | True | 1530 | fda867ae783089d7b24915233e013da0e1093a814bc9164a9cd33e772ae6ec43 |
| outputs/founderbench-paper-claim-lint.json | True | 1880 | d76476b488e2c8f2ceb2f1bd3338e89cc815e992057d56802127fe34c0f2be3c |
| outputs/founderbench-citation-audit.md | True | 2651 | 46ab5552ddf6460b39f618f456334f09fdb7d233d437cc65c0a27889ce3b56f8 |
| outputs/founderbench-citation-audit.json | True | 8482 | 4fc888f481fcc2c0ed889f4c16c3ed79bbad8d57d96f843a10def84d200d5b64 |
| outputs/founderbench-model-comparison.md | True | 5442 | 4aac8e544739e821c9a079149f658f9e715b3b63bd5dadac9307a28d02150449 |
| outputs/founderbench-model-comparison.json | True | 14115 | a6fa7a479d4bc440faa1547b0b6607223204cbb0e924e77cdfa121981171f386 |
| outputs/founderbench-model-result-cards.md | True | 4209 | 2037d912af5c527631eeada3504ebe99502541e6ee7d18d421f08871945da343 |
| outputs/founderbench-model-result-cards.json | True | 12073 | a3f0fb2626a4451e1fb7c69427a6660e80a32be0ae7957754bbb4e993fd61e15 |
| outputs/founderbench-ablation-report.md | True | 2444 | 7ca23db2ffa0ac21a917349eac06a9297147f28afb3cecd7d9ee008205c47fb2 |
| outputs/founderbench-action-ablation.md | True | 2372 | f0439186b7f1ba3d7ef0fac8f6617ad03484ca54db16044bc58d212d3b9f45af |
| outputs/founderbench-action-ablation.json | True | 643447 | 0122ae9d8c41b52b6edd9b0fa787420204d1d71f42bb38d8ad602358678edbd7 |
| outputs/founderbench-paired-statistics.md | True | 2169 | 7fe7f9a94b1061d41f84344c828578a248c9207cfb2efbcae288c85f3511b686 |
| outputs/founderbench-paired-statistics.json | True | 2706 | 95e88deb315a889c48d3490178fa3cb78689719d58a987e859944bc1d6a3a504 |
| outputs/founderbench-power-analysis.md | True | 3049 | 4df606a39d60dc538ca4ae3e9c77c6e6602120b12dc597795814c598bf26a644 |
| outputs/founderbench-power-analysis.json | True | 3782 | 39642587c0e598e192037ee3deff375e555b2b7d46779c43ea2de729a2650b03 |
| outputs/founderbench-statistical-protocol.md | True | 3516 | 8e46bb2c4b7ea43bd159bdcfc12c356e2f456849ac3abf639e5dfa63308b9af2 |
| outputs/founderbench-statistical-protocol.json | True | 3591 | bdc7422f750759d670c4a814d36514cfb7a03b7f58c02e2c0fbb8ac8ddba8d31 |
| outputs/founderbench-difficulty-calibration.md | True | 5566 | 5af63bf2fef26099f4115ce67a4932817f551acef489ae997846fea201f6f884 |
| outputs/founderbench-difficulty-calibration.json | True | 37652 | a5fa49ca8dcb2e2d4dd924aa67fe9bd0272149a1eb6bcc75fec9e0649fb46760 |
| outputs/founderbench-task-feasibility-audit.md | True | 12196 | d592e87cd82524ede76f3be513a3626dfc428985f3340e31a3390745a1b3d7eb |
| outputs/founderbench-task-feasibility-audit.json | True | 28826 | d01946bc0aff8a466ad48e128648d92ead31f47993c94f3b70838a6b852f426f |
| outputs/founderbench-task-revision-ledger.md | True | 8781 | 0b3297fd84e727861cec3a167878dd30e55ad99f57a6a9ea00c53becc6ffaaa9 |
| outputs/founderbench-task-revision-ledger.json | True | 16203 | eda16e823b10e874b5679423b0b7eb22cfe52cb396eec579c8a8c15361eebd30 |
| outputs/founderbench-determinism-audit.md | True | 1298 | ee4b8bc9a92ce669d97f0369ab712115cfeec9089d9f8ced2ddf8a9d629dc32d |
| outputs/founderbench-determinism-audit.json | True | 2364 | 41291d09fd643a4161d072b3cdbae50471b071e6317d2140a2990a4ba3cd5e88 |
| outputs/founderbench-environment-report.md | True | 2203 | db5598c4becdc8b60f4350a0f06e6eeafecc91cdacf110ee076a79a6f85fc5b0 |
| outputs/founderbench-environment-report.json | True | 18283 | 39545de891d02bf73a73cdc4376568b6d870b7b7ede078e17d33fe8f3a14fc80 |
| outputs/founderbench-simulator-invariant-audit.md | True | 1905 | 9e1c49db8b543b73e67107364c2fead3a4e5805e817c16e8aebaa837636f51dd |
| outputs/founderbench-simulator-invariant-audit.json | True | 8236 | cc42345df5327b16cd8117e03f9294c41bad1b81e86bc35345ecdd99e93e4c35 |
| outputs/founderbench-reviewer-smoke.md | True | 1325 | a227d44925f2e1c8d0f5996dcaaa754240151cd3acc17f5feae449a116980a18 |
| outputs/founderbench-reviewer-smoke.json | True | 1581 | a54006396ec006359901e285aee1e11ee4b9323f12aca7185bbc64582cb5f9a9 |
| outputs/founderbench-random-repeats.md | True | 795 | dc06a41ef8dd83b1930253d6eb9d158fd9091235fb8c883086cf10a4ec01c62a |
| outputs/founderbench-qualitative-traces.md | True | 5229 | 326e987524ee2b5877a4fab14a04e890e9296b8ad6c209518a96c0dd7fbc4eb1 |
| outputs/founderbench-experiment-matrix.md | True | 5249 | 924f78202a45f6b76351a6d1cbb6669805f4f0d6243fdf336822a5f4642eeb99 |
| outputs/founderbench-human-calibration-protocol.md | True | 3803 | 5302fff34764c754063ac2e8569f4db65ac440745adb6e5a7f776831506cc3c3 |
| outputs/founderbench-human-calibration-protocol.json | True | 4335 | 3a70e9d2e17dd777d5ec697f2e6cc67f1ff3a3b491382cd06ccc4b16c8c4d616 |
| outputs/founderbench-human-calibration-schema.md | True | 2016 | eb4d86567c915739eee019391a0ce80febaff56d6e898e3224ee3a8d1a29b5ec |
| outputs/founderbench-human-calibration-schema.json | True | 2118 | 790a413db00631b415107e57142712a79340563be79993965ab2da9ccfc32e5c |
| outputs/founderbench-human-calibration-template.json | True | 6895 | 2a49e73a5fb67eef4b683a77e482938cb86777efe7ad290001441b893c8a5023 |
| outputs/founderbench-human-calibration-analysis.md | True | 988 | 3c6f2ec7edc1cc090f9bb21464ca7dfbaf503ad0c5d8581a7e41b64c85405f44 |
| outputs/founderbench-human-calibration-analysis.json | True | 884 | be7a0e15a1704629e33adc43b22063d67cf7d50f90be3307420e3d52d22f605e |
| outputs/founderbench-human-calibration-packet.md | True | 4908 | 55166b5cf79652180929da47bf44d96105f9ce5e330752f9e66a8a26d06b8bd2 |
| outputs/founderbench-human-calibration-packet.json | True | 5426 | 4147da5795bbaac281939f6d0ef419b1ce730f9dd9a26eba287812693c7fe78e |
| outputs/founderbench-private-holdout-smoke.md | True | 1334 | 70cccafccdb0f764ba5010dd450794d0e789c126ae60dbc394d99b6e9dde10fb |
| outputs/founderbench-private-holdout-smoke.json | True | 1779 | e75d90570c7ea3c59417903f44d0791e6eb2cadc34f9b3410e9e222014c773fa |
| outputs/founderbench-model-submission-schema.md | True | 1516 | e2b422c7d307b7deb90c9e9b1c4bb1b44ffdf1b2364c3eaf347d651a55fd024f |
| outputs/founderbench-model-submission-schema.json | True | 20298 | 9a2e120e44df432ba418e04143631a8d6bf6f9d16d3bc1010725c13e49ad4dd0 |
| outputs/founderbench-submission-bundle-protocol.md | True | 1529 | ae10be4c4dbe4d4370bc5490bbd4838b8ebb630b6294a8c60b074fa27880031d |
| outputs/founderbench-submission-bundle-protocol.json | True | 1685 | 8d243af8cb374ca0e8bdfc953ff56d8964f10d9ab5753140ef9d1558517415b3 |
| outputs/founderbench-prompt-protocol.md | True | 5202 | bcce485c9516a28432493c19e7c0c14dc94bb9674395f5d76555419f18b86721 |
| outputs/founderbench-prompt-protocol.json | True | 7130 | ab4bfbc060c3888910d0c0dc6a5ff501e49c253990fdf2d16ebcfe54f610db07 |
| outputs/founderbench-release-metadata-checklist.md | True | 3591 | a85aaa07a9bfb8b4e690d742758583e00c4c129cf2676298a61297a34a0c4df9 |
| outputs/founderbench-release-metadata-checklist.json | True | 4688 | a1071327fee72e92bfb6a5733a9cb60a24fd42749d088884f2aaa4b027b53e61 |
| outputs/founderbench-cost-accounting.md | True | 2408 | cc38c163143b187b521b02b0c665f7574dc401138e409f5f8a8339a382e3158b |
| outputs/founderbench-cost-accounting.json | True | 2530 | 6ab1b03b528830e7abe68bf6798fc1160d68647a486e0fb5f270210cb839b8f5 |
| outputs/founderbench-submission-action-plan.md | True | 16587 | db1a7cc198f47f1621f6a5af0fe284d193cde03f70ce311b414cef937345ec87 |
| outputs/founderbench-submission-action-plan.json | True | 22067 | 13cd18b1807fcd4f39dc25aacbca5f866d2e4228b6d1abf3ddba23abcd25e740 |
| outputs/founderbench-completion-audit.md | True | 8186 | 8df7acbe0b245983c11c031c74543c3b901edb4107d16d5dae0e1d8f821ad371 |
| outputs/founderbench-completion-audit.json | True | 15327 | e79b4a29d3b728a087e99ff3adca7c2815a70d09deeea1c1083e4afc71ba1571 |
| outputs/founderbench-submission-manifest.md | True | 5856 | b6e76438326ae4064e56bd37549d903b12635177e55eeb9663aba5dbde78e05b |
| outputs/founderbench-submission-manifest.json | True | 9530 | d6a360d24a61e5abec3340d3c7ef8f4066aea2b26639d749561b8336cd8da244 |
| outputs/founderbench-reviewer-risk-audit.md | True | 9851 | 45d45caf5c78e9ca462be15643aaa90bb2ea51e4e97b9add254ea194e0d70b90 |
| outputs/founderbench-reviewer-risk-audit.json | True | 13320 | 23b7861b8632016982f90d697e84d0bb870f68d4a7c2ceb20d55b46a759ef3a5 |
| outputs/founderbench-responsible-use.md | True | 4057 | 46ed917985660e174c472a876b2c5eb3766a12dfb8e0b134efaa90efb6de2df9 |
| outputs/founderbench-responsible-use.json | True | 4471 | f57ec74b118ce6bc6ca8269a9f412376770ee213a8ab5bad98ce3e344514c648 |
| outputs/founderbench-failure-mode-audit.md | True | 8556 | f099c21a47a4d31342fda00dd827129b286174491cd8fdfec01fd3bb19efb1d3 |
| outputs/founderbench-failure-mode-audit.json | True | 11463 | 02975473330bdab9f300c77fbdf1e6e703787cada481c0938472a946ecd91d45 |
| outputs/founderbench-baseline-execution-plan.md | True | 17282 | 4bf1f6f99432b067c0292ab545a64c73fdf0060a2d0eb0f10eca6c8815823a41 |
| outputs/founderbench-baseline-execution-plan.json | True | 27956 | ce0e59e6d1861c438865f9077403bdc5304842ab270a516738d6cc497121e4bc |
| outputs/founderbench-experiment-runbook.md | True | 24376 | d8b0fb499cf7bc9379355906f79b8b0d008522b4b73eb477c57fccaf57addef6 |
| outputs/founderbench-experiment-runbook.json | True | 28944 | 504a8e8f5bc5797441ce5d94cb202896bf179e1a96ef02cd3753568f0a2ccbfa |
| outputs/founderbench-provider-run-status.md | True | 5434 | af8bb990d879fc13fb0a53628b59edc54758b77ff883608da3ea053dafc59167 |
| outputs/founderbench-provider-run-status.json | True | 16984 | 69ec990f8352d5074d8a357f4659a0964a5303a75d983c63017f7ed30696ef38 |
| outputs/founderbench-provider-comparability-audit.md | True | 3847 | 377f68db52d8f4b1c54350486c7e93401dddc2a673f681c40fcb6afb163ad9e8 |
| outputs/founderbench-provider-comparability-audit.json | True | 9594 | 4237a012e1e7882d389b5b47214f7ff07bd58ffa24555eeba3c5fd58d6621351 |
| outputs/founderbench-provider-contract-audit.md | True | 2167 | 08f62db81f7fd6671226379e7656946f28e0f58ec68ff15189e6d0d5ea93fae5 |
| outputs/founderbench-provider-contract-audit.json | True | 3003 | e83abd31ea34cb5bc68157aacb0b0de344c8b2c2569188d83f000e0d8387d113 |
| outputs/founderbench-contamination-leakage-audit.md | True | 4287 | 4c251a311a3d2c6ac61b3b296ec57ce2d57ae6697e49a6ea90c062b310f0235a |
| outputs/founderbench-contamination-leakage-audit.json | True | 5009 | 939e1dfbd7eca71759a1850814deed82815da11efd8db9015cb39f9def63bac7 |

## Validation

Status: PASS

All listed core source and output files are present, and no secret values are recorded.
