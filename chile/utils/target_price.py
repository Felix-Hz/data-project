import pandas as pd


def price_analysis(dfs, targets):
    '''
            Analyze the price for selected targets that are representative in a given NCM.

            Args:
                - dfs: 
                    Dataframes provided to filter the data.
                - targets:
                    Companies selected to be price representative. 

            Returns:
                - Dataframe: Minimum, Maximum, Mean, Median and Quartile distribution of the Unitary U$S price throughout a given set of years. 

    '''

    prices_describe = pd.DataFrame()

    for i in range(len(dfs)):
        df = dfs[i]

        price_dic = {
            "Año": [],
            "Importador": [],
            "Minimo": [],
            "Maximo": [],
            "Promedio": [],
            "Mediana": [],
            "Cuartiles": []
        }

        for target in targets:

            if not df[df['Importador'] == f"{target}"].empty:

                data = df[df['Importador'] == f"{target}"]

                price_dic['Importador'].append(target)

                price_dic['Año'].append(round((df.iloc[0]['Fecha'].year)))

                price_dic['Minimo'].append(
                    (data['U$S Unitario'].min().round(2))*1000)
                price_dic['Maximo'].append(
                    (data['U$S Unitario'].max().round(2))*1000)
                price_dic['Promedio'].append(
                    (data['U$S Unitario'].mean().round(2))*1000)
                price_dic['Mediana'].append(
                    (data['U$S Unitario'].median().round(2))*1000)
                price_dic['Cuartiles'].append(
                    f"Q1: {data['U$S Unitario'].quantile(0.25).round(2)*1000} | Q3: {data['U$S Unitario'].quantile(0.75).round(2)*1000}")

                print(
                    f"- Price analysis finished for: {target} ({df.iloc[0]['Fecha'].year}) ")

        transition_df = pd.DataFrame.from_records(price_dic)
        transition_df = transition_df[[
            'Importador', 'Año', 'Minimo', 'Cuartiles', 'Maximo', 'Mediana', 'Promedio']]

        prices_describe = prices_describe.append(
            transition_df, ignore_index=False)

    print(
        f"~~~~~~~~~~~~~~~~~~~\n> Price analysis for {', '.join(targets)} in the last {len(dfs)-1} years:")

    return prices_describe
