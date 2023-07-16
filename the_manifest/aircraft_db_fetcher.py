import sys
import sqlite3
from sqlite3 import Connection, Cursor


def control_tower(new_session: bool = True) -> None:
    """
    Our main function; Sets up the Database Utilities, Takes user input, Calls CRUD functions
    :param new_session: A toggle for the user menu display based on where this function is called
    :return: None
    """

    db_connection: Connection = sqlite3.connect('Aircraft Database.db')

    cursor: Cursor = db_connection.cursor()

    if new_session:  # Present options only once for everytime the user runs the program
        crud_action: str = input(
            '\tType "SEARCH" to search for a specific aircraft\'s profile by name: \n\tType "ALL" to search for '
            'all available aircraft profiles: \n\tType "ADD" to Add an aircraft to the database: \n\tType '
            '"UPDATE" to edit information on a specific aircraft in the database: \n\tType "DELETE" to delete a '
            'specific aircraft from the aircraft database: \n\tType "X" to Exit: ').strip().upper()
    else:
        crud_action: str = input('\n\tPlease state your desired task and Press Enter: ').strip().upper()

    print('\n\t\t\t\t\t>>>>>>>>>>>>>>>>>>>> And we have lift off >>>>>>>>>>>>>>>>>>\n')

    # CREATE
    if crud_action == "ADD":

        name_of_aircraft: str = input('\n\tName of Aircraft & Press Enter').strip()

        while name_of_aircraft == '':  # Enforcing non-NULLABILITY
            print('\n***Name is a required field!***')
            name_of_aircraft: str = input('\n\tName of Aircraft & Press Enter: ').strip()

        role: str = input('\n\tRole / Use of Aircraft & Press Enter: ').strip()

        while role == '':  # Enforcing non-NULLABILITY
            print('\n***Role is a required field!***')
            role: str = input('\n\tRole / Use of Aircraft & Press Enter: ').strip()

        country_of_origin: str = input('\n\tCountry of Origin of Aircraft & Press Enter: ')

        manufacturer: str = input('\n\tManufacturer of Aircraft & Press Enter: ').strip()

        while manufacturer == '':  # Enforcing non-NULLABILITY
            print('\n***Manufacturer is a required field!***')
            manufacturer: str = input('\n\tManufacturer of Aircraft & Press Enter: ').strip()

        first_flight: str = input('\n\tDate of First Flight of Aircraft & Press Enter: ')
        introduced: str = input('\n\tDate of Introduction of Aircraft & Press Enter: ')
        retired: str = input('\n\tDate of Retirement of Aircraft & Press Enter: ')
        status: str = input('\n\tStatus (e.g. Retired, Active etc ) of Aircraft & Press Enter: ')
        primary_user: str = input('\n\tPrimary User of Aircraft & Press Enter: ')
        production_years: str = input('\n\tProduction Years (e.g. 1971-1975) of Aircraft & Press Enter: ')
        number_built: str = input('\n\tNumber of Aircraft Built & Press Enter: ')
        developed_from: str = input('\n\tDeveloped From (if Aircraft was inspired by an earlier aircraft) & Press '
                                    'Enter: ')
        variants: str = input('\n\tVariants of Aircraft (names of the Makes/Models) & Press Enter: ')

        # We collect all the user input into an array which will serve as an *arg for the db insert function
        aircraft_record_info: [str] = [name_of_aircraft, role, country_of_origin, manufacturer, first_flight,
                                       introduced, retired, status, primary_user, production_years, number_built,
                                       developed_from, variants]

        create_record(db_connection, aircraft_record_info)

    # READ
    elif crud_action in ["SEARCH", "ALL"]:

        aircraft_name: str = ''

        if crud_action == "SEARCH":  # If the user wants to find a specific aircraft by name
            aircraft_name = input('\n\tType the name of the aircraft you want to search for & Press Enter: ')

        aircraft_data: [] = read_record(cursor, aircraft_name)

        if aircraft_name:  # In case the user is searching for an aircraft by name

            if len(aircraft_data) == 0:
                print('******************************************************************************')
                print(f'\t\tMAYDAY! Sorry, we have no aircraft named "{aircraft_name}" in our database.')
                print('******************************************************************************')

            elif len(aircraft_data) > 1:  # The user might search with an incomplete name and find many records (Boeing)
                print(f'\tWe have {len(aircraft_data)} aircraft names containing the name "{aircraft_name}" in our '
                      f'database.\n\tTheir Record Numbers, Names and Roles are listed below:\n')

                [print('\t', list(aircraft[:3])) for aircraft in aircraft_data]  # Display all the matching aircraft

            else:
                print(f'\n\tAircraft Profile for "{aircraft_name.title().strip()}" is displayed below:\n\t')

                [print('\t', list(aircraft)) for aircraft in aircraft_data]

        else:  # If the user hasn't specified an aircraft name, we assume they want to find all the available aircraft
            [print('\t', list(aircraft)) for aircraft in aircraft_data]

    # UPDATE
    elif crud_action == "UPDATE":

        column_headers: [str] = ['AIRCRAFT_NAME', 'ROLE', 'NATIONAL_ORIGIN', 'MANUFACTURER', 'FIRST_FLIGHT',
                                 'INTRODUCTION', 'RETIRED', 'STATUS', 'PRIMARY_USER', 'PRODUCED',
                                 'NUMBER_BUILT', 'DEVELOPED_FROM', 'VARIANTS']

        update_target: str = input("\nWhat is the name of the aircraft you would like to update?: ").strip()

        update_header: str = input(f"\nWhat would you like to update (choose one from the list below): \n"
                                   f"\n{column_headers}\t\t\t\n\n: ").upper()

        while update_header not in column_headers:
            print(f'\n\t\tWe have no column named "{update_header}".')
            update_header: str = input(f"\nWhat would you like to update (choose one from the list below): \n"
                                       f"\n{column_headers}\t\t\t\n\n: ").upper()

        updated_value: str = input("\nWhat would you like to update it to: ").strip()

        while updated_value == '':
            if update_header not in ['AIRCRAFT_NAME', 'ROLE', 'MANUFACTURER']:
                updated_value: str = 'NULL'
            elif update_header in ['AIRCRAFT_NAME', 'ROLE', 'MANUFACTURER']:
                print(f'\n***{update_header} is a required field!***')
                updated_value: str = input(f"\nWhat would you like to update {update_target.title()}'s {update_header} "
                                           f"to: ").strip()

        update_record(db_connection, update_header, updated_value, update_target)

    # DELETE
    elif crud_action == "DELETE":

        record_to_delete: str = input('\n\tType the name of aircraft you would like to delete: ')
        delete_record(db_connection, record_to_delete)

    elif crud_action == "X":
        print('\nCHEERS...')
        sys.exit()

    else:
        print('\nPlease type one of the words provided in the task choices above.')
        control_tower(False)

    # Our looping point
    proceed_or_exit: str = input('\nType "X" to Exit or "C" to Continue: ').strip().upper()

    if proceed_or_exit == "C":
        control_tower(False)
    elif proceed_or_exit == "X":
        print('\nCheers...')
        sys.exit()
    else:
        print('\n\t***Invalid input***')

    db_connection.close()


