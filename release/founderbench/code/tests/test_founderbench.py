import json
import tempfile
import unittest
from pathlib import Path

from founderbench.cli import run
from founderbench.action_semantics import build_catalog as build_action_catalog, validate_catalog as validate_action_catalog
from founderbench.action_ablation import build_report as build_action_ablation_report, validate_report as validate_action_ablation_report
from founderbench.ablation import ablation_rows, family_gain_rows
from founderbench.analysis import bootstrap_mean_ci
from founderbench.baseline_execution_plan import build_plan as build_baseline_execution_plan, validate_plan as validate_baseline_execution_plan
from founderbench.benchmark_datasheet import build_datasheet as build_benchmark_datasheet, validate_datasheet as validate_benchmark_datasheet
from founderbench.bundle_integrity import build_report as build_bundle_integrity_report, validate_report as validate_bundle_integrity_report
from founderbench.citation_audit import build_audit as build_citation_audit, validate_audit as validate_citation_audit
from founderbench.claim_evidence import build_report as build_claim_report, validate_report as validate_claim_report
from founderbench.completion_audit import build_audit as build_completion_audit, validate_audit as validate_completion_audit
from founderbench.contamination_leakage_audit import build_audit as build_contamination_leakage_audit, validate_audit as validate_contamination_leakage_audit
from founderbench.cost_accounting import build_protocol as build_cost_accounting_protocol, estimate_cost, validate_protocol as validate_cost_accounting_protocol
from founderbench.difficulty_calibration import build_report as build_difficulty_report, validate_report as validate_difficulty_report
from founderbench.determinism_audit import build_audit as build_determinism_audit, validate_audit as validate_determinism_audit
from founderbench.environment_report import build_report as build_environment_report, validate_report as validate_environment_report
from founderbench.env import FounderBenchEnv
from founderbench.experiment_matrix import build_matrix
from founderbench.experiment_runbook import build_runbook as build_experiment_runbook, validate_runbook as validate_experiment_runbook
from founderbench.failure_mode_audit import build_audit as build_failure_mode_audit, validate_audit as validate_failure_mode_audit
from founderbench.holdout import evaluator_protocol, generate_private_fingerprint_manifest, public_blueprint, validate_blueprint, validate_fingerprint_manifest
from founderbench.holdout_smoke import build_report as build_holdout_smoke_report, validate_report as validate_holdout_smoke_report
from founderbench.human_calibration import build_protocol as build_human_calibration_protocol, validate_protocol as validate_human_calibration_protocol
from founderbench.human_calibration_analysis import build_analysis as build_human_calibration_analysis, validate_analysis as validate_human_calibration_analysis
from founderbench.human_calibration_packet import build_packet as build_human_calibration_packet, validate_packet as validate_human_calibration_packet
from founderbench.human_calibration_schema import blank_template as human_calibration_template, build_schema as build_human_calibration_schema, validate_schema as validate_human_calibration_schema, validate_submission as validate_human_calibration_submission
from founderbench.license_readiness import build_report as build_license_report, validate_report as validate_license_report
from founderbench.leaderboard_policy import build_policy as build_leaderboard_policy, validate_policy as validate_leaderboard_policy
from founderbench.leaderboard_stability import build_audit as build_leaderboard_stability_audit, validate_audit as validate_leaderboard_stability_audit
from founderbench.llm_policy import redact_text
from founderbench.local_model import protocol as local_model_protocol, validate_local_config
from founderbench.market_catalog import build_catalog as build_market_catalog, validate_catalog as validate_market_catalog
from founderbench.metric_sensitivity import build_report as build_metric_sensitivity_report, validate_report as validate_metric_sensitivity_report
from founderbench.model_comparison import build_report as build_model_comparison_report, validate_report as validate_model_comparison_report
from founderbench.model_result_cards import build_cards as build_model_result_cards, validate_cards as validate_model_result_cards
from founderbench.paper_claim_lint import build_audit as build_paper_claim_lint, validate_audit as validate_paper_claim_lint
from founderbench.paper_evidence_map import build_map as build_paper_evidence_map, validate_map as validate_paper_evidence_map
from founderbench.paper_figures import build_figure_data, validate_figure_data
from founderbench.paper_tables import build_tables, provider_status
from founderbench.paired_statistics import build_report as build_paired_statistics_report, validate_report as validate_paired_statistics_report
from founderbench.power_analysis import build_analysis as build_power_analysis, validate_analysis as validate_power_analysis
from founderbench.prompt_protocol import build_protocol as build_prompt_protocol, validate_protocol as validate_prompt_protocol
from founderbench.provider_comparability_audit import build_audit as build_provider_comparability_audit, validate_audit as validate_provider_comparability_audit
from founderbench.provider_contract_audit import build_audit as build_provider_contract_audit, validate_audit as validate_provider_contract_audit
from founderbench.provider_adapter import ProviderResponseError, classify_provider_exception, parse_provider_response
from founderbench.provider_readiness import readiness_matrix
from founderbench.provider_run_status import build_status as build_provider_run_status, validate_status as validate_provider_run_status
from founderbench.private_holdout_evaluator import generate_private_tasks, run_private_holdout, validate_private_report
from founderbench.publication_audit import audit
from founderbench.qualitative import build_trace_examples, select_examples
from founderbench.references import REFERENCE_ENTRIES, bibtex_text, validate_bibtex
from founderbench.release_metadata import build_checklist as build_release_metadata_checklist, validate_checklist as validate_release_metadata_checklist
from founderbench.responsible_use import build_statement as build_responsible_use_statement, validate_statement as validate_responsible_use_statement
from founderbench.repeats import interval_rows, run_repeated, validate_repeated
from founderbench.reproducibility_manifest import build_manifest, validate_manifest
from founderbench.result_integrity_audit import build_audit as build_result_integrity_audit, validate_audit as validate_result_integrity_audit
from founderbench.reviewer_index import build_index
from founderbench.reviewer_risk_audit import build_audit as build_reviewer_risk_audit, validate_audit as validate_reviewer_risk_audit
from founderbench.reviewer_smoke import build_report as build_reviewer_smoke_report, validate_report as validate_reviewer_smoke_report
from founderbench.release import OUTPUTS, PACKAGE_ROOT, validate_outputs, write_checksum_manifest
from founderbench.resumable_runner import summarize as summarize_resumable_results
from founderbench.schema import Action
from founderbench.score_rubric import build_rubric, validate_rubric
from founderbench.scoring_consistency_audit import build_audit as build_scoring_consistency_audit, validate_audit as validate_scoring_consistency_audit
from founderbench.simulator_invariant_audit import build_audit as build_simulator_invariant_audit, validate_audit as validate_simulator_invariant_audit
from founderbench.statistical_protocol import build_protocol as build_statistical_protocol, validate_protocol as validate_statistical_protocol
from founderbench.submission import write_submission_report, validate_run
from founderbench.submission_action_plan import build_plan as build_submission_action_plan, validate_plan as validate_submission_action_plan
from founderbench.submission_bundle import bundle_payload, build_protocol as build_submission_bundle_protocol, validate_bundle, validate_protocol as validate_submission_bundle_protocol
from founderbench.submission_gate import build_gate, validate_gate
from founderbench.submission_manifest import build_manifest as build_submission_manifest, validate_manifest as validate_submission_manifest
from founderbench.submission_schema import build_schema as build_submission_schema, validate_schema as validate_submission_schema
from founderbench.task_cards import build_cards as build_task_cards, validate_cards as validate_task_cards
from founderbench.task_coverage import build_coverage, validate_coverage
from founderbench.task_feasibility_audit import build_audit as build_task_feasibility_audit, validate_audit as validate_task_feasibility_audit
from founderbench.task_provenance import build_provenance as build_task_provenance, validate_provenance as validate_task_provenance
from founderbench.task_revision_ledger import build_ledger as build_task_revision_ledger, validate_ledger as validate_task_revision_ledger
from founderbench.task_runner import run_suite, run_task
from founderbench.tasks import get_task
from founderbench.validity_report import build_report as build_validity_report, validate_report as validate_validity_report


