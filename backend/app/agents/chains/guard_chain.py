"""Content filtering and safety guard chain"""
import re
import random
import logging
from typing import Tuple
from dataclasses import dataclass
from app.agents.chains.personality import WITTY_REJECTION_RESPONSES

@dataclass
class GuardResult:
    """Result from guard chain check"""
    is_malicious: bool
    reason: str = ""
    response: str = ""

class GuardChain:
    """
    Safety and content filtering
    - Detect prompt injection attempts
    - Block malicious queries
    - Filter sensitive info requests
    """

    PROMPT_INJECTION_PATTERNS = [
        r"ignore\s+(previous|all|any)\s+(instructions?|prompts?|rules?|directives?)",
        r"forget\s+(everything|all|previous)",
        r"you\s+are\s+now",
        r"new\s+instructions?",
        r"system\s+prompt",
        r"disregard\s+(previous|above|all)",
        r"act\s+as",
        r"pretend\s+(you|to)\s+(are|be)",
        r"roleplay\s+as",
        r"what\s+(are|were)\s+your\s+(original\s+)?instructions?",
        r"show\s+me\s+your\s+prompt",
        r"bypass",
        r"override",
        r"<script>",  # XSS attempts
        r"DROP TABLE",  # SQL injection
        r"<\s*script",  # More XSS variations
    ]

    SENSITIVE_INFO_PATTERNS = [
        r"phone\s+number",
        r"home\s+address",
        r"social\s+security",
        r"credit\s+card",
        r"password",
        r"api\s+key",
        r"family\s+members?",
        r"(mother|father|sibling|parent).*name",
    ]

    def check(self, message: str) -> GuardResult:
        """Check if message is malicious or requests sensitive info"""

        # Check for prompt injection
        for pattern in self.PROMPT_INJECTION_PATTERNS:
            if re.search(pattern, message, re.IGNORECASE):
                return GuardResult(
                    is_malicious=True,
                    reason="prompt_injection",
                    response=random.choice(WITTY_REJECTION_RESPONSES)
                )

        # Check for sensitive info requests
        for pattern in self.SENSITIVE_INFO_PATTERNS:
            if re.search(pattern, message, re.IGNORECASE):
                return GuardResult(
                    is_malicious=True,
                    reason="sensitive_info_request",
                    response="I can't share personal contact details. For direct contact, please email Paolo at pjsandejas@gmail.com"
                )

        return GuardResult(is_malicious=False)

    def filter_response(self, response: str) -> str:
        """Remove any sensitive info that might have leaked into response"""
        SENSITIVE_PATTERNS = {
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b': '[PHONE_REDACTED]',  # Phone
            r'\b\d{3}-\d{2}-\d{4}\b': '[SSN_REDACTED]',  # SSN
        }

        filtered = response
        for pattern, replacement in SENSITIVE_PATTERNS.items():
            filtered = re.sub(pattern, replacement, filtered)

        return filtered
