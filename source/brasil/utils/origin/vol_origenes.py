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

        volumenTotalImportacionTn = (df['Net weight'].sum()/1000).round(2)

        registro_volumen = {
            "NCM": [],
            "Año": [],
            "Pais": [],
            "No. Importaciones": [],
            "Volumen Total (TN)": [],
            "Participacion en Vol. Total": []
        }

        if (df['Fecha'].iloc[0].year == 2022):

            for pais in df['ORIGIN COUNTRY'].unique():

                data = df[df['ORIGIN COUNTRY'] == f"{pais}"]

                volumenTotalOrigen = (data['Net weight'].sum()/1000).round(2)

                if (data['Net weight'].sum() > 100000):

                    registro_volumen['NCM'].append(
                        ''.join(df['NCM'].unique().astype(str).tolist()))
                    registro_volumen['Año'].append(
                        str(data["Fecha"].iloc[0].year)[:4])
                    registro_volumen['Pais'].append(pais)
                    registro_volumen['No. Importaciones'].append(len(data))
                    registro_volumen['Volumen Total (TN)'].append(
                        (data['Net weight'].sum()/1000).round(2))
                    registro_volumen['Participacion en Vol. Total'].append(
                        f"{round(( volumenTotalOrigen / volumenTotalImportacionTn) *100)}%")
                    print(f"- Done with: {pais} ({df['Fecha'].iloc[0].year}) ")
            else:
                print(
                    f"- Country {pais} ({df['Fecha'].iloc[0].year}) doesn't pass the threshold.")

        elif (df['Fecha'].iloc[0].year == 2023):

            for pais in df['ORIGIN COUNTRY'].unique():

                data = df[df['ORIGIN COUNTRY'] == f"{pais}"]

                volumenTotalOrigen = (data['Net weight'].sum()/1000).round(2)

                if (data['Net weight'].sum() > 1000):

                    registro_volumen['NCM'].append(
                        ''.join(df['NCM'].unique().astype(str).tolist()))
                    registro_volumen['Año'].append(
                        df['Fecha'].iloc[0].year)
                    registro_volumen['Pais'].append(pais)
                    registro_volumen['No. Importaciones'].append(len(data))
                    registro_volumen['Volumen Total (TN)'].append(
                        (data['Net weight'].sum()/1000).round(2))
                    registro_volumen['Participacion en Vol. Total'].append(
                        f"{round(( volumenTotalOrigen / volumenTotalImportacionTn) *100)}%")
                    print(f"- Done with: {pais} ({df['Fecha'].iloc[0].year}) ")
                else:
                    print(
                        f"- Country {pais} ({df['Fecha'].iloc[0].year}) doesn't pass the threshold.")

        transition_df = pd.DataFrame.from_records(registro_volumen).sort_values(
            'Volumen Total (TN)', ascending=False).reset_index(drop=True)
        transition_df = transition_df[[
            'NCM', 'Año', 'Pais', 'Volumen Total (TN)', "Participacion en Vol. Total", 'No. Importaciones']]
        excel_new_data = excel_new_data.append(
            transition_df, ignore_index=False)

    print("~~~~~~~~~~~~~~~~~~~\n> Current dataframe of the origins of each year:")

    return excel_new_data
