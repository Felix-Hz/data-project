import pandas as pd


def top_importadores(dfs):
    '''

        Analyzes the top three importers for each year of a given NCM by calculating their mean purchase price, total volume in tons,
        and market percentage participation.

            Args:
                - dfs (List[pd.DataFrame]): A list of dataframes to filter the data.

            Returns:
                - DataFrame: A dataframe containing the top three most performant companies for each year.
                    - Año (int): The year the data pertains to.
                    - Importador (str): The name of the company.
                    - Precio Promedio (float): The mean price of purchase.
                    - Volumen Total (TN) (float): The total volume in tons.
                    - Participacion (str): The market percentage participation, rounded to the nearest whole number with the '%' symbol appended.

    '''

    companies_df = pd.DataFrame()

    for i in range(len(dfs)):
        df = dfs[i]

        volumenTotalImportacionTn = (df['Kgs. Netos'].sum()/1000).round(2)

        company_dic = {
            "Año": [],
            "Importador": [],
            "Precio Promedio": [],
            "Volumen Total (TN)": [],
            "Participacion": []
        }

        for company in df['Importador'].unique():

            data = df[df['Importador'] == f"{company}"]

            if (data['Kgs. Netos'].sum() > 1500):

                volumenTotalCompania = (data['Kgs. Netos'].sum()/1000).round(2)

                company_dic['Importador'].append(company)

                company_dic['Año'].append(
                    round((pd.DatetimeIndex(data["Fecha"].unique()))[0].year))

                company_dic['Precio Promedio'].append(
                    (data['U$S Unitario'].mean().round(2))*1000)

                company_dic['Volumen Total (TN)'].append(volumenTotalCompania)

                company_dic['Participacion'].append(
                    f"{round((volumenTotalCompania / volumenTotalImportacionTn) * 100)}%")

                print(f"- Done with: {company} ({df['Fecha'].iloc[0].year}) ")

        transition_df = pd.DataFrame.from_records(company_dic)
        transition_df = transition_df.sort_values(
            by="Volumen Total (TN)", ascending=False)
        transition_df_head = transition_df.head(3)

        # print(transition_df)

        companies_df = companies_df.append(
            transition_df_head, ignore_index=False)

    print("~~~~~~~~~~~~~~~~~~~\n> Current dataframe of the top 3 importers of each year:")

    return companies_df
