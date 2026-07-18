# FounderBench v0.3 Reproducibility Manifest

This generated manifest records the source/output hashes and reproduction commands for the current workspace. It records only secret variable names, never secret values.

## Environment

| Field | Value |
| --- | --- |
| Python | 3.12.10 |
| Python executable | C:\Users\louis\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\python.exe |
| Platform | Windows-11-10.0.26200-SP0 |
| Machine | AMD64 |
| Working directory | C:\Users\louis\Documents\Codex\2026-07-14\use\work\moneybench |
| Git commit | not available |
| Secret values recorded | False |

## Commands

| Purpose | Working Directory | Command |
| --- | --- | --- |
| Regenerate all generated v0.3 artifacts | work/moneybench | `python -m moneybench.release regenerate` |
| Run tests and validate required outputs | work/moneybench | `python -m moneybench.release validate` |
| Build supplementary release bundle | work/moneybench | `python -m moneybench.release bundle` |

## Core Source Files

| Path | Exists | Bytes | SHA-256 |
| --- | --- | --- | --- |
| work/moneybench/moneybench/action_ablation.py | True | 11363 | 9b6a894529a314d20a3b313754e235e7e1e2ee509e97587d6123a68b24adc54d |
| work/moneybench/moneybench/action_semantics.py | True | 12618 | 549de44de20563d77d6d7dabf760adc159a6156b5b66e926a7eaf66d0e7493ac |
| work/moneybench/moneybench/baseline_execution_plan.py | True | 13721 | fc1cd3ed343c75cd2ee52ec38d31f862ef15f72f2373bc353c7b50dd6d948659 |
| work/moneybench/moneybench/benchmark_datasheet.py | True | 11494 | 4bcc6fd573432a2f678415958fcebd0231dc115b813a0625814466a0cf784f60 |
| work/moneybench/moneybench/bundle_integrity.py | True | 6118 | 6bd26fbafcd84015b4eecf0ab902a33985f421b1ca2965bac2847bc4a9c55408 |
| work/moneybench/moneybench/citation_audit.py | True | 10772 | f93043aae57b94c441211330aaffb2e42a4468af2ee38168b1e0e420879eb5f0 |
| work/moneybench/moneybench/completion_audit.py | True | 16972 | a33a53d2574c0ad71db06e74ef1713bcca963623a23ec20030bb788c4ccad038 |
| work/moneybench/moneybench/contamination_leakage_audit.py | True | 10823 | 3b8cd804b2652a7b06ddf6b628c22ec8c0fe0831c2e361fa89d4ad5f36d8473f |
| work/moneybench/moneybench/cost_accounting.py | True | 8282 | 5402f373947f961d6d1d98b29522fe00e12c58a41ba199d1e21ca868e3478d64 |
| work/moneybench/moneybench/determinism_audit.py | True | 6155 | a0ed8a66befba20eea09e2d6f713d95fa275d737a596d266d3a1735e02d1d501 |
| work/moneybench/moneybench/environment_report.py | True | 7175 | ae5f412061500fddbf2b88207530d585142dccdbe238fa72102c7ae1021dfeb1 |
| work/moneybench/moneybench/env.py | True | 17663 | fc60baf74776cbe02503554b759ee85793bbb541fa6c733d402a0bd3d975b320 |
| work/moneybench/moneybench/experiment_runbook.py | True | 14237 | 353d35339b70629f9ddc6d2f8e51769611628f450069d72c39e5d86e1d6bfb4a |
| work/moneybench/moneybench/failure_mode_audit.py | True | 14654 | 96ac562ad8d88e19e2d617ffd280655ea051aabde38640878cedf8386acfccf5 |
| work/moneybench/moneybench/holdout_smoke.py | True | 5580 | 0fc374259c50605d6e7a0b8d5bebe43eb6ae4f41ea1d40080cd5c0e54176f7dc |
| work/moneybench/moneybench/human_calibration.py | True | 9299 | cbc2a9955bf16a1bcb78c901a05f92eed4c6cd4fb2c2052e1a4a5c60ee754bb0 |
| work/moneybench/moneybench/human_calibration_analysis.py | True | 11905 | 33a3fe43d815b047c66c4e2bdb5dcb2dd1f0a1bab6ed2362c4a2c71af395bb68 |
| work/moneybench/moneybench/human_calibration_packet.py | True | 11952 | a5bbca0d87b5c5dc51fd030f144422c94433af0fdca465c8e653d984f9ecca74 |
| work/moneybench/moneybench/human_calibration_schema.py | True | 9496 | 1096cb117aaca95e6b1f6c995490c88ba0e2daf4fa2bd82fc107c3d21f699d8e |
| work/moneybench/moneybench/leaderboard_policy.py | True | 8991 | c266aedf7250a16b03df4eca0e3e594ea5635064add89ca4a9291eff9930a64a |
| work/moneybench/moneybench/leaderboard_stability.py | True | 10233 | f3e09f974e2be5ce18c0f4aaecd80f1ebcf8bddca5edcbde3e31fc01381fb1b1 |
| work/moneybench/moneybench/market_catalog.py | True | 8265 | fc29b1264a6ebf774966153dbd6dd7aede16cfb8bdcf809b1980ded0a88f0063 |
| work/moneybench/moneybench/tasks.py | True | 34061 | 352f0461a2252567319f33662da4a85cf8ac3e55628d55e8fdbe0cac1688c9d3 |
| work/moneybench/moneybench/task_cards.py | True | 7585 | 913fb40239c498acac2c73a14a1a343871788a3be28b5be2258119d5cc673741 |
| work/moneybench/moneybench/task_feasibility_audit.py | True | 10705 | 6b2e043163b712b30dc6c6a0b28af39e627012ce2d67574ed0158b85c64c4158 |
| work/moneybench/moneybench/task_runner.py | True | 8645 | 18fa28a684337850aea0e207b8447cd0492b33e7225dd86ce319f7d6ba4e7ad8 |
| work/moneybench/moneybench/task_provenance.py | True | 11857 | 034667fe15355ae28ec9e75fdf8bf363663a8173b7d7e70fa2a61fb06560e5fe |
| work/moneybench/moneybench/task_revision_ledger.py | True | 9982 | a93414f2e0b692e3aacb94b102fe0dade361df9328f18fbc2533d8679a7ab77a |
| work/moneybench/moneybench/policies.py | True | 17055 | a3474fbf6de7c1b5da4d440ff90b1945504bf9a32148d80eea38ce6d9dfda223 |
| work/moneybench/moneybench/difficulty_calibration.py | True | 11987 | f834a7b486d13593c4b56e7484c4c1860eb9d60a8d7735b35f49154ef41ddf1c |
| work/moneybench/moneybench/llm_policy.py | True | 17178 | 1f15a75ab068f8039168b8989acadd01633d41050fb33cf2c6046bf4ce85183e |
| work/moneybench/moneybench/metric_sensitivity.py | True | 10942 | 931fe5cc85f822ab6cfe7b6e9f8bd8dcad18cebdd6473428cd04c935e8e30c65 |
| work/moneybench/moneybench/model_comparison.py | True | 9017 | 97e3343a1af993a624474b4fd938b3692bc0ff6cf5addb7a32b0c854a07e1265 |
| work/moneybench/moneybench/model_result_cards.py | True | 10855 | 830a8a7b5080d3d8a9ebb7e2596a0c10ed2f67d4d0cd27b17eedf91b9c0b5de2 |
| work/moneybench/moneybench/paper_claim_lint.py | True | 8768 | 592f0cf74c034e223d42f299f3415df085f4caed6bd14c128e61902349ac39de |
| work/moneybench/moneybench/paper_evidence_map.py | True | 13956 | 0cc4ad795db6426174e8e7842236ed770a98dcca8f2fa484a3dc785cd11cf508 |
| work/moneybench/moneybench/paper_figures.py | True | 8692 | 780bae958ed90e145b811bc11fdb92231177ed75a766c3277922cad61b89b862 |
| work/moneybench/moneybench/paired_statistics.py | True | 10772 | f891c75220b429704941b5cfc89a4e441fcadcaf5ab3359a62d9001aed4578d7 |
| work/moneybench/moneybench/power_analysis.py | True | 8924 | 04662ea5e3fd858bd42857eb6438064fb20ef4f76a73a1867b1106b03e6d7087 |
| work/moneybench/moneybench/prompt_protocol.py | True | 8341 | 5937978a9def514d8b0d616f101438a8a6b924e36d0369fee6387a2b5d7d40c8 |
| work/moneybench/moneybench/private_holdout_evaluator.py | True | 7766 | 24a1c1579cd8d992545031140ef3352945afa3377f3e15d7fbbc4c63384f3f5b |
| work/moneybench/moneybench/provider_comparability_audit.py | True | 10967 | 52699863ce49c4f98dde9f53727df7379e74f8ccaa1b2d9b3475318bd91db39e |
| work/moneybench/moneybench/provider_contract_audit.py | True | 8912 | aeadca3ab62d4bcb8ab3775045f245fd7066767df5e90e9aea72da01a0ff3cae |
| work/moneybench/moneybench/provider_run_status.py | True | 10829 | 22db2f97ae1223d5f83e2239259cb9ee4d7fc5fc769746f226dc5959b00e04fc |
| work/moneybench/moneybench/release_metadata.py | True | 7465 | bbc7352d82f2ed11fa608cb48fcc0f5d2d38a4f99f171aeeeb8234439d3ea2c5 |
| work/moneybench/moneybench/responsible_use.py | True | 9266 | 9ffd201a857987aeb872c76612d6741a69a1cb108ab52e0c4ab513fca46eb721 |
| work/moneybench/moneybench/result_integrity_audit.py | True | 9898 | 353647712da5a6659711addfbbe62c38e0f67cdedbe4f2ce827e902a1861bf24 |
| work/moneybench/moneybench/reviewer_risk_audit.py | True | 16191 | 343bdff0cedccd2d6b467399b7572b3efd765c280ca11178c04ebb2b9175e103 |
| work/moneybench/moneybench/reviewer_smoke.py | True | 5860 | e62f92b5c78848159b4edeafb6a659da5fdcd181a76b4ae29bf849e4132adbdb |
| work/moneybench/moneybench/simulator_invariant_audit.py | True | 12450 | 670f1ef8a295eb866cc29031376ee0134c467bf882a00a57397162b5786f0804 |
| work/moneybench/moneybench/scoring_consistency_audit.py | True | 10969 | c25c1d3839c8657eb6f455e3441d3b0cba075bb586dbcc40b6aba6404a7dc3d5 |
| work/moneybench/moneybench/statistical_protocol.py | True | 8619 | 7e2e4e1aa90abec11d77e98466611c3ff3c65f8e91dea1fcf9be91cdf69c76c4 |
| work/moneybench/moneybench/submission.py | True | 8913 | db3c30122c5b906fb57062af409b2e8e80f3bc2d30168c7166f94af9d1e145f6 |
| work/moneybench/moneybench/submission_action_plan.py | True | 9588 | 9f9b44c67ec44f9d10f791996e495b303c133a01b026e3b1659842d7a63dcfd6 |
| work/moneybench/moneybench/submission_bundle.py | True | 8649 | 346dbb055103541bfc61e1b83291c01f2fe3a625fcf9aae8d810a07d4f31b545 |
| work/moneybench/moneybench/submission_manifest.py | True | 10732 | b4318b2748c0e6aa04c8e3086d2648f4897792316a27b24e7c4ea16b63812dc9 |
| work/moneybench/moneybench/submission_schema.py | True | 9164 | aa7f7922bbdf9dde5da06da1b16d77f704049de7836b5aa6845719fbc77d2219 |
| work/moneybench/moneybench/release.py | True | 32799 | 579e57ed57224780181026a3ad01707a7900e1a3910a42a8fb53b090e8b541aa |
| work/moneybench/moneybench/resumable_runner.py | True | 4750 | 3f061139fe9c550345488586106c576fcafad6e6da291457beef93507db914e5 |
| work/moneybench/tests/test_moneybench.py | True | 68047 | 1abd9ef9ce55ee98e6d66f948166e5e485dae48235f8d1fb99db2986a29ea2a9 |
| work/moneybench/README.md | True | 21778 | c598c1515ac868979b0a9d00a0d7d3f5c17563c2da075501484a141e254e2eda |
| work/moneybench/SPEC.md | True | 9226 | 924c5166bb5f2f2e10a12aae609c728253630ddb886cc2205de6c33b8810a525 |
| work/moneybench/CITATION.cff | True | 541 | fc79196709ee50f87478b68eb24ad22090a93e82fe08c22c71920d121d40feb5 |
| work/moneybench/CITATION.cff.template | True | 571 | 56e998b3e9b2d2d023079083d88bfc013ffacc084f110d7acf6328e050556bc4 |
| work/moneybench/LICENSE-TODO.md | True | 361 | c14a53909dd6844c3eb87cf091891b87354ab7f269178acd2a4b7ad46f66a718 |
| work/moneybench/LICENSE.template | True | 475 | 8f84386c7c53bd2edac1f378e7bbe01d83e7a2c05880ad699ffca18408962744 |

