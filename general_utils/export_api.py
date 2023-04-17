import os
import gspread as gs

CURRENT_WD = os.getcwd()
COUNTRY_WD = (os.path.basename(CURRENT_WD).split('/')[-1]).upper()
CREDENTIALS = '../../service-credentials.json'


def export_API(df):
    '''
    
        Export a DataFrame to a Google Sheet:

        This function checks if a sheet for the DataFrame's country exists. If it does, the function appends the new data to the existing sheet. 
        If the sheet doesn't exist, the function creates one, naming the sheet after the directory where the DataFrame is located. Note that this 
        function requires personal credentials from Google Cloud Services to be passed in.

                Args:
                    - df (pandas DataFrame): the DataFrame to be exported to Google Sheets.

                Returns:
                    - None: this function does not return anything, but exports the DataFrame to a Google Sheet.

    '''

    gc = gs.service_account(filename=CREDENTIALS)
    sh = gc.open('SouthAmerica_10years')

    worksheet_list = sh.worksheets()

    print("\n__________________________ ~ EXPORT ~ __________________________\n")
    print(
        f"\033[1m> Las hojas del excel actualmente son:\033[0m\n\n {worksheet_list}\n\n- - - - - - - - - -\n")
    try:
        ws = sh.worksheet(f'{COUNTRY_WD}')
        # Code if spreadsheet exists:
        print(
            "Spreadsheet exists: Modifying existing working sheet...\n\n- - - - - - - - - -\n")
        # ws.clear()
        ws.append_rows([df.columns.values.tolist()] +
                       df.values.tolist())
        print("> Spreadsheet modified.\n")
        print('_________________________________________________________________\n')
    except gs.exceptions.WorksheetNotFound:
        # Code if spreadsheet doesn't exist:
        print("Spreadsheet doesn't exist: Creating the new worksheet...\n\n- - - - - - - - - -\n")
        sh.add_worksheet(title=f"{COUNTRY_WD}", rows=100, cols=12)
        ws = sh.worksheet(f'{COUNTRY_WD}')
        ws.append_rows([df.columns.values.tolist()] +
                       df.values.tolist())
        print("> Spreadsheet created.\n")
        print('_________________________________________________________________\n')
