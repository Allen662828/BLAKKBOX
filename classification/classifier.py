class RegionClassifier:

    def classify(self, regions):

        for region in regions:

            if region.length >= 64:

                region.region_type = "CALIBRATION"
                region.calibration = True
                region.confidence = 0.60

            elif region.length >= 16:

                region.region_type = "UNKNOWN"
                region.confidence = 0.30

            else:

                region.region_type = "SMALL_EDIT"
                region.confidence = 0.10

        return regions