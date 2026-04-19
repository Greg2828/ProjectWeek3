import pandas as pd
import numpy as np

##################################################
def info_df(df):                   ## General Information about the DataFrame

    ### title
    print("*"*100,"\n"+"*"*43+"DATAFRAME INFO"+"*"*43,"\n"+"*"*100)

    ## datainfo
    data_info = df.info()
    print(f"\nINFO OF THE DATAFRAME: {data_info}")
    print("*"*100,"\n"+"*"*100)

    # Shape of the DataFrame (rows, columns)
    data_shape = df.shape
    print(f"\nSHAPE OF THE DATAFRAME: {data_shape}")
    print("*"*100,"\n"+"*"*100)

    # Column names
    column_names = df.columns
    print(f"\nCOLUMN NAMES: {column_names}")
    print("*"*100,"\n"+"*"*100)

    # Data types of each column
    data_types = df.dtypes
    print(f"\nDATA TYPES:\n{data_types}")
    print("*"*100,"\n"+"*"*100)

    ################### Statistical Summary
    data_summary = df.describe(include='all')
    print("\nSTATISTICAL SUMMARY:")
    print(data_summary)
    print("*"*100,"\n"+"*"*100)
    ###################  sample records from the data frame
    print("\nFIRST 5 ROWS:")
    data_head = display(df.head())
    print(data_head)
    print("*"*100,"\n"+"*"*100)

    ###################  sample records from the data frame
    data_unique = df.nunique()
    print("\nUNIQUE VALUES PER COLUMN:")
    print(data_unique)
    print("*"*100,"\n"+"*"*100)
########

def normalize_column_names(df):             ### convert to lower snake_case names
    df.columns = [col.lower().replace(" ", "_") for col in df.columns]
    print("\n********** NEW COLUMN NAMES NORMALIZED **********\n",df.columns)
    return df

#########

def cutting_df(columns,df):   
    ### Receive a list of columns and create an return the new dataframe 
    # accepts a single column as a string
    
    # column list is empty
    if not columns:
        print("\n*** ATTENTION! The column list is empty ***")
        return None
    else:
        if isinstance(columns, str):
            columns = [columns]
        else:
            # PARAMETER 2 , is a pandas DataFrame??
            if not isinstance(df, pd.DataFrame):
                print("\n************** PARAMETER 2 , must be a pandas DataFrame **************")
            else:
                # Check if all columns are in the DataFrame
                if all(col in df.columns for col in columns):
                    cut_df = df[columns].copy()
                    print("\n************** CUT FROM DATASET PERFORMED OK **************")
                    print("\n*************** NEW DATA FRAME COLUMN NAMES ***************\n",df.columns)
                    return cut_df
                else:
                    # Missing columns  
                    missing = [col for col in columns if col not in df.columns]
                    print("\n*** ATTENTION! DATASET PERFORMED KO , Missing columns:", missing," ***")
                    return None              
#########

def check_nulls_empty(df):

    print("\n*************** CLEANING EMPY & NULLS ***************\n")

    if not isinstance(df, pd.DataFrame):
        print("\n********ERROR: IT'S NOT A DATAFRAME********")
        return None

    # Copia del DataFrame original
    df_clean = df.copy()

    # Guardar número de filas iniciales
    filas_iniciales = len(df_clean)

    filas_validas = []

    # Recorrer filas
    for idx, fila in df_clean.iterrows():

        fila_valida = True

        # Recorrer valores de la fila
        for valor in fila:

            # Si es NaN → eliminar fila
            if pd.isna(valor):
                fila_valida = False
                break

            # Si es vacío o solo espacios → eliminar fila
            if str(valor).strip() == '':
                fila_valida = False
                break

        # Si la fila es válida, se guarda
        if fila_valida:
            filas_validas.append(idx)

    # Mantener solo filas válidas
    df_clean = df_clean.loc[filas_validas]

    # Calcular filas eliminadas
    filas_finales = len(df_clean)
    filas_eliminadas = filas_iniciales - filas_finales

    print("\n********ROWS ELIMINATED: ",filas_eliminadas," ********")
    print("******ROWS & COLUMNS IN DATAFRAME CLEANED : ",df_clean.shape)

    return df_clean
#########

def remove_non_positive(df, column):

    print("\n*************** REMOVE VALUES <= 0 ***************")
    print("\n************ COLUMN ",column," ***************\n")

    # Check if input is a DataFrame
    if not isinstance(df, pd.DataFrame):
        print("\n*****ERROR: INPUT IS NOT A DATAFRAME*****")
        return None

    # Check if column exists
    if column not in df.columns:
        print("*****ERROR: COLUMN DOES NOT EXIST*****")
        return None

    # Create a copy of the DataFrame
    df_clean = df.copy()

    # Convert column to numeric (invalid values become NaN)
    df_clean[column] = pd.to_numeric(df_clean[column], errors='coerce')

    # Store initial number of rows
    initial_rows = len(df_clean)

    # Remove rows where value in the column is <= 0
    df_clean = df_clean[df_clean[column] > 0]

    # Calculate removed rows
    removed_rows = initial_rows - len(df_clean)

    print(f"\n*****ROWS REMOVED: ", removed_rows," *****")

    return df_clean

