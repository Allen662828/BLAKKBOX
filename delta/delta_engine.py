from delta.extractor import DeltaExtractor
from delta.clustering import DeltaCluster
from delta.merger import DeltaMerger
from delta.statistics import DeltaStatistics
from delta.report import DeltaReport


class DeltaEngine:
    """
    Delta Analysis Engine

    Pipeline

        ORIGINAL
            │
        MODIFIED
            │
        Byte Comparison
            │
        Region Clustering
            │
        Region Merging
            │
        Statistics
            │
        Report
    """

    def __init__(self):

        self.extractor = DeltaExtractor()
        self.cluster = DeltaCluster()
        self.merger = DeltaMerger(max_gap=8)
        self.statistics = DeltaStatistics()
        self.report = DeltaReport()

    def analyze(self, original: bytes, mod: bytes):

        # ==========================================================
        # BYTE COMPARISON
        # ==========================================================

        offsets = self.extractor.extract(original, mod)

        # ==========================================================
        # INITIAL REGION CLUSTERING
        # ==========================================================

        regions = self.cluster.cluster(offsets)

        # ==========================================================
        # SMART REGION MERGING
        # ==========================================================

        merged_regions = self.merger.merge(regions)

        self.merger.statistics(regions, merged_regions)

        # ==========================================================
        # DELTA STATISTICS
        # ==========================================================

        stats = self.statistics.summarize(merged_regions)

        # ==========================================================
        # REPORT
        # ==========================================================

        self.report.print(stats)

        return merged_regions
