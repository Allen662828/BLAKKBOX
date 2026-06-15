from delta.region import DeltaRegion


class DeltaCluster:

    def cluster(self, offsets):

        if not offsets:
            return []

        regions = []

        start = offsets[0]
        end = offsets[0]

        for offset in offsets[1:]:

            if offset == end + 1:
                end = offset
            else:
                regions.append(DeltaRegion(start, end))
                start = end = offset

        regions.append(DeltaRegion(start, end))

        return regions