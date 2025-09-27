import repo.tables as tafelRepo
import repo.registrations as inschrijvingenRepo
import repo.groups as r_groups
import services.planner as s_planner
import pandas as pd


def return_planning(event_id):
    group_number_lookup = r_groups.make_groups()[1]
    group_list = r_groups.make_groups()[0]
    group_members = list(map(lambda x: x[1], group_list))
    table_objects, remaining_participants = s_planner.plan_tafels(event_id)

    j = 1
    tables = []
    if len(remaining_participants) > 0:
        message = []
        message.append("!!!!!")
        message.append("Teweinig plaatsen!")
        message.append("Onderstaande spelers zijn niet toegekent")
        for participant in remaining_participants:
            message.append(participant.name)
        tables.append(message)

    for table_object in table_objects:
        i = 0
        table = []

        table.append(f"__{table_object.max_number + 1}__   >>>Tafel: {table_object.table_number} <<<")

        table.append(f"<{i}> > {table_object.DM_name} {table_object.DM}")
        i += 1

        for participant in table_object.participants:
            groepnummer = 0
            if participant.name in group_members:
                groepnummer = group_number_lookup[participant.name]
            happy = ":)"

            if participant.DM != table_object.DM_name:
                happy = ":("
            if participant.DM == "No preference":
                happy = "NP"

            table_row = f"<{i}> o {groepnummer} {j} {happy} {participant.name}"
            i += 1
            j += 1
            table.append(table_row)

        for empty_spots in range(table_object.max_number - len(table_object.participants)):
            table.append(f"<{i}> (x)")
            i += 1

        tables.append(table)




    planning = tables_to_string(tables)

    return planning


def tables_to_string(planning):
    planningString = ""

    for tafel in planning:
        for item in tafel:
            planningString += item +"\n"
        planningString += "\n"
    return planningString

def to_excel(event_id):
    table_objects, remaining_participants = s_planner.plan_tafels(event_id)
    output = []
    for table in table_objects:
        output.append(table.DM_name)
        for participant in table.participants:
            output.append(participant.name)
        output.append(" ")

    df = pd.DataFrame(output, columns=["Planning"])

    # Write the DataFrame to an Excel file
    df.to_excel("output.xlsx", index=False)


















