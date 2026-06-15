class ClassificationReport:

    def print(self, regions):

        calibration = 0
        unknown = 0
        small = 0

        for region in regions:

            if region.region_type == "CALIBRATION":
                calibration += 1

            elif region.region_type == "SMALL_EDIT":
                small += 1

            else:
                unknown += 1

        print()
        print("=" * 60)
        print("REGION CLASSIFICATION")
        print("=" * 60)

        print(f"Calibration Regions : {calibration}")
        print(f"Unknown Regions     : {unknown}")
        print(f"Small Regions       : {small}")

        print("=" * 60)