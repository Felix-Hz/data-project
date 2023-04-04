
def compare_cols(dfs):
    '''

        Compare a list of DataFrames to identify any columns that are unique to one or more DataFrames:

            Args:
                dfs (list): A list of pandas DataFrames to be compared.

            Returns:
                None: Prints output that provides valuable information about the DataFrame.

                This function takes a list of pandas DataFrames and checks whether they have the same columns. If they have the same columns, it prints a message indicating that 
                all DataFrames have the same columns. If the DataFrames have different columns, it prints a message indicating that they do not have the same columns, and lists the 
                unique columns for each DataFrame that has them.

                For example, if dfs contains three DataFrames, and the first and second have columns A, B, and C, while the third has columns A, C, and D, the function will print a 
                message stating that the DataFrames do not have the same columns, and then list the unique columns for each DataFrame:

                    > The dataframes do not have the same columns.
                    > Unique columns in dataframe 0: {'D'}
                    > Unique columns in dataframe 2: {'B'}

    '''

    all_columns_set = set().union(*[df.columns for df in dfs])
    common_columns_set = set(dfs[0].columns)

    for df in dfs[1:]:
        common_columns_set &= set(df.columns)

    for df in dfs[1:]:
        if set(df.columns) != common_columns_set:
            print("> The dataframes do not have the same columns.\n")
            # Find unique columns for each dataframe
            unique_columns_set = all_columns_set - set(df.columns)
            print(
                f"~ Unique columns in dataframe: {unique_columns_set}")
            break
    else:
        print("> The dataframes have the same columns.\n\n")
