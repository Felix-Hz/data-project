import pandas as pd


def annual_data(dfs):
    '''

        Calculates the annual total volume for each NCM code in the provided DataFrames.

            Args:
                - dfs: a list of pandas DataFrames containing import data.

            Returns:
                - annual_total_volume: a pandas DataFrame with columns 'NCM', 'Año', and 'Volumen Total',
                where 'NCM' is the NCM code, 'Año' is the year of the data, and 'Volumen Total' is the
                annual total import volume in metric tons.

    '''

    transition_dic = {
        "NCM": [],
        "Año": [],
        "Volumen Total": []
    }

    last_iterated_year = None
    last_iterated_ncm = None

    for df in dfs:

        if df is not None and not df.empty and not pd.isnull(df["Fecha"].iloc[0].year):

            year = df['Fecha'].iloc[0].year

            transition_dic['NCM'].append(
                ''.join(df['Código SACH'].unique()))

            transition_dic['Año'].append(df["Fecha"].iloc[0].year)

            volumenTotalImportacionTn = (
                df['Cantidad Comercial'].sum()/1000).round(2)

            transition_dic['Volumen Total'].append(
                volumenTotalImportacionTn)

            last_iterated_year = year
            last_iterated_ncm = df['Código SACH'].iloc[0]

            print(f"- {last_iterated_ncm} ({last_iterated_year}) appended.")

        else:
            print(
                f"> Well, it seems there's no data for {last_iterated_ncm} ({last_iterated_year+1}). I'm sorry.")

    print("~~~~~~~~~~~~~~~~~~~\n> Transition dictionary:")

    for key, values in transition_dic.items():
        print(f"- {key}: {values}\n")

    annual_total_volume = pd.DataFrame.from_records(transition_dic)

    return annual_total_volume