def create_record(db_connect, new_aircraft_profile: []) -> None:
    """
    Inserting a new record in the database
    :param db_connect: Our Database connection object
    :param new_aircraft_profile: An array containing the entire aircraft profile
    :return: None
    """

    check_for_match: bool = True

    # Checking for a duplicate aircraft name
    matching_record: int = check_for_record(db_connect, new_aircraft_profile[0], check_for_match)

    if matching_record != 1:
        # Accounting for Non-Required Fields' Empty String '' Inputs & Converting them to 'NULL' in the DB
        for column, cell in enumerate(new_aircraft_profile):
            if cell == '':
                new_aircraft_profile.remove(cell)
                cell = 'NULL'
                new_aircraft_profile.insert(column, cell)

        db_connect.execute("INSERT INTO Aircraft_Profiles VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           new_aircraft_profile)
        db_connect.commit()
        print(f'\n\tYou have successfully added the aircraft "{new_aircraft_profile[0]}" to the database!')


def read_record(db_connect, aircraft_name: str = None) -> []:
    """
    Search for a specific aircraft or all aircraft if no aircraft name has been specified
    :param db_connect: Our Database connection object
    :param aircraft_name: Optional parameter for when the user wants to search for a specific aircraft name / names
    :return: An array of one aircraft's full profile or various arrays of various aircraft profiles
    """

    if aircraft_name:  # Search for this aircraft or similar if the name provided by the user is not complete
        profile = db_connect.execute("SELECT rowid, * FROM Aircraft_Profiles WHERE AIRCRAFT_NAME LIKE (?)",
                                     (f'%{aircraft_name}%',))

    # If aircraft name has not been specified, search for all aircraft on the database
    else:
        profile = db_connect.execute("SELECT rowid, AIRCRAFT_NAME, ROLE FROM Aircraft_Profiles")
        print('\n\tAll the Record Numbers, Names and Roles of all the aircraft in the database are listed below:\n\t')

    return list(profile)


def update_record(db_connect, update_target_column: str, the_update: str, update_target_record: str) -> None:
    """
    Update any information on a particular aircraft profile available on the database
    :param db_connect: The database connection object
    :param update_target_column: The column we want to update
    :param the_update: The new information to update the information in the above specified column
    :param update_target_record: Name of aircraft to update
    :return: None
    """

    # Can't update what doesn't exist
    record_available: int = check_for_record(db_connect, update_target_record)

    if record_available != 0:
        db_connect.execute(f"UPDATE Aircraft_Profiles SET {update_target_column} = '{the_update}' "
                           f"WHERE AIRCRAFT_NAME LIKE '{update_target_record}'")
        db_connect.commit()
        print(f'\n\tYou have successfully updated the {update_target_column} for the aircraft "{update_target_record}" '
              f'to "{the_update}"!.')


def delete_record(db_connect, delete_target: str) -> None:
    """
    Delete function for removing a specific record by name from the database
    :param db_connect: Our database connection object
    :param delete_target: The name of the aircraft being deleted
    :return: None
    """

    # Can't delete what doesn't exist
    record_available: int = check_for_record(db_connect, delete_target)

    if record_available != 0:
        # The nested query statement works as a filter and returns the first match's row ID to avoid deleting all
        # matches
        db_connect.execute("DELETE FROM Aircraft_Profiles WHERE rowid = ("
                           "SELECT MIN(rowid) FROM Aircraft_Profiles WHERE AIRCRAFT_NAME LIKE (?))",
                           (f"%{delete_target}%",))
        db_connect.commit()
        print(f'\n\tYou have successfully deleted the profile for the aircraft "{delete_target}" from the database!.')


def check_for_record(db_connect, record_name: str, duplicate_check: bool = False) -> int:
    """
    A utility function for checking if the record being queried exists. This is useful for creating, updating & deleting
    :param db_connect: Our database connection object
    :param record_name: The name of the aircraft name being queried
    :param duplicate_check: An optional parameter for the record creating function to distinguish CLI output
    :return: An integer which determines if the record in question exists
    """

    record_check = db_connect.execute("SELECT * FROM Aircraft_Profiles WHERE AIRCRAFT_NAME LIKE (?)",
                                      (f'{record_name}',))

    if duplicate_check:
        if len(list(record_check)) >= 1:  # Because at least one already exists, so we can't create it
            print(f'\n\t\tWe already have a profile for the aircraft "{record_name}" in our database. Use the update '
                  f'option if you want to add or edit information on this aircraft.')
            return 1
    else:
        if len(list(record_check)) == 0:  # Because none such record exists, so we can't update or delete it
            print(f'\n\t\tSorry, we have no aircraft named "{record_name}" in our database.')
            return 0

