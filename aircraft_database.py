import sys
from the_manifest.aircraft_db_fetcher import control_tower


def script_summary() -> None:
    print('''
               ***----------------------------------------------------------------------------------------***
         \t***------------------------ DUMELANG means GREETINGS! ~ G-CODE -----------------------***
                     \t***------------------------------------------------------------------------***\n
              
        \t"AIRCRAFT-DATABASE" Version 1.0.0\n
        
        This database contains information on all the Civilian and Military Aircraft ever made,
        sourced from Wikipedia. The information is essentially in the form of profiles including categories
        such as Manufacturer, Country of Origin, Usage, Year Introduced etc.
        
        Cheers!!!
    ''')


def black_box() -> None:
    try:
        control_tower()
    except Exception as exp:
        if 'sqlite3' in str(exp):
            print(str(exp))
        elif FileNotFoundError:
            print('\t*** We\'re unable to locate your database file. Please make sure it is in the same directory as '
                  'this file and that its name is "Aircraft Database.db" ***')

        input('\nPress Enter to Exit & Try Again.')
        sys.exit(1)
    
    input('\nPress Enter to Exit.')


def main() -> None:
    script_summary()
    black_box()


if __name__ == '__main__':
    main()
