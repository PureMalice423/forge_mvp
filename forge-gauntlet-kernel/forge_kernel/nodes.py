# File: forge_kernel/nodes.py

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

from .state import ForgeState


# ---------------------------------------------------------------------------
# Load ipsum data (internal + public) from ipsum.json, if present
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
IPSUM_PATH = BASE_DIR / "ipsum.json"

try:
    with IPSUM_PATH.open("r", encoding="utf-8") as f:
        IPSUM_DATA: Dict[str, Any] = json.load(f)
except FileNotFoundError:
    IPSUM_DATA = {}


def _log(state: ForgeState, message: str) -> ForgeState:
    """
    Append a log message into the state's logs list.
    """
    logs = state.get("logs") or []
    logs.append(message)
    state["logs"] = logs
    return state


def _get_public_ipsum(ref_id: Optional[str]) -> Optional[str]:
    """
    Look up a public-safe ipsum line by id from ipsum.json.
    This is optional sugar: if not found, we just return None.
    """
    if not ref_id:
        return None

    public = IPSUM_DATA.get("public", {})
    entries = public.get("entries", [])
    for entry in entries:
        if entry.get("id") == ref_id:
            return entry.get("encoded")
    return None


# ---------------------------------------------------------------------------
# Node 1: Intake / normalization
# ---------------------------------------------------------------------------

def intake_node(state: ForgeState) -> ForgeState:
    """
    First stop in the kernel: normalize the raw idea and seed feature_brief.
    """
    idea = state.get("idea", "").strip()
    if not idea:
        idea = "Untitled idea (empty input)."

    state["idea"] = idea
    state["feature_brief"] = state.get("feature_brief") or idea

    _log(
        state,
        f"[intake] normalized idea: {idea[:80]}{'...' if len(idea) > 80 else ''}",
    )
    return state


# ---------------------------------------------------------------------------
# Node 2: Fixer stub (quick smoothing / sanity)
# ---------------------------------------------------------------------------

def fixer_node(state: ForgeState) -> ForgeState:
    """
    Stub fixer node. In the real gauntlet this would:
    - Clean up contradictions
    - Normalize structure
    - Remove obvious junk
    For now, we just log and pass through.
    """
    brief = state.get("feature_brief", "")
    _log(state, "[fixer] received feature_brief, length=" + str(len(brief)))
    return state


# ---------------------------------------------------------------------------
# Node 3: Gauntlet core stub (multi-LLM orchestration placeholder)
# ---------------------------------------------------------------------------

def gauntlet_node(state: ForgeState) -> ForgeState:
    """
    Stub gauntlet node. This is where the Perplexity → Gemini → Grok → ChatGPT
    chain will eventually live.

    Today, it just attaches a simple structured skeleton to prove the pipe works.
    """
    idea = state.get("idea", "Untitled idea")
    skeleton = {
        "title": f"FORGE draft for: {idea[:60]}",
        "stages": [
            "research_stub",
            "blueprint_stub",
            "stress_test_stub",
            "integration_stub",
        ],
    }
    metadata = state.get("metadata") or {}
    metadata["skeleton"] = skeleton
    state["metadata"] = metadata

    _log(state, "[gauntlet] attached draft skeleton structure.")
    return state


# ---------------------------------------------------------------------------
# Node 4: Linearizer stub (make it read-out friendly)
# ---------------------------------------------------------------------------

def linearizer_node(state: ForgeState) -> ForgeState:
    """
    Stub linearizer node. This is where you'd turn the internal graph-shaped
    result into a linear, human-readable blueprint.
    """
    idea = state.get("idea", "Untitled idea")
    feature_brief = state.get("feature_brief", idea)

    linear_brief = (
        f"PROJECT: {idea}\n\n"
        f"SUMMARY:\n{feature_brief}\n\n"
        "NOTE: This is a stub linearization from the FORGE kernel."
    )

    metadata = state.get("metadata") or {}
    metadata["linear_brief"] = linear_brief
    state["metadata"] = metadata

    _log(state, "[linearizer] produced stub linear brief.")
    return state


# ---------------------------------------------------------------------------
# Node 5: Vault prep stub (ready for storage / UI)
# ---------------------------------------------------------------------------

def vault_prep_node(state: ForgeState) -> ForgeState:
    """
    Final stub node before Vault. Here we:
    - Attach one public-safe FORGE ipsum line (if available)
    - Mark the state as `status=draft`
    """
    metadata = state.get("metadata") or {}

    # Try to grab a public ipsum line, if the file exists
    public_meta = IPSUM_DATA.get("public", {}).get("meta", {})
    default_ref = None
    if public_meta:
        # just pick first entry if we have any
        entries = IPSUM_DATA.get("public", {}).get("entries", [])
        if entries:
            default_ref = entries[0].get("id")

    ipsum_line = _get_public_ipsum(default_ref)
    if ipsum_line:
        metadata["forge_ipsum"] = {
            "ref": default_ref,
            "text": ipsum_line,
        }

    metadata["status"] = "draft"
    state["metadata"] = metadata

    _log(state, "[vault_prep] marked state as draft and attached FORGE ipsum (if available).")
    return state
