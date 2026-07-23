import os
import unittest
from unittest.mock import patch

from founderbench.llm_policy import (
    AnthropicTaskPolicy,
    KimiTaskPolicy,
    OpenAIHostedTaskPolicy,
)


class KimiK3PolicyTests(unittest.TestCase):
    def test_kimi_k3_is_default_and_uses_supported_parameters(self):
        # K3 rejects custom sampling values and counts reasoning tokens toward
        # max_completion_tokens, so its request differs from older Kimi models.
        with patch.dict(
            os.environ,
            {"KIMI_API_KEY": "test-key", "KIMI_TIMEOUT_S": "180"},
            clear=True,
        ):
            policy = KimiTaskPolicy()
            payload = policy._chat_payload("{}")

        self.assertEqual(policy.model, "kimi-k3")
        self.assertEqual(policy.max_tokens, 4096)
        self.assertEqual(policy.timeout_s, 180)
        self.assertEqual(payload["reasoning_effort"], "max")
        self.assertEqual(payload["max_completion_tokens"], 4096)
        self.assertNotIn("temperature", payload)
        self.assertNotIn("max_tokens", payload)

    def test_gpt_5_6_sol_uses_supported_completion_parameters(self):
        # Sol rejects max_tokens and non-default temperature values.
        with patch.dict(
            os.environ,
            {"OPENAI_API_KEY": "test-key", "OPENAI_TIMEOUT_S": "120"},
            clear=True,
        ):
            policy = OpenAIHostedTaskPolicy()
            payload = policy._chat_payload("{}")

        self.assertEqual(policy.model, "gpt-5.6-sol")
        self.assertEqual(policy.max_tokens, 4096)
        self.assertEqual(policy.timeout_s, 120)
        self.assertEqual(payload["max_completion_tokens"], 4096)
        self.assertNotIn("temperature", payload)
        self.assertNotIn("max_tokens", payload)

    def test_sonnet_5_omits_deprecated_sampling_parameters(self):
        with patch.dict(
            os.environ,
            {"ANTHROPIC_API_KEY": "test-key", "ANTHROPIC_TIMEOUT_S": "120"},
            clear=True,
        ):
            policy = AnthropicTaskPolicy()
            payload = policy._message_payload("{}")

        self.assertEqual(policy.model, "claude-sonnet-5")
        self.assertEqual(policy.max_tokens, 4096)
        self.assertEqual(policy.timeout_s, 120)
        self.assertEqual(payload["max_tokens"], 4096)
        self.assertNotIn("temperature", payload)


if __name__ == "__main__":
    unittest.main()
