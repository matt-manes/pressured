import random
import time
from datetime import datetime

from pathier import Pathier
from printbuddies import Spinner

from pressured import Pressured

root = Pathier(__file__).parent
testdb_path = root / "test.db"

spinner = Spinner()


def test_add_reading():
    if not testdb_path.exists():
        with Pressured(testdb_path) as db:
            for _ in range(100):
                db.add_reading(random.randint(120, 160), random.randint(50, 90))
                spinner.display()
                time.sleep(1)


def test_get_readings():
    with Pressured(testdb_path) as db:
        readings = db.get_readings()
        assert len(readings) > 0
        readings = db.get_readings(stop_date=datetime.fromtimestamp(0))
        assert len(readings) == 0


def test_get_averages():
    with Pressured(testdb_path) as db:
        averages = db.get_averages()
        assert averages[0] > 120
        assert averages[0] < 160
        assert averages[1] > 50
        assert averages[1] < 90
