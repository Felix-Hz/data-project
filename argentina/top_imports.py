import pandas as pd

def top_importadores(dfs):

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

            if (data['Kgs. Netos'].sum() > 15000):

                volumenTotalCompania = (data['Kgs. Netos'].sum()/1000).round(2)

                company_dic['Importador'].append(company)
                
                company_dic['Año'].append(round((pd.DatetimeIndex(data["Fecha"].unique()))[0].year))

                company_dic['Precio Promedio'].append((data['U$S Unitario'].mean().round(2))*1000)

                company_dic['Volumen Total (TN)'].append(volumenTotalCompania)
                
                company_dic['Participacion'].append(f"{round((volumenTotalCompania / volumenTotalImportacionTn) * 100)}%")

                print(f"- Done with: {company} ({df['Fecha'][4].year}) ")

        transition_df = pd.DataFrame.from_records(company_dic)
        transition_df = transition_df.sort_values(by="Volumen Total (TN)", ascending=False)
        transition_df_head = transition_df.head(3)

        # print(transition_df)

        companies_df = companies_df.append(transition_df_head, ignore_index=False)

    print("~~~~~~~~~~~~~~~~~~~\n> Current dataframe of the top 3 importers of each year:")

    
    return companies_df
