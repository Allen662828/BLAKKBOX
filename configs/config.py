"""
configs/config.py

BLAKKBOX Global Configuration

Central location for all configurable values used throughout
the analysis pipeline.
"""

# ==========================================================
# Project
# ==========================================================

PROJECT_NAME = "BLAKKBOX"
PROJECT_VERSION = "0.4.0-dev"

# ==========================================================
# Delta
# ==========================================================

# Maximum number of bytes allowed between two adjacent regions
# before they are considered separate regions.
MERGE_MAX_GAP = 8

# ==========================================================
# Region Classification
# ==========================================================

# Minimum region size to be considered a large structural region.
CLASSIFICATION_MIN_LENGTH = 64

# Minimum region size for an unknown candidate.
UNKNOWN_MIN_LENGTH = 16

# Classification confidence values.
CALIBRATION_CONFIDENCE = 0.60
UNKNOWN_CONFIDENCE = 0.30
SMALL_EDIT_CONFIDENCE = 0.10

# ==========================================================
# Axis Analysis
# ==========================================================

# Sliding window length used when scanning for monotonic sequences.
AXIS_WINDOW = 8

# Minimum score required for a valid structural candidate.
AXIS_MIN_SCORE = 70

# ==========================================================
# Geometry Analysis
# ==========================================================

# Minimum geometry score required for a valid structure.
GEOMETRY_MIN_SCORE = 70

# Expected structural limits.
MIN_ROWS = 2
MIN_COLUMNS = 2

MAX_ROWS = 64
MAX_COLUMNS = 64

# ==========================================================
# Reporting
# ==========================================================

# Maximum number of candidates displayed in reports.
MAX_REPORT_CANDIDATES = 5

# ==========================================================
# Logging
# ==========================================================

LOG_LEVEL = "INFO"

# ==========================================================
# Future Configuration
# ==========================================================

ENABLE_DEBUG = False
ENABLE_TIMING = True
ENABLE_STATISTICS = True

SAVE_REPORTS = True
EXPORT_JSON = False
EXPORT_CSV = False

# ==========================================================
# Reserved
# ==========================================================

RESERVED = {}
