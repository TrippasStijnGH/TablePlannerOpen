import sqlite3
import os

import settings

import repo.registrations as r_registrations

import classes.registration_objects as Iobs

import repo.participants as r_participants

import repo.events as Revents

import repo.DMs as r_DMs

import pandas as pd

#saves all participants from the excel file to the database
#if this is an amended list after a previous planning attement
#it will first delete all previous registrations in the db and
#again enter those of the excel file

def save_participants():

    excel = settings.EXCEL_REGISTRATIONS


    excel_file = pd.read_excel(excel)

    event_code = os.path.splitext(os.path.basename(excel))[0]

    # kijkt of er al inschrijvingen zijn met deze eventId en verwijdert ze allemaal
    test_and_delete(event_code)

    # Go through the data and create new participants and registrations
    for _, row in excel_file.iterrows():

        create_new_particpant(row['FirstName'], row['LastName'], row['Email'], row['BirthDate'].strftime('%Y-%m-%d'), row['Postcode'])

        partic_id = r_participants.get_participant_id_by_email(row['Email'])

        DM = row['DMPreference']

        pref_DM_id = 0

        notes = row['Notes']

        if isinstance(DM, str) and DM != "No preference":
            first_name, last_name = DM.split(maxsplit=1)
            first_name = first_name.strip()
            last_name = last_name.strip()
            pref_DM_id = r_DMs.get_DM_id(first_name, last_name)


        r_registrations.make_registration(event_code, partic_id, pref_DM_id, notes)



def create_new_particpant(first_name, last_name, email, date_birth, postcode=None):

    if not r_participants.known_email(email):

        r_participants.make_new_participant(first_name, last_name, email, date_birth, postcode)



def known_name(name):
    result = False
    if name in r_participants.return_all_names():
        return True
    return result


### Inschrijving functies

def known_registration(participant_id):
    return r_registrations.find_registration(participant_id)


def filter_to_string(value):
    answer = " "
    if not isinstance(value,float):
        answer = value
    return answer


def test_and_delete(event_id):
     r_registrations.delete_registration(event_id)








