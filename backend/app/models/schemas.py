"""
Pydantic models for request/response schemas
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum


class QueryRequest(BaseModel):
    """Request model for queries"""
    query: str
    
    
class DataPoint(BaseModel):
    """Single data point from time series"""
    timestamp: datetime
    value: float
    tags: Dict[str, str] = {}
    fields: Dict[str, Any] = {}
