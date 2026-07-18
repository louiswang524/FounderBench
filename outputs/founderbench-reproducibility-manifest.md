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
| Git commit | 55c63c6ac76119a0a3e2edef5e233b680d709558 |
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
| work/founderbench/founderbench/baseline_execution_plan.py | True | 16971 | 7eced1be7d4f268e9a537870fc0a5ddc00b3f196291c57ca74d327e25d928ff6 |
| work/founderbench/founderbench/benchmark_datasheet.py | True | 11702 | 9f250c29419a6080458ba8c8f9e76874cecf2ca12e8da365de64d2907d7b95f1 |
| work/founderbench/founderbench/bundle_integrity.py | True | 6118 | 6bd26fbafcd84015b4eecf0ab902a33985f421b1ca2965bac2847bc4a9c55408 |
| work/founderbench/founderbench/citation_audit.py | True | 11027 | df083b1d0d9f1f70676250113d748f8c4e9a6b298ccb9fb3a0c6be7c32f69f5d |
| work/founderbench/founderbench/completion_audit.py | True | 16934 | 7041593517bbb5bed7435ef2e1a50423340d075dbd96b049645d89a9e79f84ec |
| work/founderbench/founderbench/contamination_leakage_audit.py | True | 11061 | 04ecfa9a8e2dd5cc4945a25e0cf78529f2c15a86e1f36b26e9ec075b5a43dd10 |
| work/founderbench/founderbench/cost_accounting.py | True | 8483 | e4c266377447785ff952a44de5277df1c3c99efd5ef78e963365e74919c83f15 |
| work/founderbench/founderbench/determinism_audit.py | True | 6320 | 8dc6a065938e2a8446f8f1a8016337c2cb213c9b9f6859ff651932fd575ccf10 |
| work/founderbench/founderbench/environment_report.py | True | 7384 | 011ae101999f58f7cc76edd33159e1b7bb1097c5a21f6bf4fd841c079cecdd68 |
| work/founderbench/founderbench/env.py | True | 17665 | ba3a31f3f4655d6a7988b8cb30cbea0a4abc4d309250be8aeff4f1ecd72f3fcf |
| work/founderbench/founderbench/experiment_runbook.py | True | 14463 | e0219172c6c12c5cbf7f0d28784f0e839e9e9fae0e24aaf1ea5c7a3a536bc478 |
| work/founderbench/founderbench/failure_mode_audit.py | True | 14748 | 671d3c5f807a0e7977227b41b1a977716ae0d24836be288d550b9ca7df39204c |
| work/founderbench/founderbench/holdout_smoke.py | True | 5696 | 26ae665d5dccd80ad03d8f9fd3b5bb298385bd573ad1575be5d7cd21dbce9524 |
| work/founderbench/founderbench/human_calibration.py | True | 9513 | 4faec0573771743aa8e4cc2b0a5d1ed068d04dcc823373fc1f259c8477a56aff |
| work/founderbench/founderbench/human_calibration_analysis.py | True | 12171 | 3c9de21c3248a3980beb6eba265c9f534f7b787968ceed6ba78d38fce213ceed |
| work/founderbench/founderbench/human_calibration_packet.py | True | 12073 | 27300023239d31874e11caa213bc9d0e2d1d9539e282205cdc8b6085dde6ac84 |
| work/founderbench/founderbench/human_calibration_schema.py | True | 9720 | 70cda560e35391951f3adb2c3cf881c8b2549516b01afd9153e1955b9307b795 |
| work/founderbench/founderbench/leaderboard_policy.py | True | 9225 | 4d2c37945edd2bb8e3930f039534961a59366f102e023263f310f0b7ca36c805 |
| work/founderbench/founderbench/leaderboard_stability.py | True | 10450 | 8867bab6a72299de7a32a755719fa5971ccc65503985eb9fb271ad47ff911dbc |
| work/founderbench/founderbench/market_catalog.py | True | 8477 | a331819eb40a30cbe606206fb46f57aa207a03233b6a19eae98dc95afafb7be3 |
| work/founderbench/founderbench/tasks.py | True | 34135 | 620c586982ae3fe06899a3bb366e89c1d5cde57aec7f518b1156ba2e63ccec95 |
| work/founderbench/founderbench/task_cards.py | True | 7785 | 3c4ebe219310be0d4a66fc7428d6cdaab89f5d390f4aa5243a22cea710096967 |
| work/founderbench/founderbench/task_feasibility_audit.py | True | 10949 | 47a8afa7115ddc8de62d045edb0a90ac298faf662d1410e874c5bed9ae035e20 |
| work/founderbench/founderbench/task_runner.py | True | 9758 | 66177476ad6617392c6d904eb9e2544cadc91455782db057a8e214528a413c35 |
| work/founderbench/founderbench/task_provenance.py | True | 12157 | 5aa249c7c8e9373f23545834133b1f5ac3eafea0a1b8c3ed2e735758ccf0c66f |
| work/founderbench/founderbench/task_revision_ledger.py | True | 10220 | feb20a522e90a8c685f4c82cfb2ace89bdc989afeb2d3b3a5ac7ec1c40dc21c1 |
| work/founderbench/founderbench/policies.py | True | 17055 | a3474fbf6de7c1b5da4d440ff90b1945504bf9a32148d80eea38ce6d9dfda223 |
| work/founderbench/founderbench/difficulty_calibration.py | True | 12235 | c136f65d8600085765bccc579bc42ea4179b68922a21cfb08f9e677a46539253 |
| work/founderbench/founderbench/llm_policy.py | True | 20973 | 648deb86c958563114db70ccf156e4e779b2bf85e2c84312cc6e0b88605a2b3a |
| work/founderbench/founderbench/metric_sensitivity.py | True | 11162 | de915f79dade6336b27a90327871f1e62352cd0d6c5dbe6dc2386fde0ce3ef9e |
| work/founderbench/founderbench/model_comparison.py | True | 9212 | cfa33c2716e58daafe039f849486f26e4802efb1e2c57521d901e0d16e3e11dd |
| work/founderbench/founderbench/model_result_cards.py | True | 11102 | 02608a7c5df3c7924db2ee6f1f99924399c06c2f49ba11e8a1a8df91663e90ed |
| work/founderbench/founderbench/paper_claim_lint.py | True | 8991 | 8ae9619d0409386b9449a50b17bc99d88681569e0bc280e7cfb409d2588cda66 |
| work/founderbench/founderbench/paper_evidence_map.py | True | 13775 | 7a83027ecfe7f96fcca5876ebd6208eb5fc2f04747d113ac037d3cd4232106d3 |
| work/founderbench/founderbench/paper_figures.py | True | 8902 | 8b5d23f91c3c9e67f58a2d8686a00e1e566c751d39f44575442560e92e8e9c30 |
| work/founderbench/founderbench/paired_statistics.py | True | 11014 | 3dbe752b2b3f521523e88654b253490ff80a87fa6140573fa52202739fc7a25f |
| work/founderbench/founderbench/power_analysis.py | True | 9117 | 3aad5932c9356034949573ceac58529496cc96bb63d40063eb9c2d39fc57cbef |
| work/founderbench/founderbench/prompt_protocol.py | True | 8347 | 6ee0a4e042118fce724b6d8e0ec0923db56f1c03b34dc2fd404fc0108786da02 |
| work/founderbench/founderbench/private_holdout_evaluator.py | True | 7766 | 24a1c1579cd8d992545031140ef3352945afa3377f3e15d7fbbc4c63384f3f5b |
| work/founderbench/founderbench/provider_comparability_audit.py | True | 11200 | d31ec618a796ecad76cd2e0a523c13765a960d9aaad60065d224bad474302a8d |
| work/founderbench/founderbench/provider_contract_audit.py | True | 9134 | d3450247b5bee0c79a12bd9265666bf138e8c3bd6d2843575316cf19fda18de0 |
| work/founderbench/founderbench/provider_run_status.py | True | 11070 | 495dc70ba9c70e7e66b2c830a4bc4f301dccf7a725509fc4ae8f3cd784997d94 |
| work/founderbench/founderbench/release_metadata.py | True | 7649 | 53981e59728c5a20e3ba428609c2df07cb94b3bb3b52758ed635ca988d12dc69 |
| work/founderbench/founderbench/responsible_use.py | True | 9449 | 9528c90ae9b3ffaa9e4d0708a4f7e2d1bd0ea6ccef26b5f0527a5f4194319b33 |
| work/founderbench/founderbench/result_integrity_audit.py | True | 10087 | f124e7af05e8d03f75ba6cb28a3b8a2b9a34ab0aeed09079bdb9da66ae689912 |
| work/founderbench/founderbench/reviewer_risk_audit.py | True | 16237 | 19b688040a0e795aa640274b861eb0ecebd13e35c3646991c26179e0969adf2f |
| work/founderbench/founderbench/reviewer_smoke.py | True | 5965 | 28a558a1f7e34de455a08ff0129a3e9f7158412f9f464db43c6ea07e9e02a43a |
| work/founderbench/founderbench/simulator_invariant_audit.py | True | 12749 | f520fc2d1fd4024c18df132306fc0f32be5f79f86b00a177e3e8523f1ceba4a1 |
| work/founderbench/founderbench/scoring_consistency_audit.py | True | 11197 | f0ee2f307355f845bdc4a40b83f6a098992a491aefe9fcf06827dfc33b37d507 |
| work/founderbench/founderbench/statistical_protocol.py | True | 8794 | 51b1294b70223b6f4751d48bc8aae5824263af8e30fd29262b6e9aaeeaf802f3 |
| work/founderbench/founderbench/submission.py | True | 8913 | db3c30122c5b906fb57062af409b2e8e80f3bc2d30168c7166f94af9d1e145f6 |
| work/founderbench/founderbench/submission_action_plan.py | True | 9838 | 8ad83f33fa091a708a5a5a863ae5892e480f92857ab3ead4b70c1c7ec8810e3c |
| work/founderbench/founderbench/submission_bundle.py | True | 8809 | 8d44dab7e566026c9bceed78917c2be513c02d377df8ceaf8f11a97da72ac897 |
| work/founderbench/founderbench/submission_manifest.py | True | 10876 | 10ea0f8dc898234fad855a100b1ea43ab14aeea874e9d9658bd158c736464a37 |
| work/founderbench/founderbench/submission_schema.py | True | 9386 | 7b6c6c352a7ffe338594d51354554b18ad9f86adb2eacc6b0fe832fc681cf4fe |
| work/founderbench/founderbench/release.py | True | 30881 | b7cf6205e236017a273074dbde41fb42044b2a548cdf7ec707819abcb41b711f |
| work/founderbench/founderbench/resumable_runner.py | True | 4750 | 3f061139fe9c550345488586106c576fcafad6e6da291457beef93507db914e5 |
| work/founderbench/tests/test_founderbench.py | True | 69401 | 6a7746edb26433c1aa494e4e234ec449b141b4d4fbc316f34c8ec6da811d1e04 |
| work/founderbench/README.md | True | 20771 | 84804177a87b199bd7533bc671c4754ba5da3ef8f39434bc205ac88193eb1c08 |
| work/founderbench/SPEC.md | True | 9639 | c26af0b2a378b2b854b726114d27bb65d0e59d799d4d3865d22d70d2b3424410 |
| work/founderbench/CITATION.cff | True | 554 | c89452bacf9e1273d9c4cb2fef691b1f6e95af6e9b96e3c316dcec398c44582c |
| work/founderbench/CITATION.cff.template | True | 582 | 0f537b4c02dece317c61dcb1ea1a49470049450e45eae7ffac1ae5958e2f452d |
| work/founderbench/LICENSE-TODO.md | True | 361 | c14a53909dd6844c3eb87cf091891b87354ab7f269178acd2a4b7ad46f66a718 |
| work/founderbench/LICENSE.template | True | 466 | 07f71722a4e11a880dcd2ca24d74e75e35d6b9099f3e242257e5140f20cb3d25 |

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
| outputs/founderbench-baseline-raw.json | True | 342129 | 47494e318c4134e055d116de87e196faff0da7fc7275eff20107826b91b4f72c |
| outputs/founderbench-baseline-leaderboard.json | True | 2653 | 26aefe1109d7ff5ab0874a1019ee9f5e8e962482b0063184cfc08b9838ddb854 |
| outputs/founderbench-leaderboard-policy.md | True | 3516 | ed8ff2dafcb7e5d96248b6bf6612f90602bbb23e2ee9a009b0f258056612e007 |
| outputs/founderbench-leaderboard-policy.json | True | 4256 | 14b99d8ce6f9b5a7cadbd0a5e11297dfc264e6a85bfe6e4eea40f2698bb23fe6 |
| outputs/founderbench-leaderboard-stability.md | True | 3181 | dc9a94adb6cd36d440c85720757fff8ea8a174a97f0c697d6b124db16b081f7a |
| outputs/founderbench-leaderboard-stability.json | True | 7593 | 401cd7098887e5618e693e57bbfbd9333a155a00e2d74d5703e3c1cb7dcc3b76 |
| outputs/founderbench-baseline-analysis.md | True | 4380 | ac32eeb85d6ef3d99ce300f6acf81fd66a4007120f22665864795512166045ae |
| outputs/founderbench-result-integrity-audit.md | True | 1582 | 5775845487070b74036712353911ec7f97efeb221601cc7afedd262fa818830c |
| outputs/founderbench-result-integrity-audit.json | True | 2081 | 5555e71699734b2144f4f45320332a224b1c5ce573e65dcfabc56ba6bc668d36 |
| outputs/founderbench-paper-tables.md | True | 5625 | 1d9d663b0cb630a9ef0dd7ea26b2e0664bee813ccd079a12e919021f8b0c92ae |
| outputs/founderbench-paper-figure-data.md | True | 1628 | 045386e39beec6bb40748ee699f81bdd780713ea7ce7d181f17cb722396fd130 |
| outputs/founderbench-paper-figure-data.json | True | 15206 | 315f479ff4babf5b4ba8e69977615ee9a5748fac84f090944419331ce5985fc0 |
| outputs/founderbench-paper-evidence-map.md | True | 8114 | 3b68f9a27005b150c26bd69d1a823ebeab26235e8e963fc454589168699403f0 |
| outputs/founderbench-paper-evidence-map.json | True | 17081 | 35148d48c611dfdea89e34ad28e3b6addfe78140103dfaa841f536512e7ac083 |
| outputs/founderbench-paper-claim-lint.md | True | 1530 | fda867ae783089d7b24915233e013da0e1093a814bc9164a9cd33e772ae6ec43 |
| outputs/founderbench-paper-claim-lint.json | True | 1880 | d76476b488e2c8f2ceb2f1bd3338e89cc815e992057d56802127fe34c0f2be3c |
| outputs/founderbench-citation-audit.md | True | 2651 | 46ab5552ddf6460b39f618f456334f09fdb7d233d437cc65c0a27889ce3b56f8 |
| outputs/founderbench-citation-audit.json | True | 8482 | 4fc888f481fcc2c0ed889f4c16c3ed79bbad8d57d96f843a10def84d200d5b64 |
| outputs/founderbench-model-comparison.md | True | 5638 | 27a48607f4bb20c4bcf47f9f44fa166081f5fe255786006562d2cb521a40d8da |
| outputs/founderbench-model-comparison.json | True | 15007 | 97b8a3c6d095a6bd9a7e62883e260a985606b0954d3022d605757611e2fb9bb2 |
| outputs/founderbench-model-result-cards.md | True | 4442 | 67fabd55538b83418c57cb9e35b7db3405614ae436c3d45c9a47efd105c35322 |
| outputs/founderbench-model-result-cards.json | True | 12832 | 56dfc316126d35a4be1fada3ce4d01730fd2f65d68287b668f76b7bf3f301e25 |
| outputs/founderbench-ablation-report.md | True | 2444 | 7ca23db2ffa0ac21a917349eac06a9297147f28afb3cecd7d9ee008205c47fb2 |
| outputs/founderbench-action-ablation.md | True | 2372 | f0439186b7f1ba3d7ef0fac8f6617ad03484ca54db16044bc58d212d3b9f45af |
| outputs/founderbench-action-ablation.json | True | 643481 | b34601a8f91528cde4cd89d3d7b8db69c3e4f733b8b25093ad52437faba77657 |
| outputs/founderbench-paired-statistics.md | True | 2169 | 7fe7f9a94b1061d41f84344c828578a248c9207cfb2efbcae288c85f3511b686 |
| outputs/founderbench-paired-statistics.json | True | 2706 | 95e88deb315a889c48d3490178fa3cb78689719d58a987e859944bc1d6a3a504 |
| outputs/founderbench-power-analysis.md | True | 3049 | 4df606a39d60dc538ca4ae3e9c77c6e6602120b12dc597795814c598bf26a644 |
| outputs/founderbench-power-analysis.json | True | 3782 | 39642587c0e598e192037ee3deff375e555b2b7d46779c43ea2de729a2650b03 |
| outputs/founderbench-statistical-protocol.md | True | 3578 | 9b15ebead486d8885fa9c485cce4c64fe1192bef490200ea90e9edd982e2bb36 |
| outputs/founderbench-statistical-protocol.json | True | 3653 | 0167f7c32c6584f277d6fbce6632d8aae6a87ea7d32bee0e4b01957a68cf1700 |
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
| outputs/founderbench-experiment-matrix.md | True | 5418 | 50b45c7cb7d87ea7c046eefa0f8c5470e499a170008dc6de40501760ca7f44cc |
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
| outputs/founderbench-private-holdout-smoke.json | True | 1782 | 48d1ce8ffdb28fcddfaa44eba4605c413d93827345bfccf0510f4763e5abf4b1 |
| outputs/founderbench-model-submission-schema.md | True | 1516 | e2b422c7d307b7deb90c9e9b1c4bb1b44ffdf1b2364c3eaf347d651a55fd024f |
| outputs/founderbench-model-submission-schema.json | True | 20298 | 9a2e120e44df432ba418e04143631a8d6bf6f9d16d3bc1010725c13e49ad4dd0 |
| outputs/founderbench-submission-bundle-protocol.md | True | 1529 | ae10be4c4dbe4d4370bc5490bbd4838b8ebb630b6294a8c60b074fa27880031d |
| outputs/founderbench-submission-bundle-protocol.json | True | 1685 | 8d243af8cb374ca0e8bdfc953ff56d8964f10d9ab5753140ef9d1558517415b3 |
| outputs/founderbench-prompt-protocol.md | True | 5417 | cfbefee0f0357f6b19e8ae5b32fdaccfd54fbab6e9e0f0319766d942c4ff7738 |
| outputs/founderbench-prompt-protocol.json | True | 7838 | ef85bd2194f28326b2763f17f4dde533bf9f2643272adc01ef0a5abf76f56048 |
| outputs/founderbench-release-metadata-checklist.md | True | 3591 | a85aaa07a9bfb8b4e690d742758583e00c4c129cf2676298a61297a34a0c4df9 |
| outputs/founderbench-release-metadata-checklist.json | True | 4688 | a1071327fee72e92bfb6a5733a9cb60a24fd42749d088884f2aaa4b027b53e61 |
| outputs/founderbench-cost-accounting.md | True | 2408 | cc38c163143b187b521b02b0c665f7574dc401138e409f5f8a8339a382e3158b |
| outputs/founderbench-cost-accounting.json | True | 2530 | 6ab1b03b528830e7abe68bf6798fc1160d68647a486e0fb5f270210cb839b8f5 |
| outputs/founderbench-submission-action-plan.md | True | 18184 | 43c29d7a28ac57d7490fe406d57be044ceaf8907ebe3a8f0fcad14b01424d1b6 |
| outputs/founderbench-submission-action-plan.json | True | 24004 | d84d2c55bf7a8f1d276a9e5c0add6ef675a00716750aaa7eeb70a7a60bbc7317 |
| outputs/founderbench-completion-audit.md | True | 8186 | b3278e061f5014cff61f0f0ae3a517bb5d183fb563110e32a0c2d21e3a416e8b |
| outputs/founderbench-completion-audit.json | True | 15327 | d2548bd990b8c70b72a4dd24a8c42ce4554435bc40cd5a71195ebe3fbccb602a |
| outputs/founderbench-submission-manifest.md | True | 5856 | 0fffd906ada5d38eb239d4dbfa68896999ba9f3a34d31d9adbb51f958a584574 |
| outputs/founderbench-submission-manifest.json | True | 9530 | 0a06b071bbc9305169ab2330060f28a0ff08ec9c0af8343a635b9a1b3f6956b7 |
| outputs/founderbench-reviewer-risk-audit.md | True | 9851 | 45d45caf5c78e9ca462be15643aaa90bb2ea51e4e97b9add254ea194e0d70b90 |
| outputs/founderbench-reviewer-risk-audit.json | True | 13320 | fc4e179c61bfb755698ad0a339139d47d1a102445e13fbc4e873b307e2ae1ddc |
| outputs/founderbench-responsible-use.md | True | 4094 | d4d97a03a5f262f77857b2080e62283d0af9f80e0d0177dcc48bb13b72a553be |
| outputs/founderbench-responsible-use.json | True | 4508 | 251eebc2d69a4287b0ce75c7d28f4f1fddfcf503a7f44c0552ab506066338a1e |
| outputs/founderbench-failure-mode-audit.md | True | 8556 | f099c21a47a4d31342fda00dd827129b286174491cd8fdfec01fd3bb19efb1d3 |
| outputs/founderbench-failure-mode-audit.json | True | 11463 | d060226a66cdcc48519d6c9990c0ca82e6abfe5993cd042e2bfaff298fff893f |
| outputs/founderbench-baseline-execution-plan.md | True | 18804 | 53f2243a40c5bef1623e7188f4798cb54d104b028e6afa86799037ff57b1ca28 |
| outputs/founderbench-baseline-execution-plan.json | True | 30474 | 7c3a4194cf1ed30d0ec791efacdd9ee3458c965c12f2579290cca73962eef750 |
| outputs/founderbench-experiment-runbook.md | True | 26306 | 73b635c75479a8b0846d19d108dc9365c43ea3d39d22ecd6aec1cd3c83c523a1 |
| outputs/founderbench-experiment-runbook.json | True | 31206 | 034f22575d961aa5a48ca7280b97171fc758c79cf0194bb4c4286b551c406e8b |
| outputs/founderbench-provider-run-status.md | True | 5626 | 08e609ce192f0abc3cac731627a67ae5022e5026375ae90dad20290e5e2dfdfb |
| outputs/founderbench-provider-run-status.json | True | 18244 | 0dd3347c5ac88c6d593854983a889b539c8b8652e989dd4739057227fbfb378b |
| outputs/founderbench-provider-comparability-audit.md | True | 4317 | df63651b77decacd178cf22e656ad8b5e5a6b2e226c111c026f6883fcea84e0b |
| outputs/founderbench-provider-comparability-audit.json | True | 10947 | 81d51ac436838b35a02b509cf505adfce4c5dc4bc2038b94c3de4e136debb2b3 |
| outputs/founderbench-provider-contract-audit.md | True | 2167 | 08f62db81f7fd6671226379e7656946f28e0f58ec68ff15189e6d0d5ea93fae5 |
| outputs/founderbench-provider-contract-audit.json | True | 3003 | e83abd31ea34cb5bc68157aacb0b0de344c8b2c2569188d83f000e0d8387d113 |
| outputs/founderbench-contamination-leakage-audit.md | True | 4315 | 3aca44ef8e48a38d86b30ef560d52daf180223ce55a16c09b58fcc310a3ddb31 |
| outputs/founderbench-contamination-leakage-audit.json | True | 5037 | f1bfe67f4de333c1a0d8001d5fba6ef0df17beb35b833bba9b1de3262be488de |

## Validation

Status: PASS

All listed core source and output files are present, and no secret values are recorded.
