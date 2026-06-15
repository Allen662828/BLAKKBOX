class DeltaExtractor:

    def extract(self, original: bytes, mod: bytes):

        changed = []

        for offset, (o, m) in enumerate(zip(original, mod)):
            if o != m:
                changed.append(offset)

        return changed