#########

import pandas as pd

def keep_between_0_1(df, column):

    print("\n*************** KEEP VALUES BETWEEN 0 AND 1 ***************\n")
    print("\n************ COLUMN ",column," ***************\n")

    # Check if input is a DataFrame
    if not isinstance(df, pd.DataFrame):
        print("\n*****ERROR: INPUT IS NOT A DATAFRAME*****")
        return None

    # Check if column exists
    if column not in df.columns:
        print("*****ERROR: COLUMN DOES NOT EXIST*****")
        return None

    df_clean = df.copy()

    initial_rows = len(df_clean)

    # Clean and convert column for problems with spaces and , - . 
    df_clean[column] = (
        df_clean[column]
        .astype(str)
        .str.strip()
        .str.replace(',', '.')
    )
    
    # Convert column to numeric (invalid values become NaN)
    df_clean[column] = pd.to_numeric(df_clean[column], errors='coerce')

    # Keep only values between 0 and 1
    df_clean[column] = df_clean[column].astype(float)
    df_clean = df_clean[(df_clean[column] >= 0) & (df_clean[column] <= 1.0)]

    removed_rows = initial_rows - len(df_clean)

    print(f"\n*****ROWS REMOVED: ", removed_rows," *****")

    return df_clean

#############

def keep_valid_dates(df, column):

    print("\n*************** KEEP VALID DATE FORMAT (M/D/YYYY or MM/DD/YYYY) ***************\n")
    print("\n************ COLUMN ", column, " ***************\n")

    # Check if input is a DataFrame
    if not isinstance(df, pd.DataFrame):
        print("\n*****ERROR: INPUT IS NOT A DATAFRAME*****")
        return None

    # Check if column exists
    if column not in df.columns:
        print("*****ERROR: COLUMN DOES NOT EXIST*****")
        return None

    df_clean = df.copy()
    initial_rows = len(df_clean)

    # Clean column (remove spaces and ensure string type)
    df_clean[column] = (
        df_clean[column]
        .astype(str)
        .str.strip()
    )

    def validate_date(value):
        try:
            # Split by '/'
            parts = value.split('/')

            # Must have exactly 3 parts
            if len(parts) != 3:
                return False

            m_month, d_day, y_year = parts

            # Length checks
            if not (1 <= len(m_month) <= 2 and 1 <= len(d_day) <= 2 and len(y_year) == 4):
                return False

            # Numeric check
            if not (m_month.isdigit() and d_day.isdigit() and y_year.isdigit()):
                return False

            # Convert to integers
            m_month = int(m_month)
            d_day = int(d_day)
            y_year = int(y_year)

            # Range validation
            if not (1 <= m_month <= 12):
                return False
            if not (1 <= d_day <= 31):
                return False
            if not (1 <= y_year <= 9999):
                return False

            return True

        except:
            return False

    # Apply validation
    valid_mask = df_clean[column].apply(validate_date)

    # Keep only valid rows
    df_clean = df_clean[valid_mask]

    removed_rows = initial_rows - len(df_clean)

    print(f"\n*****ROWS REMOVED: ", removed_rows, " *****")

    return df_clean


def convert_to_datetime(df, column):

    print("\n*************** CONVERT COLUMN TO DATETIME ***************\n")
    print("\n************ COLUMN ", column, " ***************\n")

    # Check if input is a DataFrame
    if not isinstance(df, pd.DataFrame):
        print("\n*****ERROR: INPUT IS NOT A DATAFRAME*****")
        return None

    # Check if column exists
    if column not in df.columns:
        print("*****ERROR: COLUMN DOES NOT EXIST*****")
        return None

    df_clean = df.copy()

    initial_rows = len(df_clean)

    # Clean column (ensure string and strip spaces)
    df_clean[column] = (
        df_clean[column]
        .astype(str)
        .str.strip()
    )

    # Convert to datetime (invalid values become NaT)
    df_clean[column] = pd.to_datetime(
        df_clean[column],
        errors='coerce',
        infer_datetime_format=True
    )

    # Remove rows where conversion failed
    df_clean = df_clean[df_clean[column].notna()]

    removed_rows = initial_rows - len(df_clean)

    print(f"\n*****ROWS REMOVED: ", removed_rows, " *****")

    return df_clean