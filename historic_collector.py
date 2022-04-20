# Copyright (c) 2020 Cisco and/or its affiliates.
#
# This software is licensed to you under the terms of the Cisco Sample
# Code License, Version 1.1 (the "License"). You may obtain a copy of the
# License at
#
#                https://developer.cisco.com/docs/licenses
#
# All use of the material herein must be in accordance with the terms of
# the License. All rights not expressly granted by the License are
# reserved. Unless required by applicable law or agreed to separately in
# writing, software distributed under the License is distributed on an "AS
# IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied.

import os
import csv
import meraki
from apscheduler.schedulers.blocking import BlockingScheduler

from credentials import API_KEY, organization_id, time_in_min
from serial_device_name import device_name_dict

device_name_serial_dict = device_name_dict(API_KEY, organization_id)


# Validate existing .csv, if not present create a new one
# For the Interface Status:
if os.path.isfile('csv_historic_collector/historic_interface_status.csv'):
    print("File Interface Status exist")
else:
    print("File Interface Status does not exist - creating file")
    with open(f'csv_historic_collector/historic_interface_status.csv', 'w', newline='') as f:
        writer_A = csv.writer(f)
        writer_A.writerow(['Name', 'Serial_ID', 'Interface_WAN1', 'Interface_WAN1_Status', 'Interface_WAN2',
                           'Interface_WAN2_Status','Current_Date','Current_Time', 'Meraki_Time'])

# For the Interface loss and latency
if os.path.isfile('csv_historic_collector/historic_loss_latency.csv'):
    print("File Interface Loss and Latency exist")
else:
    print("File does Interface Loss and Latency not exist - creating file")
    with open(f'csv_historic_collector/historic_loss_latency.csv', 'w', newline='') as f:
        writer_B = csv.writer(f)
        writer_B.writerow(['Name','Serial_ID','Uplink','IP','Loss_Percent','Latency','Current_Date','Current_Time', 'Meraki_Time'])


# Function for interface status:
def get_interface_status():
    dashboard = meraki.DashboardAPI(API_KEY, suppress_logging=True)
    interface_status = dashboard.organizations.getOrganizationUplinksStatuses(organization_id, total_pages='all',
                                                                              timespan=60)
    print('Writing File for Interface Status')
    with open('csv_historic_collector/historic_interface_status.csv', 'a', newline='') as _f:
        writer1 = csv.writer(_f)
        for n in interface_status:
            try:
                if len(n['uplinks']) == 1:
                    writer1.writerow(
                        (device_name_serial_dict[n['serial']],
                         n['serial'],
                         n['uplinks'][0]['interface'],
                         n['uplinks'][0]['status'], 'wan2', 'not active',
                         n['lastReportedAt'][0:10],
                         n['lastReportedAt'][11:19],
                         n['lastReportedAt'])
                    )
                else:
                    writer1.writerow(
                        (device_name_serial_dict[n['serial']],
                         n['serial'],
                         n['uplinks'][0]['interface'],
                         n['uplinks'][0]['status'],
                         n['uplinks'][1]['interface'],
                         n['uplinks'][0]['status'],
                         n['lastReportedAt'][0:10],
                         n['lastReportedAt'][11:19],
                         n['lastReportedAt'])
                    )
            except IndexError:
                pass


# interface_status()

# Function for interface loss and latency
def get_interface_loss_latency():
    dashboard = meraki.DashboardAPI(API_KEY, suppress_logging=True)
    loss_latency = dashboard.organizations.getOrganizationDevicesUplinksLossAndLatency(organization_id,
                                                                                       total_pages='all', timespan=60)
    print('Writing File for Loss and Latency')
    # print(loss_latency)
    with open('csv_historic_collector/historic_loss_latency.csv', 'a', newline='') as _f:
        writer2 = csv.writer(_f)
        for m in loss_latency:
            try:
                writer2.writerow((device_name_serial_dict[m['serial']],
                                  m['serial'],
                                  m['uplink'],
                                  m['ip'],
                                  m['timeSeries'][0]['lossPercent'],
                                  m['timeSeries'][0]['latencyMs'],
                                  m['timeSeries'][0]['ts'][0:10],
                                  m['timeSeries'][0]['ts'][11:19],
                                  m['timeSeries'][0]['ts'])
                                 )
            except IndexError:
                print('There was and index error')


# Build .csv files
# Collect info and build the .csv for Interface Status and Loss-Latency
scheduler = BlockingScheduler()
scheduler.add_job(get_interface_status, 'interval', minutes=time_in_min)
scheduler.add_job(get_interface_loss_latency, 'interval', minutes=time_in_min)
scheduler.start()

