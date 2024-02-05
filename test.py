import random
from datetime import datetime

from pathier import Pathier

from pressured import Pressured

root = Pathier(__file__).parent
testdb_path = root / "test.db"


def test_add_reading():
    if not testdb_path.exists():
        with Pressured(testdb_path) as db:
            for _ in range(100):
                db.add_reading(
                    random.randint(120, 160),
                    random.randint(50, 90),
                    random.randint(60, 90),
                )


def test_get_readings():
    with Pressured(testdb_path) as db:
        readings = db.get_readings()
        assert len(readings) > 0
        readings = db.get_readings(stop_date=datetime.fromtimestamp(0))
        assert len(readings) == 0


def test_get_averages():
    with Pressured(testdb_path) as db:
        averages = db.get_averages()
        assert 120 < averages["systolic"] < 160
        assert 50 < averages["diastolic"] < 90
        assert 60 < averages["pulse"] < 90
