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

import csv
import meraki
import datetime as dt

from credentials import API_KEY, organization_id
from serial_device_name import device_name_dict

print('Getting Device Name / Serial list')
device_name_serial_dict = device_name_dict(API_KEY, organization_id)
print('Printing Device Name / Serial list')
print(device_name_serial_dict)


# Function for interface status:
def get_interface_status():
    dashboard = meraki.DashboardAPI(API_KEY, suppress_logging=True)
    interface_status = dashboard.organizations.getOrganizationUplinksStatuses(organization_id, total_pages='all',
                                                                              timespan=60)
    print('Writing File for Interface Status')
    with open(f'csv_instant_collector/instant_interface_status_{dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv', 'w', newline='') as f:
        writer_a = csv.writer(f)
        writer_a.writerow(['Name', 'Serial_ID', 'Interface_WAN1', 'Interface_WAN1_Status', 'Interface_WAN2',
                           'Interface_WAN2_Status', 'Current_Date', 'Current_Time', 'Meraki_Time'])
        for n in interface_status:
            try:
                if len(n['uplinks']) == 1:
                    writer_a.writerow(
                        (device_name_serial_dict[n['serial']],
                         n['serial'],
                         n['uplinks'][0]['interface'],
                         n['uplinks'][0]['status'], 'wan2', 'not active',
                         n['lastReportedAt'][0:10],
                         n['lastReportedAt'][11:19],
                         n['lastReportedAt'])
                    )
                    print(f"Processing information for device: {device_name_serial_dict[n['serial']]}")
                else:
                    writer_a.writerow(
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
                    print(f"Processing information for device: {device_name_serial_dict[n['serial']]}")
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
    with open(f'csv_instant_collector/instant_loss_latency_{dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv', 'w', newline='') as f:
        writer_b = csv.writer(f)
        writer_b.writerow(
            ['Name', 'Serial_ID', 'Uplink', 'IP', 'Loss_Percent', 'Latency', 'Current_Date', 'Current_Time',
             'Meraki_Time'])
        for m in loss_latency:
            try:
                writer_b.writerow((device_name_serial_dict[m['serial']],
                                  m['serial'],
                                  m['uplink'],
                                  m['ip'],
                                  m['timeSeries'][0]['lossPercent'],
                                  m['timeSeries'][0]['latencyMs'],
                                  m['timeSeries'][0]['ts'][0:10],
                                  m['timeSeries'][0]['ts'][11:19],
                                  m['timeSeries'][0]['ts']))
                print(f"Processing information for device: {device_name_serial_dict[m['serial']]}")
            except IndexError:
                print('There was and index error')


get_interface_status()
get_interface_loss_latency()
