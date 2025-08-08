from __future__ import annotations
from dataclasses import dataclass

@dataclass
class ApiKeyAuth:
    header: str
    value: str
    def headers(self) -> dict:
        return {self.header: self.value}

# Placeholders for future schemes (OAuth2, AWS SigV4)