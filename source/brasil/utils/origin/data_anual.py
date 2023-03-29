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
        "Volumen Total Bruto (TN)": []
    }

    for df in dfs:

        if df is not None and not df.empty:

            transition_dic['NCM'].append(
                ''.join(df['Código NCM'].unique().astype(str).tolist()))

            transition_dic['Año'].append(df["Fecha"].iloc[0].year)

            volumenTotalImportacionTn = (df['Kgs. Brutos'].sum()/1000).round(2)

            transition_dic['Volumen Total Bruto (TN)'].append(
                volumenTotalImportacionTn)

            print(
                f"- {df['Código NCM'].iloc[0]} ({df['Fecha'].iloc[0].year}) appended.")

    print(f"- - - - - - - - - - - - - - - - - - -\n> Dictionary:\n")

    for key, values in transition_dic.items():
        print(f"- {key}: {values}\n")

    annual_total_volume = pd.DataFrame.from_records(transition_dic)

    return annual_total_volume
