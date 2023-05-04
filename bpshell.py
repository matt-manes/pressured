from datetime import datetime

import plotly.graph_objects
from argshell import ArgShellParser, Namespace, with_parser
from databased import DataBased, DBShell, dbparsers
from pathier import Pathier

from pressured import Pressured

root = Pathier(__file__).parent


def get_reading_parser() -> ArgShellParser:
    parser = ArgShellParser()
    parser.add_argument(
        "systolic", type=int, help=""" The top number of the reading. """
    )
    parser.add_argument(
        "diastolic", type=int, help=""" The bottom number of the reading. """
    )
    parser.add_argument("-p", "--pulse", type=int, default=0, help=""" Pulse rate. """)
    return parser


def get_date_parser() -> ArgShellParser:
    parser = ArgShellParser()
    parser.add_argument(
        "--start",
        type=str,
        default=None,
        help=""" Don't plot data before this date.
        Required format: month_digit/day_digit/4_digit_year""",
    )
    parser.add_argument(
        "--stop",
        type=str,
        default=None,
        help=""" Don't plot data after this date.
        Required format: month_digit/day_digit/4_digit_year""",
    )
    return parser


def convert_to_datetime(args: Namespace) -> Namespace:
    convert = lambda date: datetime.strptime(date, "%m/%d/%Y")
    if args.start:
        args.start = convert(args.start)
    if args.stop:
        args.stop = convert(args.stop)
    return args


class BPShell(DBShell):
    intro = "Starting bpshell (enter help or ? for command info)..."
    prompt = "bpshell>"
    dbpath = root / "blood_pressure.db"

    @with_parser(get_reading_parser)
    def do_reading(self, args: Namespace):
        """Add a reading to the database."""
        with Pressured(self.dbpath) as db:
            db.add_reading(args.systolic, args.diastolic, args.pulse)

    @with_parser(get_date_parser, [convert_to_datetime])
    def do_averages(self, args: Namespace):
        """Display table averages."""
        with Pressured(self.dbpath) as db:
            averages = db.get_averages(args.start, args.stop)
        print(Pressured.data_to_string([averages]))

    @with_parser(get_date_parser, [convert_to_datetime])
    def do_plot(self, args: Namespace):
        """Plot readings data."""
        fig = plotly.graph_objects.Figure()
        Scatter = plotly.graph_objects.Scatter
        with Pressured(self.dbpath) as db:
            readings = db.get_readings(args.start, args.stop)
            averages = db.get_averages(args.start, args.stop)
        sys_average = [averages["systolic"]] * len(readings)
        dys_average = [averages["diastolic"]] * len(readings)
        pulse_pressure = readings["systolic"] - readings["diastolic"]
        annotation_x = (
            readings["date"].min()
            + (readings["date"].max() - readings["date"].min()) * 0.5
        )

        fig.add_trace(
            Scatter(x=readings["date"], y=readings["systolic"], name="Systolic")
        )
        fig.add_annotation(
            x=annotation_x,
            y=readings["systolic"].max(),
            text=f"Systolic min: {readings['systolic'].min()} Systolic max: {readings['systolic'].max()}",
        )
        fig.add_trace(
            Scatter(x=readings["date"], y=readings["diastolic"], name="Diastolic")
        )
        fig.add_annotation(
            x=annotation_x,
            y=readings["diastolic"].max(),
            text=f"Diastolic min: {readings['diastolic'].min()} Diastolic max: {readings['diastolic'].max()}",
        )
        fig.add_trace(
            Scatter(x=readings["date"], y=sys_average, name="Average Systolic")
        )
        fig.add_annotation(
            x=annotation_x,
            y=sys_average[0],
            text=f"Systolic average: {sys_average[0]}",
        )
        fig.add_trace(
            Scatter(x=readings["date"], y=dys_average, name="Average Diastolic")
        )
        fig.add_annotation(
            x=annotation_x,
            y=dys_average[0],
            text=f"Diastolic average: {dys_average[0]}",
        )
        fig.add_trace(
            Scatter(x=readings["date"], y=pulse_pressure, name="Pulse Pressure")
        )
        fig.add_annotation(
            x=annotation_x,
            y=pulse_pressure.max(),
            text=f"Pulse pressure min: {pulse_pressure.min()} Pulse pressure max: {pulse_pressure.max()}",
        )
        ave_pulse_pressure = [pulse_pressure.mean()] * len(readings)
        fig.add_trace(
            Scatter(
                x=readings["date"], y=ave_pulse_pressure, name="Average Pulse Pressure"
            )
        )
        fig.add_annotation(
            x=annotation_x,
            y=ave_pulse_pressure[0],
            text=f"Average pulse pressue: {round(ave_pulse_pressure[0])}",
        )
        fig.update_layout(
            xaxis_title=f"Date ({readings['date'].min().strftime('%m/%d/%Y')}-{readings['date'].max().strftime('%m/%d/%Y')})",
            yaxis_title="mmHg",
        )
        fig.update_annotations(font={"color": "red", "size": 18})
        fig.show()


if __name__ == "__main__":
    # Create db file if it doesn't exist before BPShell tries to scan for one.
    Pressured()
    BPShell().cmdloop()
