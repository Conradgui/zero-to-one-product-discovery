"""Offline provider error handling tests.

These tests use mocked HTTP responses only. They must never call a real API.
"""

from __future__ import annotations

import io
import os
import unittest
import urllib.error
from unittest.mock import patch

from tests import conftest


class TestProviderErrorRedaction(unittest.TestCase):
    def test_security_provider_error__does_not_expose_api_key_in_error_text(self):
        fake_key = "sk-test-should-not-leak"

        def raise_http_error(_request, timeout=60):
            raise urllib.error.HTTPError(
                url="https://api.deepseek.com/v1/chat/completions",
                code=401,
                msg="Unauthorized",
                hdrs=None,
                fp=io.BytesIO(f'{{"error":"bad key {fake_key}"}}'.encode("utf-8")),
            )

        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": fake_key}, clear=False):
            with patch("urllib.request.urlopen", side_effect=raise_http_error):
                result = conftest.call_llm("hello", provider="deepseek")

        self.assertFalse(result["ok"])
        self.assertEqual(result["status_code"], 401)
        self.assertNotIn(fake_key, result["error"])
        self.assertIn("[REDACTED_API_KEY]", result["error"])

    def test_error_provider_mock__timeout_returns_structured_error(self):
        def raise_timeout(_request, timeout=60):
            raise urllib.error.URLError(TimeoutError("timed out"))

        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "sk-test"}, clear=False):
            with patch("urllib.request.urlopen", side_effect=raise_timeout):
                result = conftest.call_llm("hello", provider="deepseek", timeout=1)

        self.assertEqual(result["ok"], False)
        self.assertIn("error", result)
        self.assertIn("URL error", result["error"])

    def test_error_provider_mock__malformed_response_returns_structured_error(self):
        class FakeResponse:
            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

            def read(self):
                return b'{"choices":[]}'

        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "sk-test"}, clear=False):
            with patch("urllib.request.urlopen", return_value=FakeResponse()):
                result = conftest.call_llm("hello", provider="deepseek")

        self.assertEqual(result["ok"], False)
        self.assertIn("error", result)


if __name__ == "__main__":
    unittest.main()
