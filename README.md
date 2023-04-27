# pressured

Track and plot blood pressure measurements.

## Installation

Install with:

<pre>
git clone https://github.com/matt-manes/pressured
pip install -r requirements.txt
</pre>

## Usage

Launch `bpshell.py` in a terminal.<br>
Primary commands are `reading` and `plot`.<br>
`reading` takes two numbers, the systolic and diastolic blood pressure numbers.<br>
The command will add them to the database along with the current date.<br>
`plot` will plot the blood pressure data from the database along with the pulse pressure and averages in a browser window.
<pre>
bpshell>help reading
Add a reading to the database.
Parser help for reading:
usage: bpshell.py [-h] systolic diastolic

positional arguments:
  systolic    The top number of the reading.
  diastolic   The bottom number of the reading.

options:
  -h, --help  show this help message and exit
  
bpshell>help plot
Plot readings data.
Parser help for plot:
usage: bpshell.py [-h] [--start START] [--stop STOP]

options:
  -h, --help     show this help message and exit
  --start START  Don't plot data before this date. Required format: month_digit/day_digit/4_digit_year
  --stop STOP    Don't plot data after this date. Required format: month_digit/day_digit/4_digit_year
</pre>
