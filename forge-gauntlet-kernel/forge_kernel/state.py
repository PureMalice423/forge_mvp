# File: forge_kernel/state.py

from __future__ import annotations

from typing import Any, Dict, List, Optional, TypedDict


class ForgeState(TypedDict, total=False):
    """
    Minimal shared state object that flows through the FORGE kernel.
    This is intentionally simple and flexible.
    """
    idea: str
    feature_brief: str
    project_id: Optional[str]
    metadata: Dict[str, Any]
    logs: List[str]
#test webhook
