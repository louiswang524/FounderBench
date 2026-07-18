# FounderBench Reproducibility Manifest

This generated manifest records the source/output hashes and reproduction commands for the current workspace. It records only secret variable names, never secret values.

## Environment

| Field | Value |
| --- | --- |
| Python | 3.12.10 |
| Python executable | C:\Users\louis\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\python.exe |
| Platform | Windows-11-10.0.26200-SP0 |
| Machine | AMD64 |
| Working directory | C:\Users\louis\Documents\Codex\2026-07-14\use\work\moneybench |
| Git commit | af888c3b7791de3678c6f03a18bc0c86e8477ff4 |
| Secret values recorded | False |

## Commands

| Purpose | Working Directory | Command |
| --- | --- | --- |
| Regenerate all generated current release artifacts | work/moneybench | `python -m moneybench.release regenerate` |
| Run tests and validate required outputs | work/moneybench | `python -m moneybench.release validate` |
| Build supplementary release bundle | work/moneybench | `python -m moneybench.release bundle` |

## Core Source Files

| Path | Exists | Bytes | SHA-256 |
| --- | --- | --- | --- |
| work/moneybench/moneybench/action_ablation.py | True | 11627 | 54c3d06edc79d45c67a6ca7311d9e3bd65b3d902abacb731530e08cb0dac68d1 |
| work/moneybench/moneybench/action_semantics.py | True | 12872 | 666c494e8916fb4fe65dfdd145012b8b4c64edd7e9e1086a3d869c94427fdb68 |
| work/moneybench/moneybench/baseline_execution_plan.py | True | 16955 | df105e2eec9730be7d329520d1dc97d0bacecf99d3ae9434128e8ef355aae3fd |
| work/moneybench/moneybench/benchmark_datasheet.py | True | 11702 | 9f250c29419a6080458ba8c8f9e76874cecf2ca12e8da365de64d2907d7b95f1 |
| work/moneybench/moneybench/bundle_integrity.py | True | 6118 | 6bd26fbafcd84015b4eecf0ab902a33985f421b1ca2965bac2847bc4a9c55408 |
| work/moneybench/moneybench/citation_audit.py | True | 11027 | df083b1d0d9f1f70676250113d748f8c4e9a6b298ccb9fb3a0c6be7c32f69f5d |
| work/moneybench/moneybench/completion_audit.py | True | 16918 | 20298389359af1185289608788d2baa511b563b8d79738b17ca3bad1b99ae247 |
| work/moneybench/moneybench/contamination_leakage_audit.py | True | 11061 | 04ecfa9a8e2dd5cc4945a25e0cf78529f2c15a86e1f36b26e9ec075b5a43dd10 |
| work/moneybench/moneybench/cost_accounting.py | True | 8483 | e4c266377447785ff952a44de5277df1c3c99efd5ef78e963365e74919c83f15 |
| work/moneybench/moneybench/determinism_audit.py | True | 6320 | 8dc6a065938e2a8446f8f1a8016337c2cb213c9b9f6859ff651932fd575ccf10 |
| work/moneybench/moneybench/environment_report.py | True | 7366 | da7d93f842025b938eb75e485ec9620fc9621260faad3e86b85e710dd63da2ea |
| work/moneybench/moneybench/env.py | True | 17663 | fc60baf74776cbe02503554b759ee85793bbb541fa6c733d402a0bd3d975b320 |
| work/moneybench/moneybench/experiment_runbook.py | True | 14453 | 892469ae044082415f814265a59fc291b65f37da581e9093b030a8c0324bac93 |
| work/moneybench/moneybench/failure_mode_audit.py | True | 14742 | 5a99b4fe447f88e794ccb1c93d8fce03115be68af80bf3682489981cd8a68446 |
| work/moneybench/moneybench/holdout_smoke.py | True | 5696 | 26ae665d5dccd80ad03d8f9fd3b5bb298385bd573ad1575be5d7cd21dbce9524 |
| work/moneybench/moneybench/human_calibration.py | True | 9513 | 4faec0573771743aa8e4cc2b0a5d1ed068d04dcc823373fc1f259c8477a56aff |
| work/moneybench/moneybench/human_calibration_analysis.py | True | 12171 | 3c9de21c3248a3980beb6eba265c9f534f7b787968ceed6ba78d38fce213ceed |
| work/moneybench/moneybench/human_calibration_packet.py | True | 12069 | faf2bb570a41b4115a44c78e7ed329b2f316af52d4e9e66c686e396163a4dd18 |
| work/moneybench/moneybench/human_calibration_schema.py | True | 9720 | 70cda560e35391951f3adb2c3cf881c8b2549516b01afd9153e1955b9307b795 |
| work/moneybench/moneybench/leaderboard_policy.py | True | 9223 | e192e49d8c34efb3121e0f91f2dbed54e482d0bc422cdef0dede21e074505821 |
| work/moneybench/moneybench/leaderboard_stability.py | True | 10450 | 8867bab6a72299de7a32a755719fa5971ccc65503985eb9fb271ad47ff911dbc |
| work/moneybench/moneybench/market_catalog.py | True | 8477 | a331819eb40a30cbe606206fb46f57aa207a03233b6a19eae98dc95afafb7be3 |
| work/moneybench/moneybench/tasks.py | True | 34061 | 352f0461a2252567319f33662da4a85cf8ac3e55628d55e8fdbe0cac1688c9d3 |
| work/moneybench/moneybench/task_cards.py | True | 7781 | dd375e05aaea0d95bfa8c0c6b6df6bf4551562d7fa07b2a237eb43c20f728533 |
| work/moneybench/moneybench/task_feasibility_audit.py | True | 10949 | 47a8afa7115ddc8de62d045edb0a90ac298faf662d1410e874c5bed9ae035e20 |
| work/moneybench/moneybench/task_runner.py | True | 9754 | d3a8b999b302c02ba607125cc9ddd59595ee2ba3ff8881ff54bb9a7337071aa5 |
| work/moneybench/moneybench/task_provenance.py | True | 12153 | 9668ef0e32a99600d9744c4d77cd2fb09a6f0dc5ec2e6ad3ebc5719a4b9949ee |
| work/moneybench/moneybench/task_revision_ledger.py | True | 10220 | feb20a522e90a8c685f4c82cfb2ace89bdc989afeb2d3b3a5ac7ec1c40dc21c1 |
| work/moneybench/moneybench/policies.py | True | 17055 | a3474fbf6de7c1b5da4d440ff90b1945504bf9a32148d80eea38ce6d9dfda223 |
| work/moneybench/moneybench/difficulty_calibration.py | True | 12235 | c136f65d8600085765bccc579bc42ea4179b68922a21cfb08f9e677a46539253 |
| work/moneybench/moneybench/llm_policy.py | True | 20973 | 648deb86c958563114db70ccf156e4e779b2bf85e2c84312cc6e0b88605a2b3a |
| work/moneybench/moneybench/metric_sensitivity.py | True | 11162 | de915f79dade6336b27a90327871f1e62352cd0d6c5dbe6dc2386fde0ce3ef9e |
| work/moneybench/moneybench/model_comparison.py | True | 9212 | cfa33c2716e58daafe039f849486f26e4802efb1e2c57521d901e0d16e3e11dd |
| work/moneybench/moneybench/model_result_cards.py | True | 11102 | 02608a7c5df3c7924db2ee6f1f99924399c06c2f49ba11e8a1a8df91663e90ed |
| work/moneybench/moneybench/paper_claim_lint.py | True | 8991 | 8ae9619d0409386b9449a50b17bc99d88681569e0bc280e7cfb409d2588cda66 |
| work/moneybench/moneybench/paper_evidence_map.py | True | 13773 | 13dcc4abf2aa107e1ebd3d39829ffb00fe382afe06ce868a4e18be4170b0cf5e |
| work/moneybench/moneybench/paper_figures.py | True | 8902 | 8b5d23f91c3c9e67f58a2d8686a00e1e566c751d39f44575442560e92e8e9c30 |
| work/moneybench/moneybench/paired_statistics.py | True | 11014 | 3dbe752b2b3f521523e88654b253490ff80a87fa6140573fa52202739fc7a25f |
| work/moneybench/moneybench/power_analysis.py | True | 9117 | 3aad5932c9356034949573ceac58529496cc96bb63d40063eb9c2d39fc57cbef |
| work/moneybench/moneybench/prompt_protocol.py | True | 8341 | 5937978a9def514d8b0d616f101438a8a6b924e36d0369fee6387a2b5d7d40c8 |
| work/moneybench/moneybench/private_holdout_evaluator.py | True | 7766 | 24a1c1579cd8d992545031140ef3352945afa3377f3e15d7fbbc4c63384f3f5b |
| work/moneybench/moneybench/provider_comparability_audit.py | True | 11196 | 59c0ddf60d88c9c06a5bb1461052520bb07b22470a8fc34a6300349f2cdae5f2 |
| work/moneybench/moneybench/provider_contract_audit.py | True | 9132 | 99a2aff79e464a4492a84fd987e0f371a68160f7a7c3434b42890cf58504a294 |
| work/moneybench/moneybench/provider_run_status.py | True | 11070 | 495dc70ba9c70e7e66b2c830a4bc4f301dccf7a725509fc4ae8f3cd784997d94 |
| work/moneybench/moneybench/release_metadata.py | True | 7635 | 684146d4fe3c23177e60267f96a0ae8f7999f400f1245e81eb75f0148a1729bd |
| work/moneybench/moneybench/responsible_use.py | True | 9449 | 9528c90ae9b3ffaa9e4d0708a4f7e2d1bd0ea6ccef26b5f0527a5f4194319b33 |
| work/moneybench/moneybench/result_integrity_audit.py | True | 10087 | f124e7af05e8d03f75ba6cb28a3b8a2b9a34ab0aeed09079bdb9da66ae689912 |
| work/moneybench/moneybench/reviewer_risk_audit.py | True | 16233 | 74de905be5f174cac994990afe075599257dfae079c489c26c6a880b97c1c929 |
| work/moneybench/moneybench/reviewer_smoke.py | True | 5955 | 69bee98e4be09c3546d470cc68e79f5de694e72a9b42ecd420536f580252b562 |
| work/moneybench/moneybench/simulator_invariant_audit.py | True | 12743 | de60c0b0291148b51f9e62cfc3c7891925ab1258c3d238dfe0528d923f2e4c49 |
| work/moneybench/moneybench/scoring_consistency_audit.py | True | 11197 | f0ee2f307355f845bdc4a40b83f6a098992a491aefe9fcf06827dfc33b37d507 |
| work/moneybench/moneybench/statistical_protocol.py | True | 8794 | 51b1294b70223b6f4751d48bc8aae5824263af8e30fd29262b6e9aaeeaf802f3 |
| work/moneybench/moneybench/submission.py | True | 8913 | db3c30122c5b906fb57062af409b2e8e80f3bc2d30168c7166f94af9d1e145f6 |
| work/moneybench/moneybench/submission_action_plan.py | True | 9834 | 4fa80bcfe91fbdb8cb35f3fc6825ac9eb16d1b806db24dc5ebcbf26054352d49 |
| work/moneybench/moneybench/submission_bundle.py | True | 8799 | 8859396e953b108d3526288a0925b648a390789409dfdbc917fc47ba5026359f |
| work/moneybench/moneybench/submission_manifest.py | True | 10864 | 79869aff9a070f2e247978e15feb870c60795a541f4814a6e3d9fae14657a918 |
| work/moneybench/moneybench/submission_schema.py | True | 9382 | 06aad592d10788e790da9b59dd29fbf51d0103d82e26460d5ce0ce8e4de3c00d |
| work/moneybench/moneybench/release.py | True | 30875 | ec573cb9453d1aa027d0ef1c6d4df783521b356cdf61675c7a3c0598504a3d45 |
| work/moneybench/moneybench/resumable_runner.py | True | 4750 | 3f061139fe9c550345488586106c576fcafad6e6da291457beef93507db914e5 |
| work/moneybench/tests/test_moneybench.py | True | 69223 | 8e16f84660a0053508573e65b18e6b81ff20db7907b2bc1bfebf11ded157f66f |
| work/moneybench/README.md | True | 20647 | f83dc5011ddd82a1573f9624b72690ad28bd0c5bb6f877dc6e3596ba554f2aac |
| work/moneybench/SPEC.md | True | 9629 | 0236f89c81a33c55d8f369f93ebea444607db4ece6b31607e404b2c47ef77fd0 |
| work/moneybench/CITATION.cff | True | 554 | c89452bacf9e1273d9c4cb2fef691b1f6e95af6e9b96e3c316dcec398c44582c |
| work/moneybench/CITATION.cff.template | True | 582 | 0f537b4c02dece317c61dcb1ea1a49470049450e45eae7ffac1ae5958e2f452d |
| work/moneybench/LICENSE-TODO.md | True | 361 | c14a53909dd6844c3eb87cf091891b87354ab7f269178acd2a4b7ad46f66a718 |
| work/moneybench/LICENSE.template | True | 466 | 07f71722a4e11a880dcd2ca24d74e75e35d6b9099f3e242257e5140f20cb3d25 |

