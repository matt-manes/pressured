from datetime import datetime

from databased import DataBased
from pandas import DataFrame
from pathier import Pathier

root = Pathier(__file__).parent


class Pressured(DataBased):
    def __init__(self, dbpath: Pathier = root / "blood_pressure.db"):
        super().__init__(dbpath)
        self.init_table()

    def init_table(self):
        """Create pressure table."""
        self.create_table(
            "readings",
            [
                "systolic int",
                "diastolic int",
                "pulse int",
                "date timestamp",
                "pulse_pressure int",
            ],
        )

    def add_reading(self, systolic: int, diastolic: int, pulse: int):
        """Add blood pressure reading to database."""
        self.add_row(
            "readings",
            (systolic, diastolic, pulse, datetime.now(), systolic - diastolic),
        )

    def get_readings(
        self, start_date: datetime | None = None, stop_date: datetime | None = None
    ) -> DataFrame:
        """Returns readings as a DataFrame.
        The date range can be narrowed through 'start_date' and/or 'stop_date'."""
        if not start_date and not stop_date:
            readings = self.get_rows("readings", return_as_dataframe=True)
        else:
            query = "SELECT * FROM readings WHERE"
            if start_date and stop_date:
                condition = f"'{start_date}' < date and date < '{stop_date}'"
            elif start_date:
                condition = f"'{start_date}' < date"
            elif stop_date:
                condition = f"date < '{stop_date}'"
            readings = self.query(f"{query} {condition};")
            readings = [self._get_dict("readings", reading) for reading in readings]
            readings = DataFrame(readings)
        return readings

    def get_averages(
        self, start_date: datetime | None = None, stop_date: datetime | None = None
    ) -> dict:
        """Returns a dictionary of `readings` table averages.

        Averaging range can be specified with one or both 'start_date' and 'stop_date' params."""
        readings = self.get_readings(start_date, stop_date)
        averages = {
            col: round(readings[col].mean()) for col in readings if col != "date"
        }
        return averages