class MissingActionsPolicy:
    def act(self, observation):
        raise ProviderResponseError("missing_actions", "synthetic missing actions")


class FounderBenchTests(unittest.TestCase):
    def test_environment_runs_one_step(self):
        env = FounderBenchEnv(seed=1, weeks=2)
        obs = env.reset()
        result = env.step([Action("research_market", market_id=obs.markets[0]["market_id"], budget=120)])
        self.assertGreater(result.cost, 0)
        self.assertEqual(env.state.week, 2)

    def test_heuristic_beats_bankruptcy_smoke(self):
        result = run("heuristic", seed=7, weeks=12)
        self.assertFalse(result["summary"]["bankrupt"])
        self.assertGreater(result["summary"]["score"], 0)

    def test_heuristic_beats_conservative_on_smoke_seeds(self):
        heuristic_scores = [run("heuristic", seed=seed, weeks=52)["summary"]["score"] for seed in range(3)]
        conservative_scores = [run("conservative", seed=seed, weeks=52)["summary"]["score"] for seed in range(3)]
        self.assertGreater(sum(heuristic_scores) / len(heuristic_scores), sum(conservative_scores) / len(conservative_scores))

    def test_fixed_task_suite_runs(self):
        result = run_suite("heuristic")
        self.assertEqual(result["tasks"], 50)
        self.assertGreater(result["average_task_score"], 0)
        self.assertIn("provider_total_tokens", result["diagnostics"])

    def test_redacts_provider_keys(self):
        text = "deepseek sk-testsynthetic1234567890 gemini AQ.synthetic_test_key_1234567890"
        redacted = redact_text(text)
        self.assertNotIn("sk-testsynthetic1234567890", redacted)
        self.assertNotIn("AQ.synthetic_test_key", redacted)
        self.assertIn("[REDACTED_API_KEY]", redacted)

    def test_bootstrap_ci_is_deterministic_and_ordered(self):
        low, high = bootstrap_mean_ci([0.0, 50.0, 100.0], iterations=50, seed=1)
        self.assertLessEqual(low, high)
        self.assertEqual((low, high), bootstrap_mean_ci([0.0, 50.0, 100.0], iterations=50, seed=1))

    def test_release_outputs_validate(self):
        self.assertEqual(validate_outputs(), [])

    def test_holdout_blueprint_and_fingerprints(self):
        blueprint = public_blueprint()
        self.assertEqual(validate_blueprint(blueprint), [])
        self.assertEqual(blueprint["private_holdout_size"], 20)
        first = generate_private_fingerprint_manifest("synthetic-secret")
        second = generate_private_fingerprint_manifest("synthetic-secret")
        self.assertEqual(validate_fingerprint_manifest(first), [])
        self.assertEqual(first, second)
        self.assertEqual(first["task_count"], 20)
        self.assertNotIn("synthetic-secret", str(first))
        self.assertIn("public_report_fields", evaluator_protocol())

    def test_private_holdout_evaluator_runs_aggregate_only_report(self):
        secret = "synthetic-private-holdout-secret"
        tasks = generate_private_tasks(secret)
        self.assertEqual(len(tasks), 20)
        self.assertEqual(len({task.task_id for task in tasks}), 20)
        self.assertTrue(all(task.task_id.startswith("PRIV-") for task in tasks))
        payload = run_private_holdout("conservative", secret)
        self.assertEqual(validate_private_report(payload), [])
        self.assertEqual(payload["private_tasks"], 20)
        self.assertFalse(payload["secret_values_recorded"])
        self.assertNotIn(secret, str(payload))
        self.assertNotIn("private_results", payload)

    def test_private_holdout_smoke_report_is_aggregate_only_and_not_official(self):
        payload = build_holdout_smoke_report()
        self.assertEqual(validate_holdout_smoke_report(payload), [])
        self.assertEqual(payload["status"], "smoke_test_only_not_official_holdout")
        self.assertEqual(payload["summary"]["private_tasks"], 20)
        self.assertFalse(payload["summary"]["contains_raw_private_results"])
        self.assertIn("official private leaderboard", payload["official_claim_guardrail"])
        self.assertNotIn("private_results", payload["private_report"])

    def test_contamination_leakage_audit_keeps_public_split_honest(self):
        payload = build_contamination_leakage_audit()
        self.assertEqual(validate_contamination_leakage_audit(payload), [])
        self.assertEqual(payload["status"], "public_suite_visible_private_holdout_not_executed")
        self.assertEqual(payload["summary"]["public_tasks"], 50)
        self.assertEqual(payload["summary"]["public_dev"], 30)
        self.assertEqual(payload["summary"]["public_test"], 20)
        self.assertFalse(payload["summary"]["official_private_leaderboard"])
        self.assertFalse(payload["summary"]["contamination_free_claim_supported"])
        public_test = next(row for row in payload["split_controls"] if row["split"] == "public_test")
        self.assertFalse(public_test["hidden"])
        guardrails = " ".join(payload["claim_guardrails"])
        self.assertIn("Do not claim", guardrails)
        self.assertIn("contamination", guardrails)

    def test_provider_response_taxonomy(self):
        with self.assertRaises(ProviderResponseError) as invalid_json:
            parse_provider_response("not json")
        self.assertEqual(invalid_json.exception.category, "invalid_json")

        with self.assertRaises(ProviderResponseError) as missing_actions:
            parse_provider_response('{"rationale": "ok"}')
        self.assertEqual(missing_actions.exception.category, "missing_actions")

        with self.assertRaises(ProviderResponseError) as invalid_numeric:
            parse_provider_response('{"actions": [{"type": "do_nothing", "budget": "bad"}]}')
        self.assertEqual(invalid_numeric.exception.category, "invalid_numeric_field")
        self.assertEqual(classify_provider_exception(invalid_numeric.exception), "invalid_numeric_field")

    def test_runner_counts_provider_error_categories(self):
        result = run_task(get_task("FND-001"), MissingActionsPolicy())
        self.assertGreater(result["diagnostics"]["provider_errors"], 0)
        self.assertIn("missing_actions", result["diagnostics"]["provider_error_categories"])

    def test_provider_contract_audit_covers_parser_and_diagnostics(self):
        payload = build_provider_contract_audit()
        self.assertEqual(validate_provider_contract_audit(payload), [])
        self.assertEqual(payload["status"], "contract_validated_no_provider_results_claimed")
        self.assertFalse(payload["summary"]["llm_baseline_evidence"])
        self.assertEqual(payload["summary"]["parser_cases"], payload["summary"]["parser_cases_passed"])
        observed = {row["observed"] for row in payload["parser_cases"]}
        self.assertIn("invalid_json", observed)
        self.assertIn("missing_actions", observed)
        self.assertIn("invalid_numeric_field", observed)
        self.assertTrue(all(row["passed"] for row in payload["simulator_checks"]))

    def test_submission_validator_accepts_complete_suite(self):
        result = run_suite("conservative")
        problems = validate_run(result)
        self.assertEqual(problems, [])

    def test_resumable_runner_summary_matches_submission_contract(self):
        result = run_suite("conservative")
        payload = summarize_resumable_results(result["results"], "conservative", seed=2)
        self.assertEqual(validate_run(payload), [])
        self.assertEqual(payload["benchmark_version"], "0.3.0")
        self.assertEqual(payload["run_seed"], 2)
        self.assertEqual(set(payload["splits"]), {"public_dev", "public_test"})
        self.assertIn("provider_prompt_tokens", payload["diagnostics"])
        self.assertIn("provider_error_categories", payload["diagnostics"])

    def test_submission_validator_rejects_partial_suite(self):
        result = run_suite("conservative", task_ids=["FND-001"])
        problems = validate_run(result)
        self.assertTrue(any("expected tasks=50" in problem for problem in problems))
        self.assertTrue(any("missing task ids" in problem for problem in problems))

    def test_submission_schema_matches_validator_contract(self):
        payload = build_submission_schema()
        self.assertEqual(validate_submission_schema(payload), [])
        self.assertEqual(payload["version"], "0.3.0")
        self.assertEqual(len(payload["required_task_ids"]), 50)
        self.assertIn("provider_error_categories", payload["required_diagnostics"])
        self.assertIn("results", payload["$defs"]["run"]["required"])
        self.assertIn("founderbench.submission", payload["validator_command"])

    def test_submission_bundle_combines_repeated_runs(self):
        first = run_suite("conservative")
        first["run_seed"] = 0
        second = run_suite("heuristic")
        second["run_seed"] = 1
        payload = bundle_payload([first, second], ["seed0.json", "seed1.json"])
        self.assertEqual(validate_bundle(payload), [])
        self.assertEqual(payload["version"], "0.3.0")
        self.assertEqual(len(payload["runs"]), 2)
        self.assertEqual(payload["input_files"], ["seed0.json", "seed1.json"])

    def test_submission_bundle_rejects_duplicate_policy_seed(self):
        first = run_suite("conservative")
        first["run_seed"] = 0
        second = run_suite("conservative")
        second["run_seed"] = 0
        problems = validate_bundle(bundle_payload([first, second]))
        self.assertTrue(any("Duplicate run identity" in problem for problem in problems))

    def test_submission_bundle_protocol_documents_repeat_workflow(self):
        payload = build_submission_bundle_protocol()
        self.assertEqual(validate_submission_bundle_protocol(payload), [])
        self.assertIn("no duplicate policy/run_seed pairs", payload["validation_checks"])
        self.assertTrue(any("submission_bundle" in command for command in payload["example_commands"]))

    def test_ablation_tables_cover_policy_ladder(self):
        runs = [run_suite(policy) for policy in ["random", "conservative", "heuristic", "task_heuristic"]]
        rows = ablation_rows(runs)
        self.assertEqual([row[0] for row in rows], ["random", "conservative", "heuristic", "task_heuristic"])
        self.assertEqual(rows[0][4], "n/a")
        self.assertEqual(len(family_gain_rows(runs)), 10)

    def test_action_ablation_quantifies_expanded_action_space(self):
        payload = build_action_ablation_report()
        self.assertEqual(validate_action_ablation_report(payload), [])
        self.assertEqual(payload["summary"]["tasks_per_ablation"], 50)
        self.assertGreaterEqual(payload["summary"]["ablations"], 6)
        self.assertGreater(payload["summary"]["largest_score_drop"], 0)
        row_ids = {row["ablation_id"] for row in payload["rows"]}
        self.assertIn("no_discovery", row_ids)
        self.assertIn("no_pivot", row_ids)

    def test_difficulty_calibration_validates_public_suite_spread(self):
        payload = build_difficulty_report()
        self.assertEqual(validate_difficulty_report(payload), [])
        self.assertEqual(payload["summary"]["tasks"], 50)
        self.assertEqual(payload["summary"]["policies"], 4)
        self.assertGreater(payload["summary"]["tasks_not_solved_by_task_heuristic"], 0)
        self.assertLess(payload["summary"]["saturated_tasks"], 50)
        self.assertEqual(len(payload["family_summary"]), 10)
        self.assertEqual({row["split"] for row in payload["split_summary"]}, {"public_dev", "public_test"})

    def test_qualitative_example_selection_and_traces(self):
        runs = [run_suite(policy) for policy in ["random", "conservative", "heuristic", "task_heuristic"]]
        selections = select_examples(runs)
        self.assertEqual(len(selections), 4)
        self.assertEqual({selection["policy"] for selection in selections}, {"random", "heuristic", "task_heuristic"})

    def test_reference_bibtex_has_expected_keys(self):
        text = bibtex_text()
        self.assertEqual(validate_bibtex(text), [])
        for entry in REFERENCE_ENTRIES:
            self.assertIn("{" + entry["key"] + ",", text)

    def test_repeated_run_payload_validates(self):
        payload = run_repeated("random", [0, 1])
        self.assertEqual(validate_repeated(payload), [])
        self.assertEqual(len(payload["runs"]), 2)
        self.assertEqual({run["run_seed"] for run in payload["runs"]}, {0, 1})
        self.assertEqual(len(interval_rows(payload)), 2)

    def test_publication_audit_tracks_open_blockers(self):
        payload = audit()
        self.assertGreaterEqual(payload["summary"]["complete"], 1)
        blockers = {item["id"]: item for item in payload["items"] if item["status"] != "complete"}
        self.assertIn("hosted_llm_baselines", blockers)
        self.assertIn("final_license_metadata", blockers)

    def test_local_model_protocol_config_validates(self):
        payload = local_model_protocol({"base_url": "http://localhost:8000/v1", "model": "local-test-model", "api_key_configured": False, "timeout_s": 5})
        self.assertEqual(validate_local_config(payload["config"]), [])
        self.assertIn("reporting_requirements", payload)
        self.assertTrue(any("resumable_runner" in command for command in payload["commands"]))

    def test_provider_readiness_does_not_expose_secret_values(self):
        payload = readiness_matrix()
        text = str(payload)
        self.assertIn("providers", payload)
        self.assertNotIn("sk-", text)
        self.assertNotIn("AQ.", text)
        self.assertTrue(all("run_command" in row for row in payload["providers"]))

    def test_cost_accounting_protocol_documents_formula(self):
        payload = build_cost_accounting_protocol()
        self.assertEqual(validate_cost_accounting_protocol(payload), [])
        self.assertIn("MODEL_INPUT_COST_PER_MILLION", payload["price_environment_variables"])
        self.assertIn("provider_total_tokens", payload["usage_fields"])
        self.assertEqual(estimate_cost(100_000, 25_000, 0.10, 0.40), 0.02)
        self.assertFalse("sk-" in str(payload))

    def test_baseline_execution_plan_covers_required_llm_runs(self):
        payload = build_baseline_execution_plan()
        self.assertEqual(validate_baseline_execution_plan(payload), [])
        self.assertEqual(payload["scope"]["task_count"], 50)
        self.assertGreaterEqual(payload["summary"]["required_runs"], 4)
        self.assertGreaterEqual(payload["summary"]["hosted_runs"], 8)
        self.assertGreaterEqual(payload["summary"]["local_open_source_runs"], 1)
        policies = {row["policy"] for row in payload["runs"]}
        self.assertIn("openai", policies)
        self.assertIn("deepseek", policies)
        self.assertIn("kimi", policies)
        self.assertIn("qwen", policies)
        self.assertIn("llm", policies)
        removed_policy = "deepseek" + "_sc"
        self.assertNotIn(removed_policy, policies)
        self.assertTrue(all("founderbench.submission" in row["validation_command"] for row in payload["runs"]))

    def test_experiment_runbook_keeps_missing_llm_runs_executable_but_unexecuted(self):
        payload = build_experiment_runbook()
        self.assertEqual(validate_experiment_runbook(payload), [])
        self.assertEqual(payload["material_passport"]["verification_status"], "planned_not_executed")
        self.assertGreaterEqual(payload["summary"]["providers"], 5)
        phase_ids = {phase["id"] for phase in payload["phases"]}
        self.assertIn("single_required_runs", phase_ids)
        self.assertIn("postprocess_and_claim_gate", phase_ids)
        self.assertTrue(any("API keys" in gate for gate in payload["quality_gates"]))
        self.assertTrue(any(rule["claim"] == "hosted_llm_comparison" for rule in payload["claim_unlock_rules"]))

    def test_provider_run_status_tracks_planned_and_excluded_evidence(self):
        payload = build_provider_run_status()
        self.assertEqual(validate_provider_run_status(payload), [])
        self.assertGreaterEqual(payload["summary"]["planned_runs"], 11)
        self.assertGreaterEqual(payload["summary"]["required_runs"], 7)
        self.assertFalse(payload["summary"]["ready_for_llm_claims"])
        ids = {row["id"] for row in payload["planned_runs"]}
        self.assertIn("openai_single", ids)
        self.assertIn("deepseek_single", ids)
        self.assertIn("kimi_single", ids)
        self.assertIn("qwen_single", ids)
        self.assertIn("local_open_model_single", ids)
        self.assertTrue(all(row["status"] in {"missing", "invalid", "valid"} for row in payload["planned_runs"]))

    def test_provider_comparability_audit_keeps_missing_runs_claim_blocked(self):
        payload = build_provider_comparability_audit()
        self.assertEqual(validate_provider_comparability_audit(payload), [])
        self.assertEqual(payload["status"], "protocol_comparability_ready_runs_missing")
        self.assertGreaterEqual(payload["summary"]["planned_runs"], 11)
        self.assertGreaterEqual(payload["summary"]["main_claim_comparable_required_runs"], 7)
        self.assertFalse(payload["summary"]["ready_for_hosted_llm_comparison"])
        removed_policy = "deepseek" + "_sc"
        self.assertFalse(any(row["policy"] == removed_policy for row in payload["run_rows"]))

    def test_prompt_protocol_covers_provider_contract_without_secrets(self):
        payload = build_prompt_protocol()
        self.assertEqual(validate_prompt_protocol(payload), [])
        self.assertEqual(payload["task_count"], 50)
        self.assertEqual(len(payload["action_types"]), 13)
        self.assertEqual(payload["response_contract"]["required_keys"], ["rationale", "actions"])
        policies = {row["policy"] for row in payload["provider_message_wrappers"]}
        self.assertTrue({"openai", "deepseek", "anthropic", "gemini", "kimi", "qwen", "llm"}.issubset(policies))
        removed_policy = "deepseek" + "_sc"
        self.assertNotIn(removed_policy, policies)
        self.assertNotIn("api03", str(payload))
        self.assertNotIn("AQ.", str(payload))

    def test_reviewer_index_maps_submission_artifacts(self):
        payload = build_index()
        paths = {entry["path"] for entry in payload["artifacts"]}
        self.assertIn("outputs/founderbench-task-manifest.json", paths)
        self.assertIn("outputs/founderbench-prompt-protocol.md", paths)
        self.assertIn("outputs/founderbench-experiment-matrix.md", paths)
        self.assertIn("outputs/founderbench-experiment-runbook.md", paths)
        self.assertIn("outputs/founderbench-task-feasibility-audit.md", paths)
        self.assertIn("outputs/founderbench-completion-audit.md", paths)
        self.assertIn("outputs/founderbench-submission-manifest.md", paths)
        self.assertIn("outputs/founderbench-paper-evidence-map.md", paths)
        self.assertIn("outputs/founderbench-leaderboard-stability.md", paths)
        self.assertIn("outputs/founderbench-power-analysis.md", paths)
        self.assertIn("outputs/founderbench-scoring-consistency-audit.md", paths)
        self.assertIn("outputs/founderbench-responsible-use.md", paths)
        self.assertIn("outputs/founderbench-result-integrity-audit.md", paths)
        self.assertIn("outputs/founderbench-citation-audit.md", paths)
        self.assertIn("outputs/founderbench-private-holdout-smoke.md", paths)
        self.assertIn("outputs/founderbench-reviewer-risk-audit.md", paths)
        self.assertIn("outputs/founderbench-failure-mode-audit.md", paths)
        self.assertIn("work/founderbench/LICENSE.template", paths)
        self.assertIn("work/founderbench/CITATION.cff.template", paths)
        self.assertIn("outputs/founderbench-publication-audit.md", paths)
        self.assertIn("python -m founderbench.release validate", str(payload["commands"]))
        self.assertGreaterEqual(payload["summary"]["artifact_count"], 20)
        self.assertGreaterEqual(payload["summary"]["open_blockers"], 1)

    def test_reviewer_risk_audit_names_open_external_and_claim_risks(self):
        payload = build_reviewer_risk_audit()
        self.assertEqual(validate_reviewer_risk_audit(payload), [])
        risks = {row["id"]: row for row in payload["risks"]}
        self.assertIn("missing_llm_baselines", risks)
        self.assertIn("overclaiming_real_world_success", risks)
        self.assertEqual(risks["missing_llm_baselines"]["status"], "open_external")
        self.assertEqual(risks["overclaiming_real_world_success"]["status"], "mitigated_by_claim_guardrail")
        self.assertGreaterEqual(payload["summary"]["critical"], 1)
        self.assertGreaterEqual(payload["summary"]["open_or_external"], 1)

    def test_failure_mode_audit_keeps_integrity_risks_visible(self):
        payload = build_failure_mode_audit()
        self.assertEqual(validate_failure_mode_audit(payload), [])
        checks = {row["id"]: row for row in payload["checks"]}
        self.assertIn("implementation_bug_passing_self_review", checks)
        self.assertIn("hallucinated_experimental_result", checks)
        self.assertIn("methodology_fabrication", checks)
        self.assertIn("frame_lock", checks)
        self.assertEqual(payload["summary"]["modes"], 7)
        self.assertGreaterEqual(payload["summary"]["warnings_or_blockers"], 1)
        self.assertIn("blocks_stronger_llm_claims", {row["gate_effect"] for row in payload["checks"]})

    def test_reviewer_smoke_report_checks_core_artifact_path(self):
        payload = build_reviewer_smoke_report()
        self.assertEqual(validate_reviewer_smoke_report(payload), [])
        self.assertEqual(payload["status"], "pass")
        check_ids = {row["id"] for row in payload["checks"]}
        self.assertIn("single_task_execution", check_ids)
        self.assertIn("baseline_submission_validation", check_ids)
        self.assertTrue(any("release validate" in command for command in payload["full_validation_commands"]))

    def test_release_bundle_integrity_report_verifies_checksums(self):
        with tempfile.TemporaryDirectory() as tmp:
            bundle = Path(tmp)
            sample = bundle / "code" / "sample.txt"
            sample.parent.mkdir(parents=True)
            sample.write_text("synthetic bundle file", encoding="utf-8")
            import hashlib

            digest = hashlib.sha256(sample.read_bytes()).hexdigest()
            (bundle / "SHA256SUMS.json").write_text(
                json.dumps([{"path": "code/sample.txt", "sha256": digest, "bytes": sample.stat().st_size}], indent=2),
                encoding="utf-8",
            )
            payload = build_bundle_integrity_report(bundle)
        self.assertEqual(validate_bundle_integrity_report(payload), [])
        self.assertEqual(payload["status"], "pass")
        self.assertEqual(payload["summary"]["missing"], 0)
        self.assertEqual(payload["summary"]["mismatched"], 0)
        self.assertEqual(payload["summary"]["extra_files"], 0)

    def test_release_checksum_manifest_excludes_post_manifest_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            bundle = Path(tmp)
            (bundle / "code").mkdir()
            (bundle / "code" / "sample.txt").write_text("synthetic bundle file", encoding="utf-8")
            (bundle / "SHA256SUMS.json").write_text("[]", encoding="utf-8")
            (bundle / "BUNDLE-INTEGRITY.json").write_text("{}", encoding="utf-8")
            (bundle / "BUNDLE-INTEGRITY.md").write_text("# Integrity", encoding="utf-8")
            write_checksum_manifest(bundle)
            manifest = json.loads((bundle / "SHA256SUMS.json").read_text(encoding="utf-8"))
        paths = {row["path"] for row in manifest}
        self.assertEqual(paths, {"code/sample.txt"})

    def test_experiment_matrix_tracks_required_model_evidence(self):
        payload = build_matrix()
        statuses = {row["id"]: row["status"] for row in payload["experiments"]}
        self.assertEqual(statuses["deterministic_rule_baselines"], "complete")
        self.assertEqual(statuses["action_space_ablation"], "complete")
        self.assertIn(statuses["deepseek_hosted_baseline"], {"missing", "partial", "complete"})
        self.assertGreaterEqual(payload["summary"]["experiments"], 10)
        self.assertGreaterEqual(payload["summary"]["required_missing"], 1)
        self.assertIn("current release", str(payload))

    def test_paper_tables_exclude_missing_provider_runs(self):
        payload = build_tables()
        self.assertEqual(payload["summary"]["deterministic_runs"], 4)
        self.assertEqual(payload["summary"]["valid_provider_runs"], 0)
        self.assertEqual(payload["summary"]["valid_provider_policies"], 0)
        self.assertEqual(payload["summary"]["valid_repeated_provider_bundles"], 0)
        self.assertEqual(len(payload["all_valid_policy_rows"]), 4)
        self.assertTrue(all(row["status"] in {"missing", "invalid", "valid"} for row in payload["provider_status"]))
        self.assertTrue(any(row["id"] == "deepseek_hosted_baseline" for row in payload["provider_status"]))

    def test_provider_status_accepts_valid_repeat_bundle(self):
        output = OUTPUTS / "tmp-test-provider-repeats.json"
        report = OUTPUTS / "tmp-test-provider-repeats-submission-report.md"
        try:
            first = run_suite("conservative")
            first["policy"] = "synthetic_provider"
            first["run_seed"] = 0
            second = run_suite("heuristic")
            second["policy"] = "synthetic_provider"
            second["run_seed"] = 1
            output.write_text(
                json.dumps(
                    {
                        "benchmark": "FounderBench",
                        "version": "0.3.0",
                        "runs": [first, second],
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )
            write_submission_report(output, report)
            row = provider_status(
                {
                    "id": "synthetic_provider",
                    "policy": "synthetic_provider",
                    "path": "outputs/tmp-test-provider-single.json",
                    "report": "outputs/tmp-test-provider-single-submission-report.md",
                    "repeat_bundle_path": "outputs/tmp-test-provider-repeats.json",
                    "repeat_bundle_report": "outputs/tmp-test-provider-repeats-submission-report.md",
                    "family": "hosted_llm",
                }
            )
            self.assertEqual(row["status"], "valid")
            self.assertEqual(row["evidence_kind"], "repeat_bundle")
            self.assertEqual(row["runs"], 2)
            self.assertEqual(row["repeat_summary"]["run_seeds"], [0, 1])
        finally:
            for path in [output, report]:
                if path.exists():
                    path.unlink()

    def test_paper_figure_data_covers_main_result_views(self):
        payload = build_figure_data()
        self.assertEqual(validate_figure_data(payload), [])
        ids = {figure["id"] for figure in payload["figures"]}
        self.assertIn("leaderboard_bar", ids)
        self.assertIn("family_heatmap", ids)
        self.assertIn("action_ablation_drop", ids)
        self.assertGreaterEqual(payload["summary"]["leaderboard_policies"], 4)
        self.assertGreaterEqual(payload["summary"]["family_heatmap_cells"], 40)

    def test_paper_evidence_map_keeps_llm_results_excluded_until_evidence_exists(self):
        payload = build_paper_evidence_map()
        self.assertEqual(validate_paper_evidence_map(payload), [])
        self.assertEqual(payload["summary"]["incomplete"], 0)
        statuses = {row["section"]: row["status"] for row in payload["sections"]}
        self.assertEqual(statuses["Hosted and Local LLM Results"], "excluded_until_evidence")
        metrics = [row for row in payload["sections"] if row["section"] == "Metrics"][0]
        metric_paths = {entry["path"] for entry in metrics["evidence"]}
        self.assertIn("outputs/founderbench-scoring-consistency-audit.md", metric_paths)
        self.assertIn("outputs/founderbench-power-analysis.md", metric_paths)
        intro = [row for row in payload["sections"] if row["section"] == "Abstract and Introduction"][0]
        intro_paths = {entry["path"] for entry in intro["evidence"]}
        self.assertIn("outputs/founderbench-responsible-use.md", intro_paths)
        baselines = [row for row in payload["sections"] if row["section"] == "Baselines"][0]
        baseline_paths = {entry["path"] for entry in baselines["evidence"]}
        self.assertIn("outputs/founderbench-leaderboard-stability.md", baseline_paths)
        self.assertIn("outputs/founderbench-result-integrity-audit.md", baseline_paths)
        self.assertGreaterEqual(payload["summary"]["supported"], 5)

    def test_paper_claim_lint_blocks_overclaiming_text(self):
        payload = build_paper_claim_lint()
        self.assertEqual(validate_paper_claim_lint(payload), [])
        self.assertEqual(payload["summary"]["forbidden_hits"], 0)
        self.assertEqual(payload["summary"]["missing_required_disclosures"], 0)
        target_ids = {target["id"] for target in payload["targets"]}
        self.assertIn("paper_draft", target_ids)
        self.assertIn("benchmark_card", target_ids)

    def test_model_comparison_keeps_missing_provider_claims_explicit(self):
        payload = build_model_comparison_report()
        self.assertEqual(validate_model_comparison_report(payload), [])
        self.assertEqual(payload["summary"]["deterministic_runs"], 4)
        self.assertEqual(payload["summary"]["valid_provider_runs"], 0)
        self.assertFalse(payload["summary"]["hosted_llm_claims_ready"])
        self.assertEqual(len(payload["leaderboard_rows"]), 4)
        self.assertGreaterEqual(payload["summary"]["paired_comparisons"], 3)
        self.assertGreaterEqual(len(payload["provider_status"]), 11)

    def test_model_result_cards_keep_provider_claims_excluded_until_validated(self):
        payload = build_model_result_cards()
        self.assertEqual(validate_model_result_cards(payload), [])
        self.assertEqual(payload["summary"]["deterministic_cards"], 4)
        self.assertGreaterEqual(payload["summary"]["provider_candidate_cards"], 11)
        self.assertEqual(payload["summary"]["valid_provider_cards"], 0)
        self.assertFalse(payload["summary"]["hosted_llm_claims_ready"])
        self.assertTrue(all(card["status"] == "valid" for card in payload["deterministic_cards"]))
        self.assertTrue(all(card["claim_eligibility"] == "excluded_until_validated" for card in payload["provider_cards"]))

    def test_task_coverage_validates_public_suite_balance(self):
        payload = build_coverage()
        self.assertEqual(validate_coverage(payload), [])
        self.assertEqual(payload["task_count"], 50)
        self.assertEqual(payload["summary"]["families"], 10)
        self.assertEqual(payload["summary"]["public_dev_tasks"], 30)
        self.assertEqual(payload["summary"]["public_test_tasks"], 20)
        self.assertEqual(payload["summary"]["action_types_available"], 13)

    def test_task_provenance_documents_template_curation(self):
        payload = build_task_provenance()
        self.assertEqual(validate_task_provenance(payload), [])
        self.assertEqual(payload["summary"]["tasks"], 50)
        self.assertEqual(payload["summary"]["templates"], 10)
        self.assertFalse(payload["summary"]["real_world_data_used"])
        self.assertFalse(payload["summary"]["human_subject_data_used"])
        self.assertTrue(payload["summary"]["all_templates_have_five_tasks"])

    def test_task_cards_document_all_public_tasks(self):
        payload = build_task_cards()
        self.assertEqual(validate_task_cards(payload), [])
        self.assertEqual(payload["summary"]["tasks"], 50)
        self.assertEqual(payload["summary"]["families"], 10)
        self.assertEqual(payload["summary"]["public_dev"], 30)
        self.assertEqual(payload["summary"]["public_test"], 20)
        self.assertTrue(all(card["initial_state"]["markets_visible"] >= 1 for card in payload["cards"]))
        self.assertTrue(all(len(card["scoring_metrics"]) >= 3 for card in payload["cards"]))

    def test_action_semantics_document_all_structured_actions(self):
        payload = build_action_catalog()
        self.assertEqual(validate_action_catalog(payload), [])
        self.assertEqual(payload["summary"]["actions"], 13)
        action_types = {row["type"] for row in payload["actions"]}
        self.assertIn("raise_funding", action_types)
        self.assertIn("pivot_market", action_types)
        self.assertTrue(all(row["primary_effects"] for row in payload["actions"]))

    def test_market_catalog_documents_fixed_market_set(self):
        payload = build_market_catalog()
        self.assertEqual(validate_market_catalog(payload), [])
        self.assertEqual(payload["summary"]["markets"], 8)
        market_ids = {row["market_id"] for row in payload["markets"]}
        self.assertIn("saas_churn", market_ids)
        self.assertIn("support_triage", market_ids)
        self.assertGreaterEqual(len(payload["observation_rules"]), 4)
        self.assertGreaterEqual(len(payload["settlement_rules"]), 4)

    def test_score_rubric_validates_family_weights(self):
        payload = build_rubric()
        self.assertEqual(validate_rubric(payload), [])
        self.assertEqual(payload["score_bounds"], {"min": 0, "max": 100})
        self.assertEqual(payload["pass_threshold"], 70)
        self.assertEqual(len(payload["families"]), 10)
        self.assertTrue(all(row["positive_weight_total"] == 100.0 for row in payload["families"]))

    def test_scoring_consistency_audit_checks_all_raw_score_objects(self):
        payload = build_scoring_consistency_audit()
        self.assertEqual(validate_scoring_consistency_audit(payload), [])
        self.assertEqual(payload["summary"]["task_results_checked"], 200)
        self.assertEqual(payload["summary"]["score_rows_with_problems"], 0)
        self.assertTrue(payload["summary"]["all_family_counts_valid"])
        self.assertTrue(payload["summary"]["all_split_counts_valid"])
        self.assertEqual(payload["score_contract"]["pass_threshold"], 70)
        self.assertEqual(payload["failed_rows"], [])

    def test_metric_sensitivity_compares_normalized_alternatives(self):
        payload = build_metric_sensitivity_report()
        self.assertEqual(validate_metric_sensitivity_report(payload), [])
        self.assertEqual(payload["primary_metric"], "average_task_score")
        metrics = {row["metric"] for row in payload["metric_rows"]}
        self.assertIn("task_normalized_business_score", metrics)
        self.assertIn("revenue_efficiency", metrics)
        self.assertGreaterEqual(payload["summary"]["metrics"], 6)
        self.assertEqual(payload["summary"]["policies"], 4)

    def test_statistical_protocol_prespecifies_model_comparisons(self):
        payload = build_statistical_protocol()
        self.assertEqual(validate_statistical_protocol(payload), [])
        self.assertEqual(payload["primary_endpoint"]["metric"], "average_task_score")
        self.assertEqual(payload["single_run_comparison"]["paired_unit"], "task id")
        self.assertIn("Holm-Bonferroni", payload["multiple_comparisons"]["adjustment"])
        self.assertGreaterEqual(payload["repeated_sampling_comparison"]["minimum_repeats_recommended"], 3)

    def test_paired_statistics_cover_matched_task_comparisons(self):
        payload = build_paired_statistics_report()
        self.assertEqual(validate_paired_statistics_report(payload), [])
        self.assertGreaterEqual(payload["summary"]["comparisons"], 3)
        self.assertIn("Holm-Bonferroni", payload["method"]["multiple_comparison_adjustment"])
        self.assertIn("significant_after_holm_0_05", payload["summary"])
        self.assertTrue(all(row["tasks"] == 50 for row in payload["comparisons"]))
        self.assertTrue(all(0 <= row["paired_permutation_p"] <= 1 for row in payload["comparisons"]))
        self.assertTrue(all(0 <= row["holm_adjusted_p"] <= 1 for row in payload["comparisons"]))
        self.assertTrue(all(row["holm_adjusted_p"] >= row["paired_permutation_p"] for row in payload["comparisons"]))
        self.assertTrue(all(row["significant_after_holm_0_05"] == (row["holm_adjusted_p"] < 0.05) for row in payload["comparisons"]))
        self.assertTrue(all(row["task_wins"] + row["task_losses"] + row["task_ties"] == 50 for row in payload["comparisons"]))

    def test_result_integrity_audit_recomputes_reported_baseline_rows(self):
        payload = build_result_integrity_audit()
        self.assertEqual(validate_result_integrity_audit(payload), [])
        self.assertEqual(payload["summary"]["raw_runs"], 4)
        self.assertEqual(payload["summary"]["policies_checked"], 4)
        self.assertEqual(payload["summary"]["policies_failed"], 0)
        self.assertTrue(payload["summary"]["all_integrity_checks_passed"])
        self.assertTrue(all(row["raw_tasks"] == 50 for row in payload["policy_checks"]))
        self.assertTrue(all(row["status"] == "pass" for row in payload["policy_checks"]))

    def test_power_analysis_quantifies_public_suite_resolution(self):
        payload = build_power_analysis()
        self.assertEqual(validate_power_analysis(payload), [])
        self.assertEqual(payload["summary"]["public_tasks"], 50)
        self.assertGreater(payload["summary"]["minimum_detectable_score_gap_50_tasks"], 0)
        task_counts = {row["task_episodes"] for row in payload["mde_by_task_count"]}
        self.assertIn(50, task_counts)
        self.assertGreaterEqual(payload["summary"]["paired_gap_observations"], 100)
        guardrails = " ".join(payload["claim_guardrails"]).lower()
        self.assertIn("repeated-run", guardrails)
        self.assertIn("private-holdout", guardrails)

    def test_reproducibility_manifest_tracks_hashes_without_secrets(self):
        payload = build_manifest()
        self.assertEqual(validate_manifest(payload), [])
        self.assertFalse(payload["summary"]["secret_values_recorded"])
        self.assertGreaterEqual(payload["summary"]["source_files_present"], 5)
        self.assertGreaterEqual(payload["summary"]["output_files_present"], 5)
        text = str(payload)
        self.assertNotIn("actual_secret", text)
        self.assertNotIn("api03", text)
        self.assertNotIn("AQ.", text)

    def test_environment_report_tracks_core_dependencies(self):
        payload = build_environment_report()
        self.assertEqual(validate_environment_report(payload), [])
        self.assertFalse(payload["summary"]["core_has_external_runtime_dependencies"])
        self.assertGreaterEqual(payload["summary"]["source_files"], 20)
        modules = {row["module"]: row["classification"] for row in payload["import_classification"]}
        self.assertEqual(modules["founderbench"], "local_package")

    def test_determinism_audit_replays_stable_baselines(self):
        payload = build_determinism_audit()
        self.assertEqual(validate_determinism_audit(payload), [])
        self.assertTrue(payload["summary"]["all_stable"])
        self.assertEqual(payload["summary"]["policies"], 4)
        self.assertTrue(all(row["tasks"] == 50 for row in payload["rows"]))
        self.assertTrue(all(row["stable_match"] for row in payload["rows"]))

    def test_simulator_invariant_audit_checks_state_and_score_bounds(self):
        payload = build_simulator_invariant_audit()
        self.assertEqual(validate_simulator_invariant_audit(payload), [])
        self.assertEqual(payload["status"], "simulator_invariants_validated_for_stress_scenarios")
        self.assertEqual(payload["summary"]["scenarios"], payload["summary"]["scenarios_passed"])
        self.assertTrue(payload["summary"]["task_scores_bounded"])
        self.assertTrue(payload["summary"]["pass_flags_match_threshold"])
        self.assertIn("does not validate real-world startup dynamics", payload["claim_guardrail"])

    def test_validity_report_tracks_known_limitations(self):
        payload = build_validity_report()
        self.assertEqual(validate_validity_report(payload), [])
        categories = {row["category"] for row in payload["threats"]}
        self.assertIn("construct_validity", categories)
        self.assertIn("empirical_validity", categories)
        self.assertGreaterEqual(payload["summary"]["high_severity"], 2)
        self.assertTrue(all(row["current_mitigation"] for row in payload["threats"]))

    def test_claim_evidence_blocks_unsupported_llm_claims(self):
        payload = build_claim_report()
        self.assertEqual(validate_claim_report(payload), [])
        statuses = {row["id"]: row["status"] for row in payload["claims"]}
        self.assertEqual(statuses["expanded_50_task_suite"], "supported")
        self.assertEqual(statuses["hosted_llm_comparison"], "unsupported_currently")
        self.assertEqual(statuses["private_holdout_available"], "unsupported_currently")
        self.assertGreaterEqual(payload["summary"]["unsupported_currently"], 2)

    def test_benchmark_datasheet_discloses_composition_and_limits(self):
        payload = build_benchmark_datasheet()
        self.assertEqual(validate_benchmark_datasheet(payload), [])
        self.assertEqual(payload["artifact_summary"]["public_tasks"], 50)
        self.assertFalse(payload["artifact_summary"]["contains_real_company_data"])
        self.assertFalse(payload["artifact_summary"]["contains_human_subject_data"])
        self.assertFalse(payload["artifact_summary"]["public_test_hidden"])
        section_ids = {section["id"] for section in payload["sections"]}
        self.assertIn("composition", section_ids)
        self.assertIn("distribution_and_access", section_ids)
        self.assertIn("maintenance", section_ids)

    def test_responsible_use_statement_blocks_misuse_and_discloses_data_limits(self):
        payload = build_responsible_use_statement()
        self.assertEqual(validate_responsible_use_statement(payload), [])
        self.assertFalse(payload["summary"]["contains_real_company_data"])
        self.assertFalse(payload["summary"]["contains_human_subject_data"])
        self.assertFalse(payload["summary"]["permits_real_world_startup_success_claims"])
        unsupported = " ".join(payload["unsupported_uses"]).lower()
        self.assertIn("real company", unsupported)
        self.assertIn("business, investment", unsupported)
        disclosures = " ".join(payload["required_submission_disclosures"]).lower()
        self.assertIn("token usage", disclosures)
        self.assertIn("manually repaired", disclosures)

    def test_leaderboard_policy_keeps_public_private_and_invalid_rows_separate(self):
        payload = build_leaderboard_policy()
        self.assertEqual(validate_leaderboard_policy(payload), [])
        self.assertFalse(payload["summary"]["private_leaderboard_included"])
        self.assertTrue(payload["summary"]["public_tier_active"])
        tier_ids = {row["tier"] for row in payload["leaderboard_tiers"]}
        self.assertIn("public_open", tier_ids)
        self.assertIn("private_holdout", tier_ids)
        self.assertTrue(any("Do not rank missing or invalid provider submissions" in item for item in payload["claim_guardrails"]))
        self.assertTrue(any("manual repair" in item.lower() for item in payload["rejection_rules"]))

    def test_leaderboard_stability_audits_split_family_and_task_mix(self):
        payload = build_leaderboard_stability_audit()
        self.assertEqual(validate_leaderboard_stability_audit(payload), [])
        self.assertEqual(payload["summary"]["tasks"], 50)
        self.assertEqual(payload["summary"]["families_checked"], 10)
        self.assertEqual(len(payload["split_rows"]), 2)
        self.assertEqual(len(payload["bootstrap_rows"]), payload["summary"]["policies"])
        self.assertGreater(payload["summary"]["bootstrap_primary_leader_probability"], 0)
        self.assertTrue(all(row["tasks_used"] == 45 for row in payload["leave_one_family_rows"]))

    def test_paper_draft_mentions_claim_and_validity_guardrails(self):
        draft = (OUTPUTS / "founderbench-paper-draft.md").read_text(encoding="utf-8")
        self.assertIn("claim-evidence report", draft)
        self.assertIn("paper-claim linting", draft)
        self.assertIn("datasheet", draft)
        self.assertIn("responsible-use statement", draft)
        self.assertIn("leaderboard policy", draft)
        self.assertIn("validity report", draft)
        self.assertIn("task-card catalog", draft)
        self.assertIn("action-semantics catalog", draft)
        self.assertIn("market catalog", draft)
        self.assertIn("prompt-protocol", draft)
        self.assertIn("simulator-invariant audit", draft)
        self.assertIn("difficulty-calibration report", draft)
        self.assertIn("task-feasibility audit", draft)
        self.assertIn("11 tasks as needing external calibration", draft)
        self.assertIn("non-final license/citation templates", draft)
        self.assertIn("metric-sensitivity report", draft)
        self.assertIn("scoring-consistency audit", draft)
        self.assertIn("statistical-protocol report", draft)
        self.assertIn("power-analysis report", draft)
        self.assertIn("unified model-comparison report", draft)
        self.assertIn("paired-statistics report", draft)
        self.assertIn("leaderboard-stability audit", draft)
        self.assertIn("result-integrity audit", draft)
        self.assertIn("reviewer-risk audit", draft)
        self.assertIn("contamination-leakage audit", draft)
        self.assertIn("provider-contract audit", draft)
        self.assertIn("AI research failure-mode audit", draft)
        self.assertIn("citation-context audit", draft)
        self.assertIn("holdout smoke report", draft)
        self.assertIn("not an official hidden leaderboard", draft)
        self.assertIn("hallucinated experimental results", draft)
        self.assertIn("not yet a comparison of hosted LLM providers", draft)
        self.assertIn("The benchmark does not include private task definitions or hidden-suite scores", draft)

    def test_supplementary_checklist_mentions_integrity_audits(self):
        checklist = (OUTPUTS / "founderbench-supplementary-package-checklist.md").read_text(encoding="utf-8")
        self.assertIn("Datasheet-style disclosure", checklist)
        self.assertIn("Leaderboard/reporting policy", checklist)
        self.assertIn("Reviewer-risk audit generator", checklist)
        self.assertIn("AI research failure-mode audit generator", checklist)
        self.assertIn("Paper-claim lint generator", checklist)
        self.assertIn("Reviewer-risk audit report", checklist)
        self.assertIn("Simulator invariant audit report", checklist)
        self.assertIn("Contamination/leakage audit report", checklist)
        self.assertIn("Provider contract audit report", checklist)
        self.assertIn("Power/resolution analysis report", checklist)
        self.assertIn("Public-suite power/resolution analysis", checklist)
        self.assertIn("Scoring-consistency audit", checklist)
        self.assertIn("Leaderboard stability audit", checklist)
        self.assertIn("Raw-to-report result-integrity audit", checklist)
        self.assertIn("Responsible-use statement", checklist)
        self.assertIn("Paper-claim lint report", checklist)
        self.assertIn("AI research failure-mode audit report", checklist)
        self.assertIn("Citation-context audit report", checklist)
        self.assertIn("Local citation-context audit", checklist)
        self.assertIn("Aggregate-only private holdout smoke report", checklist)
        self.assertIn("not an official hidden-suite score", checklist)
        self.assertIn("Task feasibility/discrimination audit report", checklist)
        self.assertIn("deterministic-unsolved tasks", checklist)
        self.assertIn("Non-final LICENSE/CITATION template files", checklist)
        self.assertIn("not final release metadata", checklist)
        self.assertIn("claim-blocking integrity checks", checklist)

    def test_task_feasibility_audit_keeps_unsolved_tasks_visible(self):
        payload = build_task_feasibility_audit()
        self.assertEqual(validate_task_feasibility_audit(payload), [])
        self.assertEqual(payload["summary"]["tasks"], 50)
        self.assertEqual(payload["summary"]["families"], 10)
        self.assertGreater(payload["summary"]["baseline_solved_tasks"], 0)
        self.assertGreater(payload["summary"]["needs_external_calibration"], 0)
        self.assertGreater(payload["summary"]["high_discrimination_tasks"], 0)
        unsolved = [row for row in payload["task_rows"] if row["feasibility_status"] == "needs_external_calibration"]
        self.assertTrue(all(row["solved_by"] == 0 for row in unsolved))
        self.assertIn("hosted/local LLM", payload["claim_guardrail"])

    def test_task_revision_ledger_tracks_open_calibration_rows_without_fake_resolution(self):
        payload = build_task_revision_ledger()
        self.assertEqual(validate_task_revision_ledger(payload), [])
        self.assertEqual(payload["status"], "open_revision_ledger_no_executed_human_rows")
        self.assertEqual(payload["summary"]["executed_human_revision_rows"], 0)
        self.assertGreater(payload["summary"]["open_revision_rows"], 0)
        self.assertTrue(all(row["status"] == "pending_external_calibration" for row in payload["revision_rows"]))
        self.assertTrue(any(row["source"] == "human_calibration_analysis" for row in payload["source_queue"]))
        self.assertTrue(any("not evidence" in guardrail for guardrail in payload["claim_guardrails"]))

    def test_citation_audit_links_paper_citations_to_reference_artifacts(self):
        payload = build_citation_audit()
        self.assertEqual(validate_citation_audit(payload), [])
        self.assertEqual(payload["summary"]["references"], 12)
        self.assertTrue(payload["summary"]["contiguous_numbering"])
        self.assertEqual(payload["summary"]["rows_with_context"], payload["summary"]["contexts_checked"])
        self.assertEqual(payload["summary"]["context_term_matches"], payload["summary"]["contexts_checked"])
        self.assertEqual(payload["external_status"], "local_context_verified_external_spotcheck_required")

    def test_license_readiness_tracks_owner_placeholders(self):
        payload = build_license_report()
        self.assertEqual(validate_license_report(payload), [])
        self.assertFalse(payload["summary"]["release_ready"])
        statuses = {check["id"]: check["status"] for check in payload["checks"]}
        self.assertEqual(statuses["license_template_exists"], "pass")
        self.assertEqual(statuses["citation_template_exists"], "pass")
        self.assertEqual(statuses["license_file_exists"], "missing")
        self.assertIn(statuses["citation_author_placeholder"], {"incomplete", "pass"})
        self.assertIn("license_choice", {decision["id"] for decision in payload["required_decisions"]})

    def test_release_metadata_checklist_keeps_owner_decisions_explicit(self):
        payload = build_release_metadata_checklist()
        self.assertEqual(validate_release_metadata_checklist(payload), [])
        self.assertEqual(payload["status"], "owner_action_required")
        spdx_ids = {row["spdx_id"] for row in payload["license_options"]}
        self.assertIn("MIT", spdx_ids)
        self.assertIn("Apache-2.0", spdx_ids)
        self.assertIn("<owner>/<repo>", payload["citation_template"]["repository-code"])
        self.assertTrue(any("LICENSE.template" in step for step in payload["finalization_steps"]))
        self.assertTrue(any("CITATION.cff.template" in step for step in payload["finalization_steps"]))
        self.assertTrue(any("Template files are intentionally non-final" in guardrail for guardrail in payload["guardrails"]))
        self.assertTrue(any("LICENSE" in step for step in payload["finalization_steps"]))

    def test_release_metadata_templates_exist_but_are_not_final(self):
        license_template = (PACKAGE_ROOT / "LICENSE.template").read_text(encoding="utf-8")
        citation_template = (PACKAGE_ROOT / "CITATION.cff.template").read_text(encoding="utf-8")
        self.assertIn("This file is not a license", license_template)
        self.assertIn("Do not publish", license_template)
        self.assertIn("<replace with author name>", citation_template)
        self.assertIn("<SPDX license id selected by project owner>", citation_template)

    def test_human_calibration_protocol_is_not_misreported_as_executed(self):
        payload = build_human_calibration_protocol()
        self.assertEqual(validate_human_calibration_protocol(payload), [])
        self.assertEqual(payload["status"], "protocol_only_not_executed")
        self.assertGreaterEqual(payload["task_sampling"]["minimum_tasks"], 20)
        self.assertTrue(any("Do not claim" in guardrail for guardrail in payload["claim_guardrails"]))

    def test_human_calibration_schema_validates_filled_submission(self):
        payload = build_human_calibration_schema()
        self.assertEqual(validate_human_calibration_schema(payload), [])
        template = human_calibration_template()
        self.assertTrue(validate_human_calibration_submission(template))
        for review in template["task_reviews"]:
            review["scenario_realism"] = 4
            review["action_coverage"] = 4
            review["score_alignment"] = 4
            review["difficulty"] = "appropriate"
            review["top_actions"] = ["research_market", "build_offer"]
        self.assertEqual(validate_human_calibration_submission(template), [])
        self.assertEqual(len(payload["required_task_ids"]), 20)

    def test_human_calibration_analysis_reports_no_data_honestly(self):
        payload = build_human_calibration_analysis([])
        self.assertEqual(validate_human_calibration_analysis(payload), [])
        self.assertEqual(payload["status"], "no_submissions_found")
        self.assertEqual(payload["participant_count"], 0)
        self.assertTrue(any("Do not cite" in guardrail for guardrail in payload["claim_guardrails"]))

    def test_human_calibration_packet_is_non_executed_and_actionable(self):
        payload = build_human_calibration_packet()
        self.assertEqual(validate_human_calibration_packet(payload), [])
        self.assertEqual(payload["status"], "recruitment_packet_not_executed")
        self.assertGreaterEqual(payload["minimum_participant_plan"]["minimum_total"], 10)
        self.assertEqual(len(payload["required_task_sample"]["required_task_ids"]), 20)
        self.assertTrue(any("not executed" in guardrail.lower() for guardrail in payload["claim_guardrails"]))
        self.assertTrue(any("human_calibration_analysis" in step for step in payload["collection_workflow"]))

    def test_human_calibration_analysis_aggregates_executed_submission(self):
        submission = human_calibration_template()
        submission["participant_group"] = "startup_operator"
        submission["participant_experience_years"] = 8
        submission["conflict_disclosure"] = "none"
        for index, review in enumerate(submission["task_reviews"]):
            review["scenario_realism"] = 4
            review["action_coverage"] = 4
            review["score_alignment"] = 2 if index == 0 else 4
            review["difficulty"] = "ambiguous" if index == 0 else "appropriate"
            review["top_actions"] = ["research_market", "build_offer"]
            review["gaming_risk"] = "synthetic note"
            review["recommended_revision"] = "tighten score rule" if index == 0 else ""
            review["flag_for_revision"] = index == 0
        payload = build_human_calibration_analysis([submission], ["synthetic-human.json"])
        self.assertEqual(validate_human_calibration_analysis(payload), [])
        self.assertEqual(payload["status"], "executed")
        self.assertEqual(payload["participant_count_by_group"], {"startup_operator": 1})
        self.assertEqual(payload["summary"]["flagged_tasks"], 1)
        self.assertEqual(payload["summary"]["recommended_revisions"], 1)
        self.assertEqual(payload["flagged_tasks"][0]["task_id"], "FND-001")

    def test_submission_gate_is_not_ready_until_blockers_clear(self):
        payload = build_gate()
        self.assertEqual(validate_gate(payload), [])
        self.assertEqual(payload["final_status"], "not_ready")
        gates = {gate["id"]: gate for gate in payload["gates"]}
        self.assertEqual(gates["artifact_and_documentation"]["status"], "pass")
        self.assertEqual(gates["required_experiments"]["status"], "fail")
        self.assertEqual(gates["license_and_citation"]["status"], "fail")

    def test_completion_audit_maps_goal_requirements_without_overclaiming(self):
        payload = build_completion_audit()
        self.assertEqual(validate_completion_audit(payload), [])
        self.assertEqual(payload["completion_claim"], "not_complete")
        statuses = {item["id"]: item["status"] for item in payload["items"]}
        self.assertEqual(statuses["scaled_task_suite"], "complete")
        self.assertEqual(statuses["heuristic_baselines_and_ablations"], "complete")
        self.assertEqual(statuses["representative_llm_baselines"], "missing")
        self.assertEqual(statuses["public_release_metadata"], "incomplete")
        self.assertGreaterEqual(payload["summary"]["complete"], 5)

    def test_submission_manifest_summarizes_supported_and_excluded_claims(self):
        payload = build_submission_manifest()
        self.assertEqual(validate_submission_manifest(payload), [])
        self.assertFalse(payload["readiness"]["ready_for_publication"])
        self.assertIn("required_experiments", payload["readiness"]["failed_gates"])
        self.assertGreaterEqual(payload["summary"]["supported_claims"], 5)
        self.assertGreaterEqual(payload["summary"]["excluded_or_not_yet_supported_claims"], 3)
        excluded_ids = {row["id"] for row in payload["excluded_or_not_yet_supported_claims"]}
        self.assertIn("hosted_llm_comparison", excluded_ids)

    def test_submission_action_plan_maps_failing_gates_to_commands(self):
        payload = build_submission_action_plan()
        self.assertEqual(validate_submission_action_plan(payload), [])
        self.assertEqual(payload["submission_gate_status"], "not_ready")
        gates = {step["gate"] for step in payload["steps"]}
        self.assertIn("required_experiments", gates)
        self.assertIn("provider_run_readiness", gates)
        self.assertIn("license_and_citation", gates)
        self.assertTrue(any("resumable_runner" in " ".join(step["commands"]) for step in payload["steps"]))
        self.assertTrue(any(step["owner"] == "project_owner" for step in payload["steps"]))


if __name__ == "__main__":
    unittest.main()
