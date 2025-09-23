import pandas as pd
import settings
import classes.group_objects as gr_obs



def make_groups():

    excel = settings.EXCEL_GROUPS

    excel_file = pd.read_excel(excel)

    group_headers = ["Groep","Naam"]
    group_list = []
    lookup_group = {}

    for index, row in excel_file.iterrows():
        values_group = [row[header] for header in group_headers]
        group_list.append(values_group)
        lookup_group[values_group[1]] = values_group[0]

    groups = {}

    for row in group_list:
        number, name = row
        if number not in groups:
            groups[number] = gr_obs.Group(number)
        # Append name to the existing group object
        groups[number].members.append(name)

    #groeplijst is de originele excel
    #loopupgroup is voor een naam te vinden bij welke groep
    #groups zijn objecten die een lijst namen hebben en een veld met de nummer van de groep
    groups_info = [group_list,lookup_group,groups]

    return (groups_info)

