## Core Output Files

| Path | Exists | Bytes | SHA-256 |
| --- | --- | --- | --- |
| outputs/founderbench-task-manifest.json | True | 33747 | 8b5a4abb4452d30a1fca05e626693c890561ecd67987cf2e691448e0bb95b07e |
| outputs/founderbench-task-coverage.md | True | 3566 | 245976e316d20abdb0691210a730f1ac72ba26645b6a86736718d4e8d9396a3f |
| outputs/founderbench-task-provenance.md | True | 3763 | af572f0dc9ce61731a5c72a4d79a15fb7a7301096689d3edad36d5cbd4b67237 |
| outputs/founderbench-task-provenance.json | True | 33751 | f8b985f3b66695e04e24f278e86e600d6240c10c668fe6c76c700cf82e46b595 |
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
| outputs/founderbench-baseline-raw.json | True | 342072 | 63b23e18802e4a05d5875d04453ea6ace80b9cbf0e3652e4f3945758c7c5f140 |
| outputs/founderbench-baseline-leaderboard.json | True | 2653 | 978f0637f4188746f420331439eac9461182b7f4dde8156e4da132a1570c5efa |
| outputs/founderbench-leaderboard-policy.md | True | 3514 | d42a4e1e418e8a0b778a0186d93d79415a4e1930826f70aca7f2c17771475757 |
| outputs/founderbench-leaderboard-policy.json | True | 4254 | 968d139bf42dc11b82398f1d6c9734cb909df85469e4e108e1d807f19fdb9387 |
| outputs/founderbench-leaderboard-stability.md | True | 3181 | dc9a94adb6cd36d440c85720757fff8ea8a174a97f0c697d6b124db16b081f7a |
| outputs/founderbench-leaderboard-stability.json | True | 7593 | 401cd7098887e5618e693e57bbfbd9333a155a00e2d74d5703e3c1cb7dcc3b76 |
| outputs/founderbench-baseline-analysis.md | True | 4380 | ac32eeb85d6ef3d99ce300f6acf81fd66a4007120f22665864795512166045ae |
| outputs/founderbench-result-integrity-audit.md | True | 1582 | 5775845487070b74036712353911ec7f97efeb221601cc7afedd262fa818830c |
| outputs/founderbench-result-integrity-audit.json | True | 2081 | 5555e71699734b2144f4f45320332a224b1c5ce573e65dcfabc56ba6bc668d36 |
| outputs/founderbench-paper-tables.md | True | 5625 | 1d9d663b0cb630a9ef0dd7ea26b2e0664bee813ccd079a12e919021f8b0c92ae |
| outputs/founderbench-paper-figure-data.md | True | 1628 | 045386e39beec6bb40748ee699f81bdd780713ea7ce7d181f17cb722396fd130 |
| outputs/founderbench-paper-figure-data.json | True | 15206 | 315f479ff4babf5b4ba8e69977615ee9a5748fac84f090944419331ce5985fc0 |
| outputs/founderbench-paper-evidence-map.md | True | 8112 | dcdce617d8c230c19731018a0f3c434fad1d9c9e3eca4f3795a762e34ea906d6 |
| outputs/founderbench-paper-evidence-map.json | True | 17079 | 82b19415ef436b5a3ef0d5b517422d0ba81a94afbbe0ece941d733a0b417b0c5 |
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
| outputs/founderbench-action-ablation.json | True | 643534 | bb90c0b9199d8d912228d288f737cce4756bc7c0f503302e00e05172fe54d1d1 |
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
| outputs/founderbench-environment-report.md | True | 2189 | 9035ff5406d5bd6f836ca5d22b29c52c295ea5ff29b96fc98d850eebab4e03ee |
| outputs/founderbench-environment-report.json | True | 17951 | 413d65d1718bec91f3db63e6608e1f9a0809344e284b23049c451dfa4ac55918 |
| outputs/founderbench-simulator-invariant-audit.md | True | 1905 | 9e1c49db8b543b73e67107364c2fead3a4e5805e817c16e8aebaa837636f51dd |
| outputs/founderbench-simulator-invariant-audit.json | True | 8236 | cc42345df5327b16cd8117e03f9294c41bad1b81e86bc35345ecdd99e93e4c35 |
| outputs/founderbench-reviewer-smoke.md | True | 1315 | 7614c5cdf39ebcc2c3eb227769118222eb7e9ddb3b62ccddeadf1570cefadba5 |
| outputs/founderbench-reviewer-smoke.json | True | 1571 | 86440ba60fb471b5dd9116fc9cf2cdc1d179b6f485289fc06e1f8f1252e5dd26 |
| outputs/founderbench-random-repeats.md | True | 795 | dc06a41ef8dd83b1930253d6eb9d158fd9091235fb8c883086cf10a4ec01c62a |
| outputs/founderbench-qualitative-traces.md | True | 5229 | 326e987524ee2b5877a4fab14a04e890e9296b8ad6c209518a96c0dd7fbc4eb1 |
| outputs/founderbench-experiment-matrix.md | True | 5398 | 80c7bf6983a1c7ff540188df1e385fbb662e2605ab2343db624b9a4bac54783e |
| outputs/founderbench-human-calibration-protocol.md | True | 3803 | 5302fff34764c754063ac2e8569f4db65ac440745adb6e5a7f776831506cc3c3 |
| outputs/founderbench-human-calibration-protocol.json | True | 4335 | 3a70e9d2e17dd777d5ec697f2e6cc67f1ff3a3b491382cd06ccc4b16c8c4d616 |
| outputs/founderbench-human-calibration-schema.md | True | 2016 | eb4d86567c915739eee019391a0ce80febaff56d6e898e3224ee3a8d1a29b5ec |
| outputs/founderbench-human-calibration-schema.json | True | 2118 | 790a413db00631b415107e57142712a79340563be79993965ab2da9ccfc32e5c |
| outputs/founderbench-human-calibration-template.json | True | 6895 | 2a49e73a5fb67eef4b683a77e482938cb86777efe7ad290001441b893c8a5023 |
| outputs/founderbench-human-calibration-analysis.md | True | 988 | 3c6f2ec7edc1cc090f9bb21464ca7dfbaf503ad0c5d8581a7e41b64c85405f44 |
| outputs/founderbench-human-calibration-analysis.json | True | 884 | be7a0e15a1704629e33adc43b22063d67cf7d50f90be3307420e3d52d22f605e |
| outputs/founderbench-human-calibration-packet.md | True | 4904 | 1cc7b5b3b7f564ddb7c1a64910ead67624d11eb8ffdd646bac1ce9fcf55a9c03 |
| outputs/founderbench-human-calibration-packet.json | True | 5422 | 6dc1339379ff8eb3b68f3dc073738b9af36eeb829370e4c77d9a0f96d65f2bca |
| outputs/founderbench-private-holdout-smoke.md | True | 1334 | 70cccafccdb0f764ba5010dd450794d0e789c126ae60dbc394d99b6e9dde10fb |
| outputs/founderbench-private-holdout-smoke.json | True | 1782 | 3b961963c4d20019556db8aac89a28b908d5a99d4fae8d3c687c9e8fba4a8ae8 |
| outputs/founderbench-model-submission-schema.md | True | 1512 | 2de298cf1b7e03be276f624a36a890341e0755a00e8f70e8f4d7f7854ef4ade9 |
| outputs/founderbench-model-submission-schema.json | True | 20294 | 532abe875ee6855936086fac7745452d46de8f4f6b41f02f926e9d576c8327d9 |
| outputs/founderbench-submission-bundle-protocol.md | True | 1521 | 270d73e01f303b7eaf9502c9b2ec02bea9bf657615453326eb5a6063e7aefc71 |
| outputs/founderbench-submission-bundle-protocol.json | True | 1677 | 16389b4534c407b7475e1efacf65e22baf29083a5895e5dab527a5ddd2a3b4a1 |
| outputs/founderbench-prompt-protocol.md | True | 5413 | 7f9434fa613ecdaf1280840f89d425d3d95d0570c247b42df9034789b620271f |
| outputs/founderbench-prompt-protocol.json | True | 7834 | da1ad10b1b903563a27381f092d0c9b814c7350f26fed240b2cfa0866a2d00bc |
| outputs/founderbench-release-metadata-checklist.md | True | 3569 | 936a71ec8a2cf9ad5e6887b9932c8779dd1e4dc8185e8e5836523e17ae4d70e5 |
| outputs/founderbench-release-metadata-checklist.json | True | 4666 | 8159d973932723be2577761aef7689b6e1f49cd983be8b259b494cec71b19f2d |
| outputs/founderbench-cost-accounting.md | True | 2408 | cc38c163143b187b521b02b0c665f7574dc401138e409f5f8a8339a382e3158b |
| outputs/founderbench-cost-accounting.json | True | 2530 | 6ab1b03b528830e7abe68bf6798fc1160d68647a486e0fb5f270210cb839b8f5 |
| outputs/founderbench-submission-action-plan.md | True | 12944 | c862c0508acbf7742a1f3eab9c1edf7e35069495d453266415d8a1ae1a07602a |
| outputs/founderbench-submission-action-plan.json | True | 17599 | f4c1f9f2a6161e2ec3918c96b07c3b92325b07e234864e1a2d5174542fdedf41 |
| outputs/founderbench-completion-audit.md | True | 8168 | 85a6dad002c53eade8f7b91b240d9c6ceb48fc3f39b6f9ad29898bd1e6532627 |
| outputs/founderbench-completion-audit.json | True | 15309 | c7fb3769a8139b859439471efe185ab5f07fae60cb650761b2b3d260c205f594 |
| outputs/founderbench-submission-manifest.md | True | 5822 | e8fe52c8de6c04100356939cc466f9c1351c76f8588c395eaf912f784bf79456 |
| outputs/founderbench-submission-manifest.json | True | 9496 | c8f257b522358bba75eb314d3738382f8c77935e37e7652eba31f4e6806f6ef9 |
| outputs/founderbench-reviewer-risk-audit.md | True | 9847 | 852be3312720871302cedb0d06dcf231d1e9e5bb09b667a30ff95ce226efb62a |
| outputs/founderbench-reviewer-risk-audit.json | True | 13316 | e753f85bde80dc900589ce926a9a178d9898acaee63bcafd9fd61bdbcd2e34bc |
| outputs/founderbench-responsible-use.md | True | 4094 | d4d97a03a5f262f77857b2080e62283d0af9f80e0d0177dcc48bb13b72a553be |
| outputs/founderbench-responsible-use.json | True | 4508 | 251eebc2d69a4287b0ce75c7d28f4f1fddfcf503a7f44c0552ab506066338a1e |
| outputs/founderbench-failure-mode-audit.md | True | 8550 | 3588f67aba207edfbd95625df3bdf85e3fd5a058eb4c2d8be54daac1ac6ec170 |
| outputs/founderbench-failure-mode-audit.json | True | 11457 | ff247299879028d080ddeee043b9253f2e46d155fcf36faa30756fe4451deeac |
| outputs/founderbench-baseline-execution-plan.md | True | 18654 | 1f621eeebc36dd0e2a64cc0b7645c098f48abaa448b3bd1b5f2cb9c894d40621 |
| outputs/founderbench-baseline-execution-plan.json | True | 30324 | 2b6d42b79f0528b993014dfeb1de44c482b1637399b0a492ac1a7859db65ba82 |
| outputs/founderbench-experiment-runbook.md | True | 26100 | 1e46b8838aa4cc8690a06cb9efbc7485d0af1685e0a8a80b64fe898d314fbf78 |
| outputs/founderbench-experiment-runbook.json | True | 31000 | 868e1ac28703221a74d3e7c1a119ad930ed1abf10873198e3d60d0a36920f444 |
| outputs/founderbench-provider-run-status.md | True | 5626 | 08e609ce192f0abc3cac731627a67ae5022e5026375ae90dad20290e5e2dfdfb |
| outputs/founderbench-provider-run-status.json | True | 18244 | 0dd3347c5ac88c6d593854983a889b539c8b8652e989dd4739057227fbfb378b |
| outputs/founderbench-provider-comparability-audit.md | True | 4317 | 17d7ace2473e03696485c1f688224bbc951279dbee2aa9cab812d3f8d1ce3cb2 |
| outputs/founderbench-provider-comparability-audit.json | True | 10947 | d94557c20b8a3fb521caeb03edf0dc0b8e3e3b61ed5d4bc1ad9ec960492ea2b4 |
| outputs/founderbench-provider-contract-audit.md | True | 2165 | e49002ca67a018004037ce87f06accc6fa77fea8118cad051b96739d7bdafcfd |
| outputs/founderbench-provider-contract-audit.json | True | 3001 | 142c0c08be45585ef85abae317d4312486211d6a310c5927bfe2fe4bd23971d1 |
| outputs/founderbench-contamination-leakage-audit.md | True | 4315 | 3aca44ef8e48a38d86b30ef560d52daf180223ce55a16c09b58fcc310a3ddb31 |
| outputs/founderbench-contamination-leakage-audit.json | True | 5037 | f1bfe67f4de333c1a0d8001d5fba6ef0df17beb35b833bba9b1de3262be488de |

## Validation

Status: PASS

All listed core source and output files are present, and no secret values are recorded.
