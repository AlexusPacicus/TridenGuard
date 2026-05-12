from pydantic import BaseModel, Field, validator
from typing import List, Optional, Literal
from enum import Enum

class RadicalType(str, Enum):
    ACTOR = "Actor"
    DEONTIC = "Deontic"
    ACTION = "Action"
    OBJECT = "Object"
    TEMPORAL = "Temporal"
    SPATIAL = "Spatial"
    METRIC = "Metric"
    CONDITION = "Condition"

class Radical(BaseModel):
    radical: RadicalType
    value: str = Field(..., min_length=1, max_length=500)
    
    @validator('value')
    def value_must_be_meaningful(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('Radical value too short')
        return v.strip()

class ExtractionResult(BaseModel):
    axiom: str = Field(..., min_length=5, max_length=500)
    radicals: List[Radical] = Field(..., min_items=0, max_items=8)
    
    @validator('radicals')
    def no_duplicate_radicals(cls, v):
        types = [r.radical for r in v]
        if len(types) != len(set(types)):
            raise ValueError('Duplicate radical types are not allowed')
        return v

class ValidationResult(BaseModel):
    case_id: str
    timestamp: str
    source_text: str
    extraction: ExtractionResult
    status: Literal["VALIDATED", "QUARANTINED"]
    rejection_reason: str
    errors: List[str] = []
    source_integrity: bool = True
    ungrounded_radicals: List[dict] = []
    has_critical: bool = False
    has_warning: bool = False
    has_unknown: bool = False
    has_validated: bool = False
    error_count: int = 0