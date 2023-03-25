import os
import gspread as gs

CURRENT_WD = os.getcwd()
COUNTRY_WD = (os.path.basename(CURRENT_WD).split('/')[-1]).upper()
CREDENTIALS = '../../service-credentials.json'


def export_API(df):
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
        df_values = df.values.tolist()
        # sh.values_append(f'{COUNTRY_WD}', {'valueInputOption': 'RAW'}, {
        #     'values': df_values})
        ws.append_rows([df.columns.values.tolist()] +
                       df.values.tolist())
        print("> Spreadsheet modified.\n")
        print('_________________________________________________________________\n')
    except gs.exceptions.WorksheetNotFound:
        # Code if spreadsheet doesn't exist:
        print("Spreadsheet doesn't exist: Creating the new worksheet...\n\n- - - - - - - - - -\n")
        sh.add_worksheet(title=f"{COUNTRY_WD}", rows=100, cols=12)
        ws = sh.worksheet(f'{COUNTRY_WD}')
        ws.update([df.columns.values.tolist()] +
                  df.values.tolist())
        print("> Spreadsheet created.\n")
        print('_________________________________________________________________\n')
