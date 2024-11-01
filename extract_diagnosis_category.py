import pandas as pd

# Path to the diagnosis dictionary
DICT_PATH = 'Diagnosis_coding/DIAGNOSIS_DICTIONARY.xlsx'
INT_DICT_PATH = 'Diagnosis_coding/INTEGER-  CODES DICTIONARY.xlsx'

# truncated data
# EMERGENCY_DATA_PATH = 'Emergency_truncated.csv'

# Full dataset
EMERGENCY_DATA_PATH = 'Emergency_data_new.csv'

OUT_PATH = 'Emergency_data_newer.csv'

def generate_csv(dataframe, filepath):
    print("Generating csv file: " + filepath + "\n")
    dataframe.to_csv(filepath, index=False)

def load_int_code_dict():
	int_dict = pd.read_excel(INT_DICT_PATH, sheet_name='DESTINY_CODE INTEGER')
	return {int(key): value for key, value in zip(int_dict['DESTINY_CODE INTEGER'], int_dict['CATEGORY'])}

def load_snomed_dict():
	print("Loading SNOMED diagnosis code dictionary.....\n")
	snomed = pd.read_excel(DICT_PATH, sheet_name='SNOMED TOTAL')
	# Drop rows where 'Snomed Code / ED Diagnosis Code' or 'dx_subcode_sct_integer' is missing
	snomed = snomed.dropna(subset=['Snomed Code / ED Diagnosis Code', 'dx_subcode_sct_integer'])
	snomed_dict = {str(int(key)): int(value) for key, value in zip(snomed['Snomed Code / ED Diagnosis Code'], snomed['dx_subcode_sct_integer'])}

	int_dict = load_int_code_dict()
	updated_snomed_dict =  {key: int_dict.get(value, 'NaN') for key, value in snomed_dict.items()}
	return updated_snomed_dict

def load_icd_dict():
	print("Loading ICD-9 diagnosis code dictionary.....\n")
	icd = pd.read_excel(DICT_PATH, sheet_name='ICD TOTAL')

	# Drop rows where 'ICD / ED Diagnosis Code' or 'dx_subcode_icd_integer' is missing
	icd = icd.dropna(subset=['ICD / ED Diagnosis Code', 'dx_subcode_icd_integer'])
	icd_dict = {str(key): int(value) for key, value in zip(icd['ICD / ED Diagnosis Code'], icd['dx_subcode_icd_integer'])}
	# print(icd_dict)
	int_dict = load_int_code_dict()
	updated_icd_dict =  {key: int_dict.get(value, 'NaN') for key, value in icd_dict.items()}

	return updated_icd_dict

def add_diagnosis_category(emergency, snomed_dict, icd_dict):
    # Function to add the 'diagnosis_category' column to the emergency DataFrame
    def get_diagnosis_category(row):
        if pd.notna(row['ED_DIAGNOSIS_CODE_SCT']):  # If SNOMED code exists
            
            return snomed_dict.get(str(int(row['ED_DIAGNOSIS_CODE_SCT'])), 'NaN')
        elif pd.notna(row['ED_DIAGNOSIS_CODE']):  # If ICD code exists
            return icd_dict.get(str(row['ED_DIAGNOSIS_CODE']), 'NaN')
        return 'NaN'  # Default if neither exists
    
    # Apply the function to each row
    emergency['diagnosis_category'] = emergency.apply(get_diagnosis_category, axis=1)
    
    return emergency


def main():
	snomed_dict = load_snomed_dict()
	icd_dict = load_icd_dict()
	print(snomed_dict)

	emergency = pd.read_csv(EMERGENCY_DATA_PATH)

    # Add the diagnosis_category column
	emergency = add_diagnosis_category(emergency, snomed_dict, icd_dict)
    
	# make repres30days the last column
	cols = [col for col in emergency.columns if col != 'repres30days'] + ['repres30days']
	emergency = emergency[cols]
    
    # Save the updated DataFrame to a new CSV
	generate_csv(emergency, OUT_PATH)
          
      
      
main()
      