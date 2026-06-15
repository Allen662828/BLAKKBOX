from core.pipeline import Pipeline


class Workflow:

    def __init__(self):
        self.pipeline = Pipeline()

    def run(self):

        print("=" * 60)
        print("BLAKKBOX DENSO STUDIO")
        print("=" * 60)

        self.pipeline.execute(
            "ORIGINAL.bin",
            "MOD.bin"
        )

        print("=" * 60)
        print("Workflow Finished")
        print("=" * 60)