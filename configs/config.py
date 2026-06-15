"""
configs/config.py

BLAKKBOX Global Configuration

Central location for all configurable values used
throughout the analysis pipeline.
"""

from __future__ import annotations

from typing import Any

# ==========================================================
# Project
# ==========================================================

PROJECT_NAME: str = "BLAKKBOX"
PROJECT_VERSION: str = "0.4.0-dev"

# ==========================================================
# Delta
# ==========================================================

MERGE_MAX_GAP: int = 8

# ==========================================================
# Region Classification
# ==========================================================

CLASSIFICATION_MIN_LENGTH: int = 64
UNKNOWN_MIN_LENGTH: int = 16

CALIBRATION_CONFIDENCE: float = 0.60
UNKNOWN_CONFIDENCE: float = 0.30
SMALL_EDIT_CONFIDENCE: float = 0.10

# ==========================================================
# Axis Analysis
# ==========================================================

AXIS_WINDOW: int = 8
AXIS_MIN_SCORE: int = 70

# ==========================================================
# Geometry Analysis
# ==========================================================

GEOMETRY_MIN_SCORE: int = 70

MIN_ROWS: int = 2
MIN_COLUMNS: int = 2

MAX_ROWS: int = 64
MAX_COLUMNS: int = 64

# ==========================================================
# Reporting
# ==========================================================

MAX_REPORT_CANDIDATES: int = 5

# ==========================================================
# Logging
# ==========================================================

LOG_LEVEL: str = "INFO"

# ==========================================================
# Future Configuration
# ==========================================================

ENABLE_DEBUG: bool = False
ENABLE_TIMING: bool = True
ENABLE_STATISTICS: bool = True

SAVE_REPORTS: bool = True
EXPORT_JSON: bool = False
EXPORT_CSV: bool = False

# ==========================================================
# Reserved
# ==========================================================

RESERVED: dict[str, Any] = {}