## Core Output Files

| Path | Exists | Bytes | SHA-256 |
| --- | --- | --- | --- |
| outputs/acceleratorbench-task-manifest-v0.3.json | True | 33738 | 32ff27d0692326fe86e49438d51bbc1be7031aa9a2876d470b5d884abaab49bc |
| outputs/acceleratorbench-task-coverage-v0.3.md | True | 3571 | 27fd5f52d8d38ff6a691713b23a04871b6d55afb04818afe9848f576376aba11 |
| outputs/acceleratorbench-task-provenance-v0.3.md | True | 3741 | d6547da9d61ac6329bda90b9e649a9d445864d734b659f822836eabd2de5e1b0 |
| outputs/acceleratorbench-task-provenance-v0.3.json | True | 33733 | bba4fcd591aea0f00f1babf900ed2a7ef22a5f190cd86d7b58c5609966a0c2b0 |
| outputs/acceleratorbench-task-cards-v0.3.md | True | 38551 | 72d422139229f16bda5cde94fe2c12d87e2ffd0dba1af7d36ff4726194b6e6c3 |
| outputs/acceleratorbench-task-cards-v0.3.json | True | 66552 | 9831939e9bbdb9efe5ada98e28269f101a2b55731802071273b98486d56b66fe |
| outputs/acceleratorbench-action-semantics-v0.3.md | True | 8408 | ef9622e7cc27de6faf8fc21c00baf08006ab3dfae5c5bcf18b4376faa8155b34 |
| outputs/acceleratorbench-action-semantics-v0.3.json | True | 8747 | 819c5e3da1b488d480f3c5bb3416c28e77ecee9bcf2925ce3f454f63343b7b9b |
| outputs/acceleratorbench-datasheet-v0.3.md | True | 5252 | 195fabcdaf71d37448fa2449cd9370334311319f9576662f4fe537719d1cd12f |
| outputs/acceleratorbench-datasheet-v0.3.json | True | 6704 | 629d0a6a15aa7cc8bf763f13527e1632d90583b55e3c3425eb5a50ba7347bcff |
| outputs/acceleratorbench-market-catalog-v0.3.md | True | 5291 | 19424efa3a6bf75fac1db9aa2151da0104d977a19c28d1392ec70289d8b03a89 |
| outputs/acceleratorbench-market-catalog-v0.3.json | True | 8019 | 34e6e42fd16c90c6463c581e8f53d24e18d87dc1693b46e17911fdabf5b0bfc5 |
| outputs/acceleratorbench-score-rubric-v0.3.md | True | 7097 | c47591b8930b24673f8b28ac98aff8afef6651af0e0bfa48c88f2de807258770 |
| outputs/acceleratorbench-scoring-consistency-audit-v0.3.md | True | 3812 | cd65125adb1d6dc315da67867ecdb68a4ebfeb7cd82938974bb7038402ed10c5 |
| outputs/acceleratorbench-scoring-consistency-audit-v0.3.json | True | 6421 | 6d24ced510165565d0962b9a6d7fce87d751c4d8edb6378b74460b0485f3e4a7 |
| outputs/acceleratorbench-metric-sensitivity-v0.3.md | True | 3118 | 469a36e974a9578c78f926d82b0ab55c9ed70726ff2edd649f945b677ae896b3 |
| outputs/acceleratorbench-metric-sensitivity-v0.3.json | True | 5839 | 8473ee17391722a7416b175ee119c4dfbb30442fb30e674af6df2a90342af83e |
| outputs/acceleratorbench-baseline-raw-v0.3.json | True | 342102 | 10c54bd61e3967dc740713e46e6dcddf9c5317938b45368049ead871d7aa3ea1 |
| outputs/acceleratorbench-baseline-leaderboard-v0.3.json | True | 2653 | 87620032604cb4588b43e3c3a8cd035dfe4e0c06866ac004a22943b7134a39c6 |
| outputs/acceleratorbench-leaderboard-policy-v0.3.md | True | 3488 | fd9eb2a95837bf85a236cc18b12d97dafba0520bc966180f5c74249dba758f10 |
| outputs/acceleratorbench-leaderboard-policy-v0.3.json | True | 4223 | 1b3bbaf1e083ad1425cab637d45658c680a92ea166c0dbd0570f9b19e16d618d |
| outputs/acceleratorbench-leaderboard-stability-v0.3.md | True | 3186 | 67eb2e253b6a4531efda6fb7601fad40c7853668966e42776880b542cd1876e6 |
| outputs/acceleratorbench-leaderboard-stability-v0.3.json | True | 7602 | 1633dc964cdf014224eddade9570306d339c9b9e065deef092e15dd6fedb4d9d |
| outputs/acceleratorbench-baseline-analysis-v0.3.md | True | 4385 | ecd832b81f60c951978f8af3f38f6076ac87b96a343daaee1bbf2226444eabfc |
| outputs/acceleratorbench-result-integrity-audit-v0.3.md | True | 1623 | c2828d04df1d5cacb26dff7d4f393c5e3d26624cda4de2aa5cb2a5e5684f2ec2 |
| outputs/acceleratorbench-result-integrity-audit-v0.3.json | True | 2117 | 7219fa202097fcbfab2e320e79c4e83131453f120ecf38dab1733aca5cfc7a3d |
| outputs/acceleratorbench-paper-tables-v0.3.md | True | 4587 | 7e212cf813b94e6567bb176f876c60e0112553c766e2516b1490b3adb215c203 |
| outputs/acceleratorbench-paper-figure-data-v0.3.md | True | 1647 | f9465a553455d8cb97b17b0a46542021fcdc1d319ff299c6c864378ce93ee431 |
| outputs/acceleratorbench-paper-figure-data-v0.3.json | True | 15231 | 6b97de4cd46696da4bc4d36e7799e7c76a49b786881088ae831779b0e9c11ba7 |
| outputs/acceleratorbench-paper-evidence-map-v0.3.md | True | 8562 | 0b21293b5ec274885202891606283470456cd0641b791396f17226cdf7b53312 |
| outputs/acceleratorbench-paper-evidence-map-v0.3.json | True | 17538 | 526a948b2d1af3b759dffa6bc0d43f2aedfc9b3d2c59c11e18e9a03ef8173b4d |
| outputs/acceleratorbench-paper-claim-lint-v0.3.md | True | 1548 | 75cb8a52f200be1895c5c58eba5e7616191563ab3bfb3ad5b0569bb4013910ba |
| outputs/acceleratorbench-paper-claim-lint-v0.3.json | True | 1893 | a8579d15579f8896e2b4b793ca92474ef9c4d56e4fc73e2183d01aee2064c1b6 |
| outputs/acceleratorbench-citation-audit-v0.3.md | True | 2656 | 66db0aa7861578aca92bbe5e025ed5375de420774f0fbf19a719e81f671dcb04 |
| outputs/acceleratorbench-citation-audit-v0.3.json | True | 8491 | 9fc078551b8201086b50a2de7dd7ad2772f5cbe95fcb30c196b1e74b6f32aad5 |
| outputs/acceleratorbench-model-comparison-v0.3.md | True | 4618 | c1cb5142fcbcc0d402acfcdb524ab3ea8910e839b5adecf106e88ef3f66609fc |
| outputs/acceleratorbench-model-comparison-v0.3.json | True | 9674 | a6548c7c9c6841e6d549c7ca7501d6548141d009462cbadf131fe5f82a158760 |
| outputs/acceleratorbench-model-result-cards-v0.3.md | True | 3164 | ec33567a1782d07087d0a566d34e511243999eff9b9595d8ca42c5015a6280f1 |
| outputs/acceleratorbench-model-result-cards-v0.3.json | True | 7987 | ccb8e6bb180222c69e5ff67d3cd45968730c8011756bd3d0b164c8b80e3ae033 |
| outputs/acceleratorbench-ablation-report-v0.3.md | True | 2449 | 4efa8d30bf1176a465518beb7049cdfe3293ec91de586e50e24ac2cdea5bcc9a |
| outputs/acceleratorbench-action-ablation-v0.3.md | True | 2377 | 4cc42bb8b9e0288b70d2a77a84895c8fbfdbbe18a672f6c26675120f37accb35 |
| outputs/acceleratorbench-action-ablation-v0.3.json | True | 643744 | 6f375d36be89bbcf5e6c9233dcdd51ff708293943ba2c5a672d5f072c7052e29 |
| outputs/acceleratorbench-paired-statistics-v0.3.md | True | 2174 | 0e42912ac060f0ec7cfcdea0caead5e8156d429e33f5342cd9cebdac9290eefa |
| outputs/acceleratorbench-paired-statistics-v0.3.json | True | 2715 | 1ab1840f6fd36ca2997ddfb34e6233ea453670e99205b953d6d0d9118845b90c |
| outputs/acceleratorbench-power-analysis-v0.3.md | True | 3053 | e9e7248d73d4df5d44ce946618c3733a7b86af2e7730d476324a5da40ca7bea6 |
| outputs/acceleratorbench-power-analysis-v0.3.json | True | 3790 | 99779464b555388e8eda9139029bfe7b5cf742f3a62957b7ad67eb940ec4e9e8 |
| outputs/acceleratorbench-statistical-protocol-v0.3.md | True | 3583 | 9851e7d24692febbc16a7a95434bbecee89dc7a1c81bcba263de3815ba9d73e6 |
| outputs/acceleratorbench-statistical-protocol-v0.3.json | True | 3653 | 0167f7c32c6584f277d6fbce6632d8aae6a87ea7d32bee0e4b01957a68cf1700 |
| outputs/acceleratorbench-difficulty-calibration-v0.3.md | True | 5571 | 331508f082c8d4d5dca4f0ba1710a076e3c409312877269085c20c513374f84e |
| outputs/acceleratorbench-difficulty-calibration-v0.3.json | True | 37661 | 680ca595dd73bfd172fa3ff5745e29c2f087d5a796cb6e7a1a20608e650a6e40 |
| outputs/acceleratorbench-task-feasibility-audit-v0.3.md | True | 12201 | 2e2fcd2566942cb840a4dc9fb11176d3673cb2c1e9113de2bd883c7c289a4500 |
| outputs/acceleratorbench-task-feasibility-audit-v0.3.json | True | 28826 | d01946bc0aff8a466ad48e128648d92ead31f47993c94f3b70838a6b852f426f |
| outputs/acceleratorbench-task-revision-ledger-v0.3.md | True | 8777 | 0c25c3e02af3fafd5246a3d4e83f9f36e145e06704058022b90346f7290c8fa0 |
| outputs/acceleratorbench-task-revision-ledger-v0.3.json | True | 16194 | d8cf0efb208ca9bf50fa94b9719baa4ae83f83a46fc68ae0ca46c62cbf29b850 |
| outputs/acceleratorbench-determinism-audit-v0.3.md | True | 1303 | 863d5e379c96c09b5f96c0ec383bd14f335b1041e0be9f2359550ca6e6496277 |
| outputs/acceleratorbench-determinism-audit-v0.3.json | True | 2364 | 41291d09fd643a4161d072b3cdbae50471b071e6317d2140a2990a4ba3cd5e88 |
| outputs/acceleratorbench-environment-report-v0.3.md | True | 2183 | 92fd6235d8faedb60f22f6613929043aafc758ef8d4e3c0d25b88bccd88e5e97 |
| outputs/acceleratorbench-environment-report-v0.3.json | True | 17940 | a9f6c2e9b7def5c3defade587ee26b5d1754bb5f079e3de629988adfacba1038 |
| outputs/acceleratorbench-simulator-invariant-audit-v0.3.md | True | 1910 | 596b8998b6db59d5fd3dda04cd6b059b1a738f94f80a67c63ed7ab27a24ff868 |
| outputs/acceleratorbench-simulator-invariant-audit-v0.3.json | True | 8236 | cc42345df5327b16cd8117e03f9294c41bad1b81e86bc35345ecdd99e93e4c35 |
| outputs/acceleratorbench-reviewer-smoke-v0.3.md | True | 1365 | f8d48f8e91b0d5dffb09fb1e276a699f0b07b935077aec2b0083b0aaca1505ae |
| outputs/acceleratorbench-reviewer-smoke-v0.3.json | True | 1616 | c319722727c236675084e261bca2002224d58d350da2852675c06e092db27c6d |
| outputs/acceleratorbench-random-repeats-v0.3.md | True | 800 | 8064e1fbaea3bdc388c750c91af89a2bc7c3ce5798e9b1213cd061de0b342127 |
| outputs/acceleratorbench-qualitative-traces-v0.3.md | True | 5234 | 03166c1fb171991363c2b5cd2e61e195926938f6aae2d53e5e7baeb28a730739 |
| outputs/acceleratorbench-experiment-matrix-v0.3.md | True | 5601 | ae75bd3284e1ec98fbc16d3f2249695653e2fefa611ee767b738ed1133b6a08e |
| outputs/acceleratorbench-human-calibration-protocol-v0.3.md | True | 3808 | 5f967093de83e301a26a9ed76cbad20484238665a0958fd96743ca4851d002d3 |
| outputs/acceleratorbench-human-calibration-protocol-v0.3.json | True | 4335 | 3a70e9d2e17dd777d5ec697f2e6cc67f1ff3a3b491382cd06ccc4b16c8c4d616 |
| outputs/acceleratorbench-human-calibration-schema-v0.3.md | True | 2021 | 0b9f14ebf77ed38db503f23c6b3d0e1298b46e338a03c6a2d2dfd21f7ffd764d |
| outputs/acceleratorbench-human-calibration-schema-v0.3.json | True | 2118 | 790a413db00631b415107e57142712a79340563be79993965ab2da9ccfc32e5c |
| outputs/acceleratorbench-human-calibration-template-v0.3.json | True | 6895 | 2a49e73a5fb67eef4b683a77e482938cb86777efe7ad290001441b893c8a5023 |
| outputs/acceleratorbench-human-calibration-analysis-v0.3.md | True | 993 | 80d8cb8417e932f7d908b0a750dd630000a68f2e44baab1cb7220ea098060b50 |
| outputs/acceleratorbench-human-calibration-analysis-v0.3.json | True | 884 | be7a0e15a1704629e33adc43b22063d67cf7d50f90be3307420e3d52d22f605e |
| outputs/acceleratorbench-human-calibration-packet-v0.3.md | True | 4981 | 6cd392a40061ae5473c4028ee91508d1a3bfec29654aad8ca70417b7a7a19b65 |
| outputs/acceleratorbench-human-calibration-packet-v0.3.json | True | 5494 | 3666836cac89e1f5534df74cd39e893af97cb7cb7d7cec4bc375f5ac6f72ff25 |
| outputs/acceleratorbench-private-holdout-smoke-v0.3.md | True | 1339 | d55d7ad9421812069a8d7915ab5d1a7109bd4a8d5f5b2ddd4d3c73787cebb2bb |
| outputs/acceleratorbench-private-holdout-smoke-v0.3.json | True | 1782 | 307ff25a76b6149596fb05826e7eddad90495c9de4a677261717f1f1637dd5b1 |
| outputs/acceleratorbench-model-submission-schema-v0.3.md | True | 1506 | 1e68414aa5194e3c5e44cd61e7798be30bc9caba68d28d97896a453ea72fa220 |
| outputs/acceleratorbench-model-submission-schema-v0.3.json | True | 20304 | 7df83c2e41259b6472c3dc46cb8cb161bbc47117cd48e7bf79cb0c6cf60f42f0 |
| outputs/acceleratorbench-submission-bundle-protocol-v0.3.md | True | 1584 | f55fcd33628f80fff828e360b4f67258cf1e8e4b4177808519a6fd55f1b7baa4 |
| outputs/acceleratorbench-submission-bundle-protocol-v0.3.json | True | 1740 | 1419fc96c79bf11f894eb6c17e20dc02c1eedcd0728152ec1ac366c9638b5875 |
| outputs/acceleratorbench-prompt-protocol-v0.3.md | True | 4536 | 17e221f3e75b5bdfb925a752acab3fae1cb126b0cfbbbe8c60f7eabf42165d09 |
| outputs/acceleratorbench-prompt-protocol-v0.3.json | True | 5473 | 3eab1608f4db6e35bcdccee086e4b06c5290625111eee2bde51d76341893d367 |
| outputs/acceleratorbench-release-metadata-checklist-v0.3.md | True | 3574 | fcb02b172149d4f721169b69748f167ee2011d07f71f31c03a81acbf147ac058 |
| outputs/acceleratorbench-release-metadata-checklist-v0.3.json | True | 4666 | 8159d973932723be2577761aef7689b6e1f49cd983be8b259b494cec71b19f2d |
| outputs/acceleratorbench-cost-accounting-v0.3.md | True | 2413 | 35f618708b255d2d4bea64c8afa8270f160d7d304c9417e9fea5d1d6b6e214ee |
| outputs/acceleratorbench-cost-accounting-v0.3.json | True | 2530 | 6ab1b03b528830e7abe68bf6798fc1160d68647a486e0fb5f270210cb839b8f5 |
| outputs/acceleratorbench-submission-action-plan-v0.3.md | True | 13345 | 7c42658efb279cc8cf213c84f7e584f6117be513ffc23beff123a8fa2370369e |
| outputs/acceleratorbench-submission-action-plan-v0.3.json | True | 18240 | 33091cb141aec5a317bde5c78a98fe9b3af27cb0f5ee1917b6f36cb9c6ac81fb |
| outputs/acceleratorbench-completion-audit-v0.3.md | True | 8627 | 48e2bd72722e08734c3d7d4d60bbf11732e1bd018b53c1c4e124e9d0d7477120 |
| outputs/acceleratorbench-completion-audit-v0.3.json | True | 15764 | 958fc00e09ec9d10c152ecdb31b48dc4f1db6c03087f83cdfd2ab7adefe739cf |
| outputs/acceleratorbench-submission-manifest-v0.3.md | True | 6050 | ef2772c8fc363f2c654cf4934300ca29d67da53e59bd4267e546be72e23429e4 |
| outputs/acceleratorbench-submission-manifest-v0.3.json | True | 9719 | 2df761770c0f88abfd9723546d9afd85aa35270058da5cd786abe73829cbed0e |
| outputs/acceleratorbench-reviewer-risk-audit-v0.3.md | True | 10135 | dde75a866adb88e8796ed3e71a4ddb5264fd1342ad496e21c87821489f375400 |
| outputs/acceleratorbench-reviewer-risk-audit-v0.3.json | True | 13599 | 2e9ad0f922fb69689c7ce53c740a78ea3c768a1373645d991606e5a657b4301b |
| outputs/acceleratorbench-responsible-use-v0.3.md | True | 4105 | 7e5035cbbaee8935b3172ea65061e6c007281f591e148f1950c5decceb7a72e9 |
| outputs/acceleratorbench-responsible-use-v0.3.json | True | 4514 | 203adb74b636d5b6716b1e2823ba6df5be59252560f7fba67b3023dc97fdca0c |
| outputs/acceleratorbench-failure-mode-audit-v0.3.md | True | 8786 | 1235ee36ec3be3176846d7a1764bf0f193eef9bcb46f8cfc1b7f2d72d6b3c278 |
| outputs/acceleratorbench-failure-mode-audit-v0.3.json | True | 11689 | 539f2ef81b96c249471ee39d5071ede238b3ab755b166508eb8903daf38f87b3 |
| outputs/acceleratorbench-baseline-execution-plan-v0.3.md | True | 10314 | 382cc1ee86494f4995cabc8d1e4219dc61c6aef588f3b470824b5756453bf76c |
| outputs/acceleratorbench-baseline-execution-plan-v0.3.json | True | 15421 | b03363606655bbdf4365434938ab3f39e1834f4556e5277de86a103450f5b8ce |
| outputs/acceleratorbench-experiment-runbook-v0.3.md | True | 15964 | 6dff4e5e038567df73c9d8f75d68b58bf69c2b51321c6f8d40754a38665b640e |
| outputs/acceleratorbench-experiment-runbook-v0.3.json | True | 18521 | 7c9bb334e139b038b11be8c38a34fca927c473d219248649806c9971539b332d |
| outputs/acceleratorbench-provider-run-status-v0.3.md | True | 4463 | 51c5db340d4ecc118e44288cb6187115480ba1baccdae419a5af6f462da67052 |
| outputs/acceleratorbench-provider-run-status-v0.3.json | True | 10488 | fd83d87b63b0c322378c479d9c718691d661ecfc5b165e2a776fba230ef5815b |
| outputs/acceleratorbench-provider-comparability-audit-v0.3.md | True | 3255 | d28089cf323551ca9328973cf083f68ffa9f53abd1708cfca0eac0a134578a3e |
| outputs/acceleratorbench-provider-comparability-audit-v0.3.json | True | 5893 | 00464c3e5e55819dec7d2b7d4aff3b902c0c1cc65a636365f3a38088508f4d8a |
| outputs/acceleratorbench-provider-contract-audit-v0.3.md | True | 2170 | 8e5305862432f6c2ea2de31574e580946d0c2cf8116033c6cc46d1a5f444662a |
| outputs/acceleratorbench-provider-contract-audit-v0.3.json | True | 3001 | 142c0c08be45585ef85abae317d4312486211d6a310c5927bfe2fe4bd23971d1 |
| outputs/acceleratorbench-contamination-leakage-audit-v0.3.md | True | 4302 | befbf22a0d50df9a8ee3498b547f24c14198af8cd0b732b67ffea37e559a2cd1 |
| outputs/acceleratorbench-contamination-leakage-audit-v0.3.json | True | 5019 | f4f80a1b5048332080971bc8959c6a7af5dcaf41621069c3a950e467e558ba2e |

## Validation

Status: PASS

All listed core source and output files are present, and no secret values are recorded.
