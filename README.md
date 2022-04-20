# gve_devnet_meraki_collector
Python scripts that collect data from a Meraki API call and stores it in a .csv file.
This script will collect information for the following: 

Meraki MX interface status
Meraki MX loss and latency information


The "historic_collector" will bulk-collect this information every period of time (set in the script, ideally every 1+ minute), and
the "instant_collector" will collect the same information every time the script is run showing the information collected at that instant.


## Contacts
* Max Acquatella

## Solution Components
* Meraki MX
* Python 

## Requirements
Cisco Meraki Administrator Token (can be obtained from the Meraki Dashboard)
See more here:

https://documentation.meraki.com/General_Administration/Other_Topics/Cisco_Meraki_Dashboard_API

Python environment installed in a machine that will collect the data.

## Installation/Configuration

Install python 3.6 or later

Clone this repository

Set up and activate a virtual environment (https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

```
python3 -m venv env
source env/bin/activate
```

Make sure to activate the virtual environment before proceeding to the next step


Install requirements.txt via command line

```
pip install -r requirements.txt
```

Add your organization's credentials to the credentials.py script and set the collector timer for the historic_collector script:

```python3

# Set time in MINUTES.SECONDS ,example:
time_in_min = 1.05


# Set your organization credentials:
API_KEY = '<your_api_key>'
organization_id = 'your_organization_id'
```
NOTE: the meraki API will not show information for less than one min.

Once everything is set up, you can run two scripts:

```bash
python3 historic_collector.py
```
```bash
python3 instant_collector.py
```

All the information collected will be stored in a .csv file in the csv_historic_collector directory for the historic 
collector script, and csv_instant_collector folder for the instant collector script.


## Usage

### Historic Collector

Run historic_collector.py from your command line:

```bash
python3 historic_collector.py
```

The code should generate two .csv files (historic_interface_status.csv and historic_loss_latency.csv) in the csv_historic_collector folder. 
The files will contain information similar to this:

Example for historic_collector.py - Interface Status:

![/IMAGES/image1.png](/IMAGES/image1.png)

The code will run every period set in "time_in_min", to stop the script just press Ctrl+C.
NOTE: MAKE SURE TO STOP THE SCRIPT! it will continue to collect data until stopped, and the generate files will consume space in your machine's disk.

### Instant Collector

Run instant_collector.py from your command line:

```bash
python3 instant_collector.py
```

The code should generate two .csv files (instant_interface_status_<date-time>.csv and instant_loss_latency_<date-time>.cvs) in the csv_instant_collector folder. 
The files will contain information similar to this:

Example for instant_collector.py - Interface Status:

![/IMAGES/image1.png](/IMAGES/image1.png)

The code will run only once and will show the information provided by the Meraki Dashboard in that instant. 

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.