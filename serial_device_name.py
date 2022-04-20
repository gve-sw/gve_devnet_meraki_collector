import meraki


from credentials import API_KEY, organization_id


def device_name_dict(_API_KEY,_organization_id):
    dashboard = meraki.DashboardAPI(_API_KEY, suppress_logging=True)
    interface_status = dashboard.organizations.getOrganizationUplinksStatuses(_organization_id, total_pages='all',
                                                                              timespan=60)
    # print(interface_status)
    list_of_serials = []
    for serial in interface_status:
        # print(serial['serial'])
        list_of_serials.append(serial['serial'])
    # print(list_of_serials)
    dictionary_serial_name = {}
    for serial in list_of_serials:
        response = dashboard.devices.getDevice(f'{serial}')
        try:
            # print(response['name'])
            print(f'Processing {response["name"]}')
            dictionary_serial_name[serial] = response['name']
        except KeyError:
            # print('No Name')
            print("Processing No Name")
            dictionary_serial_name[serial] = 'No Name'

    # print(dictionary_serial_name)
    return dictionary_serial_name


# print(device_name_dict(API_KEY, organization_id))
