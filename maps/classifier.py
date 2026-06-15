class StructureClassifier:

    def classify(self, candidate):

        rows, cols = candidate.get("shape", (1, 1))

        if rows == 1 and cols == 1:
            structure = "SCALAR"

        elif rows == 1 or cols == 1:
            structure = "LINEAR TABLE"

        else:
            structure = "MATRIX"

        return {
            "region": candidate["region"],
            "shape": (rows, cols),
            "structure": structure,
            "confidence": candidate.get("score", 0),
        }
