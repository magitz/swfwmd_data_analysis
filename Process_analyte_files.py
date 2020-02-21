# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

# %%
import glob
import pandas as pd


# %%
# Function to rename the "Recorded Value" column in the datasets to have the name of the analyte measured.
def rename_cols(df):
    if df['Analyte'].iloc[0] == 'Chlorophyll a (Total)':
        df=df.rename(columns={"Recorded Value": "ChlA Value"})
    elif df['Analyte'].iloc[0] == 'Nitrate-Nitrite (N) (Total)':
        df=df.rename(columns={"Recorded Value": "Nitrate Value"})
    else:
        print(f"Unexpected analyte value, {df['Analyte'].iloc[0]}, not renaming column)")
    return(df)


# %%
# May be usefull to have a list, but not really used.
file_list=[]

# Delete the All_sites dataframe if it exists.
try:
    del All_sites
except:
    pass


# %%
# This is the main part of the script that processes all the files.
# Files should be in a folder, with chlorophyll A files ending in ChlA.csv and corresponding
# nitrate files ending in Nitrate.csv.

for file in glob.glob("*ChlA.csv"):
    # Add current file to list of files processed
    file_list.append(file)
    
    # Process chlorophyll A file
    chlA_df = pd.read_csv(file)
    chlA_df = rename_cols(chlA_df)

    # Get name of Nitrate file and process that
    Nitrate_file=file[:-8] + "Nitrate.csv"
    Nitrate_df = pd.read_csv(Nitrate_file)
    Nitrate_df = rename_cols(Nitrate_df)

    # Print file names
    print(f"Processing {file} and {Nitrate_file}")

    # Merge the dfs
    merged_df = pd.merge(chlA_df, Nitrate_df['Nitrate Value'], how='inner', 
                         left_on=chlA_df['Collected Date'], right_on=Nitrate_df['Collected Date'])

    # fist pass will fail and create the df, subsequent passes will concat to existing
    try:
        All_sites = pd.concat([All_sites,merged_df], axis=0)
    except:
        All_sites = merged_df


All_sites.to_csv("All_sites_ChlA_Nitrate.csv")
All_sites.describe()


# %%


