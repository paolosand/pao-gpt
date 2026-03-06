"""Content filtering and safety guard chain"""
import re
import random
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

    MALICIOUS_PATTERNS = [
        r"ignore (previous|all) (instructions|prompts|rules)",
        r"forget (everything|all|your instructions)",
        r"you are now",
        r"new (instructions|prompt|system message|role)",
        r"reveal your (prompt|system|instructions)",
        r"<script>",  # XSS attempts
        r"DROP TABLE",  # SQL injection
        r"<\s*script",  # More XSS variations
    ]

    SENSITIVE_INFO_REQUESTS = [
        r"(phone|cell|mobile) number",
        r"home address",
        r"social security",
        r"credit card",
        r"password",
        r"mother'?s maiden name",
    ]

    def check(self, message: str) -> GuardResult:
        """Check if message is malicious or requests sensitive info"""

        # Check for prompt injection
        for pattern in self.MALICIOUS_PATTERNS:
            if re.search(pattern, message, re.IGNORECASE):
                return GuardResult(
                    is_malicious=True,
                    reason="prompt_injection",
                    response=random.choice(WITTY_REJECTION_RESPONSES)
                )

        # Check for sensitive info requests
        for pattern in self.SENSITIVE_INFO_REQUESTS:
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
