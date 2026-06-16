from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class MapSignature:
    """
    Known DENSO calibration signature.
    """

    name: str
    category: str

    rows: int
    columns: int

    element_size: int

    x_axis_length: int
    y_axis_length: int

    min_confidence: float = 0.75

    description: str = ""


class SignatureDatabase:

    MAPS: list[MapSignature] = [

        MapSignature(
            name="Driver Demand",
            category="Torque",
            rows=16,
            columns=16,
            element_size=2,
            x_axis_length=16,
            y_axis_length=16,
            description="Accelerator pedal request",
        ),

        MapSignature(
            name="Torque Limiter",
            category="Torque",
            rows=16,
            columns=16,
            element_size=2,
            x_axis_length=16,
            y_axis_length=16,
            description="Maximum permitted torque",
        ),

        MapSignature(
            name="Smoke Limiter",
            category="Fuel",
            rows=16,
            columns=16,
            element_size=2,
            x_axis_length=16,
            y_axis_length=16,
            description="Airflow-based smoke limiter",
        ),

        MapSignature(
            name="Injection Quantity",
            category="Fuel",
            rows=16,
            columns=16,
            element_size=2,
            x_axis_length=16,
            y_axis_length=16,
            description="Main injection quantity",
        ),

        MapSignature(
            name="Rail Pressure",
            category="Fuel",
            rows=16,
            columns=16,
            element_size=2,
            x_axis_length=16,
            y_axis_length=16,
            description="Common rail pressure target",
        ),

        MapSignature(
            name="Boost Target",
            category="Boost",
            rows=16,
            columns=16,
            element_size=2,
            x_axis_length=16,
            y_axis_length=16,
            description="Turbocharger boost target",
        ),

        MapSignature(
            name="Boost Limiter",
            category="Boost",
            rows=16,
            columns=16,
            element_size=2,
            x_axis_length=16,
            y_axis_length=16,
            description="Maximum boost limiter",
        ),

        MapSignature(
            name="SOI",
            category="Injection",
            rows=16,
            columns=16,
            element_size=2,
            x_axis_length=16,
            y_axis_length=16,
            description="Start of Injection",
        ),

        MapSignature(
            name="Duration",
            category="Injection",
            rows=16,
            columns=16,
            element_size=2,
            x_axis_length=16,
            y_axis_length=16,
            description="Injection duration",
        ),

        MapSignature(
            name="Pilot Injection",
            category="Injection",
            rows=16,
            columns=16,
            element_size=2,
            x_axis_length=16,
            y_axis_length=16,
            description="Pilot injection quantity",
        ),

        MapSignature(
            name="Lambda",
            category="Air",
            rows=16,
            columns=16,
            element_size=2,
            x_axis_length=16,
            y_axis_length=16,
            description="Lambda target",
        ),
    ]

    @classmethod
    def all(cls) -> list[MapSignature]:
        return cls.MAPS.copy()

    @classmethod
    def categories(cls) -> list[str]:
        return sorted(
            {
                signature.category
                for signature in cls.MAPS
            }
        )

    @classmethod
    def find_by_name(
        cls,
        name: str,
    ) -> MapSignature | None:

        for signature in cls.MAPS:

            if signature.name.lower() == name.lower():
                return signature

        return None

    @classmethod
    def by_category(
        cls,
        category: str,
    ) -> list[MapSignature]:

        return [
            signature
            for signature in cls.MAPS
            if signature.category.lower()
            == category.lower()
        ]
