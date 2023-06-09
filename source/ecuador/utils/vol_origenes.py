import pandas as pd


def analisis_origenes(dfs):
    '''

        Analyses the origin of imported goods over multiple years for given datasets.

            Parameters:
                - dfs (list): A list of pandas DataFrames containing data on imported goods.

            Returns:
                - DataFrame: Information on the origins of imported goods over multiple years.

    '''

    excel_new_data = pd.DataFrame()

    for df in dfs:

        volumenTotalImportacionTn = (df['Kgs. Netos'].sum()/1000).round(2)

        registro_volumen = {
            "NCM": [],
            "Año": [],
            "Pais": [],
            "No. Importaciones": [],
            "Volumen Total (TN)": [],
            "Participacion en Vol. Total": []
        }

        for pais in df['País de Origen'].unique():

            data = df[df['País de Origen'] == f"{pais}"]

            volumenTotalOrigen = (data['Kgs. Netos'].sum()/1000).round(2)

            if (data['Kgs. Netos'].sum() > 150000):

                registro_volumen['NCM'].append(
                    ''.join(df['NANDINA'].unique().astype(str).tolist()))

                registro_volumen['Año'].append(
                    str(data["Fecha"].iloc[0].year)[:4])

                registro_volumen['Pais'].append(pais)

                registro_volumen['No. Importaciones'].append(len(data))

                registro_volumen['Volumen Total (TN)'].append(
                    (data['Kgs. Netos'].sum()/1000).round(2))

                registro_volumen['Participacion en Vol. Total'].append(
                    f"{round(( volumenTotalOrigen / volumenTotalImportacionTn) *100)}%")

                print(
                    f"- Done with: {pais} in {data['NANDINA'].iloc[0]} ({data['Fecha'].iloc[0].year}).")

        transition_df = pd.DataFrame.from_records(registro_volumen).sort_values(
            'Volumen Total (TN)', ascending=False).reset_index(drop=True)
        transition_df = transition_df[[
            'NCM', 'Año', 'Pais', 'Volumen Total (TN)', "Participacion en Vol. Total", 'No. Importaciones']]
        excel_new_data = excel_new_data.append(
            transition_df, ignore_index=False)

    print("~~~~~~~~~~~~~~~~~~~\n> Current dataframe of the origins of each year:")

    return excel_new_data
