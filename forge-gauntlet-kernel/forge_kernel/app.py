# File: forge_kernel/app.py

from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

from .graph import FORGE_GRAPH
from .state import ForgeState


app = FastAPI(
    title="FORGE Kernel",
    description="Lightweight kernel API for FORGE gauntlet runs.",
    version="0.1.0",
)


class GauntletRequest(BaseModel):
    idea: str = Field(..., description="Raw idea text from user/Dana.")
    feature_brief: Optional[str] = Field(
        None,
        description="Optional pre-structured brief. If not provided, kernel uses idea.",
    )
    project_id: Optional[str] = Field(
        None,
        description="Optional external project id (e.g., Supabase or GitHub id).",
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Optional extra tags/flags.",
    )


class GauntletResponse(BaseModel):
    state: Dict[str, Any]


@app.get("/health")
def health_check() -> Dict[str, str]:
    """
    Simple health endpoint so you can see if the kernel is up.
    """
    return {"status": "ok"}


@app.post("/run-gauntlet", response_model=GauntletResponse)
def run_gauntlet(payload: GauntletRequest) -> GauntletResponse:
    """
    Run a single gauntlet pass through the kernel.

    This is the endpoint your frontend or JS backend will call.
    """
    initial_state: ForgeState = {
        "idea": payload.idea,
        "feature_brief": payload.feature_brief or payload.idea,
        "project_id": payload.project_id,
        "metadata": payload.metadata or {},
        "logs": [],
    }

    final_state = FORGE_GRAPH.invoke(initial_state)
    return GauntletResponse(state=final_state)
