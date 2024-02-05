from datetime import datetime

from databased import Databased
from pandas import DataFrame
from pathier import Pathier

root = Pathier(__file__).parent


class Pressured(Databased):
    def __init__(self, dbpath: Pathier = root / "blood_pressure.db"):
        super().__init__(dbpath)
        self.init_table()

    def init_table(self):
        """Create pressure table."""
        self.create_table(
            "readings",
            "systolic int",
            "diastolic int",
            "pulse int",
            "date timestamp",
            "pulse_pressure int",
        )

    def add_reading(self, systolic: int, diastolic: int, pulse: int):
        """Add blood pressure reading to database."""
        self.insert(
            "readings",
            ("systolic", "diastolic", "pulse", "date", "pulse_pressure"),
            [(systolic, diastolic, pulse, datetime.now(), systolic - diastolic)],
        )

    def _get_date_condition(self, start: datetime, stop: datetime) -> str:
        return f"date BETWEEN '{start}' AND '{stop}'"

    def get_readings(
        self,
        start_date: datetime = datetime.min,
        stop_date: datetime = datetime.max,
    ) -> DataFrame:
        """Returns readings as a DataFrame.
        The date range can be narrowed through 'start_date' and/or 'stop_date'."""
        return DataFrame(
            self.select(
                "readings", where=self._get_date_condition(start_date, stop_date)
            )
        )

    def get_averages(
        self,
        start_date: datetime = datetime.min,
        stop_date: datetime = datetime.max,
    ) -> dict:
        """Returns averages between `start_date` and `stop_date` for:

        'systolic'

        'diastolic'

        'pulse'

        'pulse_pressure'
        """
        calc = lambda s: f"ROUND(AVG({s}), 2) AS {s}"
        columns = [
            column for column in self.get_columns("readings") if column != "date"
        ]
        return self.select(
            "readings",
            columns=list(map(calc, columns)),
            where=self._get_date_condition(start_date, stop_date),
        )[0]
