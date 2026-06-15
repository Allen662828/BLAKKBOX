from validation.rom_size import RomSizeValidator


class Validator:

    def __init__(self):

        self.validators = [
            RomSizeValidator()
        ]

    def validate(self, original, mod):

        print("\nRunning Validation...\n")

        for validator in self.validators:

            result = validator.validate(original, mod)

            if result.passed:
                print(f"[PASS] {result.name}: {result.message}")
            else:
                print(f"[FAIL] {result.name}: {result.message}")
                raise RuntimeError(result.message)

        print()