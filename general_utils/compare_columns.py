
def compare_cols(dfs):
    '''

        Compare a list of DataFrames to see if they differ in any column. Case they do, provide a list of the
        unique columns that each different DataFrame has. 

            Args:
                - dfs (list): A list of dataframes to be compared.

            Returns:
                - None: Prints output that provides valuable information about the DataFrame. 


    '''

    all_columns_set = set().union(*[df.columns for df in dfs])
    common_columns_set = set(dfs[0].columns)

    for df in dfs[1:]:
        common_columns_set &= set(df.columns)

    for df in dfs[1:]:
        if set(df.columns) != common_columns_set:
            print("> The dataframes do not have the same columns.\n")
            # Find unique columns for each dataframe
            for i, df in enumerate(dfs):
                unique_columns_set = all_columns_set - set(df.columns)
                print(
                    f"~ Unique columns in dataframe {i}: {unique_columns_set}")
            break
    else:
        print("> The dataframes have the same columns.\n\n")
