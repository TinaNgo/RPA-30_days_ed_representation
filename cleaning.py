# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from contextlib import redirect_stdout


# For ARTEMIS big one
# SPECIFIC_OUTPUT_DIR = "clean_data/"
# DATA_SOURCE = "Emergency_data_newer.csv"
# SUFFIX = "_full"

# For truncated data
SPECIFIC_OUTPUT_DIR = "clean_data/"
DATA_SOURCE = "truncated.csv"
SUFFIX = "_truncated"

TARGET_VAR = 'repres30days'
SELECTED_COLUMNS = ['age_recode',
                    'arrival_time',
                    'SEX', 
                    'ED_SOURCE_OF_REFERRAL', # where to put in employer?
                    'referred_to_on_departure_recode',
                    'PREFERRED_LANGUAGE_ASCL', 
                    'MODE_OF_ARRIVAL',
                    'MODE_OF_SEPARATION', 
                    # 'ED_LOS', # not in dataset
                    'TRIAGE_CATEGORY',
                    # 'HOURS_IN_ICU', # not in dataset
                    'diagnosis_category',
                    # 'level', # hospital type
                    # 'remoteness', # not in dataset
                    # 'DEATH_DATE',  # not in dataset
                    # 'PRESENTING_PROBLEM', # not in dataset
                    TARGET_VAR,
]

NEW_COLUMNS = ['age',
               'presentation_time',
                'sex',
                'source_referral',
                'departure_referral',
                'preferred_language',
                'arrival_mode',
                'separation_mode',
                'triage_category',
                # 'icu_status', # not in dataset
               	'diagnosis_category',
                # 'level', # not in dataset
                # 'EDLOS', # not in dataset
                # 'remoteness', # not in dataset
                # 'death_status', # not in dataset
                # 'presenting_problem', # not in dataset
                TARGET_VAR
]

# ALL_COLUMNS = [
#     "project_recnum",
#     "ppn",
#     "facility_identifier",
#     "referred_to_on_departure_recode",
#     "age_recode",
#     "arrival_date",
#     "arrival_time",
#     "actual_departure_date",
#     "actual_departure_time",
#     "departure_ready_time",
#     "triage_time",
#     "PREFERRED_LANGUAGE_ASCL",
#     "ED_DIAGNOSIS_CODE",
#     "SEX",
#     "ED_DIAGNOSIS_CODE_SCT",
#     "ED_SOURCE_OF_REFERRAL",
#     "MODE_OF_ARRIVAL",
#     "MODE_OF_SEPARATION",
#     "NEED_INTERPRETER_SERVICE",
#     "TRIAGE_CATEGORY",
#     "SLA_2011_CODE",
#     "MTHYR_TRIAGE_DATE",
#     "MTHYR_WEEKDAY_DEPARTURE_READY",
#     "n_repres30days",
#     "diagnosis_category",
#     TARGET_VAR
# ]


def count_rows_containing_nan(df):
    return df.isnull().any(axis=1).sum()

def age_to_nominal(age: float) -> int:
    if age < 6:
        return "0-5"
    elif age < 16:
        return "6-15"
    elif age < 26:
        return "16-25"
    elif age < 46:
        return "26-45"
    elif age < 66:
        return "46-65"
    elif age < 86:
        return "66-85"
    return "86+"

def sex_to_nominal(sex: int) -> str:
    if sex == 1:
        return "M"
    elif sex == 2:
        return "F"
    return "other"

# To make sure the triage is interpret as a nominal value
def triage_to_nominal(triage: int) -> str:
	if triage == 1:
		return "one"
	elif triage == 2:
		return "two"
	elif triage == 3:
		return "three"
	elif triage == 4:
		return "four"
	elif triage == 5:
		return "five"
	return "NaN"


def source_of_referral_to_nominal(source: int) -> str:
    if isinstance(source, float) == False:
        return "other"
    elif source == 1: # self, family, friends
        return "self/family/friends"
    elif source <= 4: # clinic
        return "clinic"
    elif source <= 9: # hospital
        return "hospital"
    elif source <= 16: # community org
        return "community_org"
    return "other"

def referred_to_on_departure_to_nominal(source: int) -> str:
    if source < 3: # review in ED
        return "ED_review"
    elif source == 8: # not referred
        return "no_referral"
    elif source == 9: # unknown
        return "unknown"
    return "specialist" # referred to specialist or social work

def preferred_language_ascl_to_nominal(language: int) -> str:
    if isinstance(language, float) == False:
        return "other"
    elif language < 1000: # unknown or nonverbal
        return "none"
    elif language == 1201: # english
        return "english"
    elif language < 4000: # european
        return "european"
    elif language < 5000: # middle eastern
        return "middle eastern"
    elif language < 8000: # asian
        return "asian"
    return "other" # catchall other

def mode_of_arrival_to_nominal(mode: int) -> str:
    if mode in [1, 4, 5, 6]: # ambulance of some sort
        return "ambulance"
    elif mode == 3: # private vehicle
        return "private_vehicle"
    return "other"

def mode_of_separation_to_nominal(mode) -> str:
    if isinstance(mode, float) == False:
        return "died/other"
    elif mode in [1, 2, 5, 9, 10, 11, 12]: # admitted
        return "admitted"
    elif mode in [3, 8, 99]: # died or error
        return "died/other"
    elif mode in [6, 7, 13]: # left against advice
        return "left_against_advice"
    return "released" # released from ED

# def hours_in_icu_to_nominal(hours: int) -> str:
#     if hours > 0: # attended ICU
#         return "True"
#     return "False"


# def ed_los_to_nominal(hours: int) -> str:
#     if hours <= 4:
#         return "0-4"
#     elif hours <= 12:
#         return "5-12"
#     elif hours <= 24:
#         return "13-24"
#     return "25+"

# def death_to_nominal(date: str) -> str:
#     if date != 0:
#         return "True"
#     return "False"

def arrival_time_to_nominal(arrival_time: str) -> str:
    arrival_hour = pd.to_datetime(arrival_time, format='%H:%M:%S').hour

    # Discretize based on the hour
    if 8 <= arrival_hour < 17:   # 8am-5pm
        return 'business hours'
    elif 17 <= arrival_hour < 23:  # 5pm-11pm
        return 'evening'
    elif arrival_hour >= 23 or arrival_hour < 8:  # 11pm-8am
        return 'night'
    return 'NaN'

def repres30days_to_norminal(repres: int) -> str:
	if repres == 0:
		return 'false'
	else:
		return 'true'


# Something is wrong with this function so I commented it out!!!
# calculate and add the ED_LOS column
# def calculate_ed_los(df: pd.DataFrame) -> pd.DataFrame:
#     # Convert date columns to datetime objects
#     df['arrival_date'] = pd.to_datetime(df['arrival_date'], format='%d/%m/%Y', errors='coerce')
#     df['actual_departure_date'] = pd.to_datetime(df['actual_departure_date'], format='%d-%b-%y', errors='coerce', dayfirst=True)
    
#     # Convert time columns to time only
#     df['arrival_time'] = pd.to_datetime(df['arrival_time'], format='%H:%M:%S', errors='coerce').dt.time
#     df['actual_departure_time'] = pd.to_datetime(df['actual_departure_time'], format='%H:%M:%S', errors='coerce').dt.time

#     # Combine arrival_date and arrival_time into a single datetime column
#     df['arrival_datetime'] = df.apply(
#         lambda row: pd.Timestamp.combine(row['arrival_date'], row['arrival_time']) 
#         if pd.notnull(row['arrival_date']) and pd.notnull(row['arrival_time']) else pd.NaT, axis=1
#     )

#     # Combine actual_departure_date and actual_departure_time into a single datetime column
#     df['departure_datetime'] = df.apply(
#         lambda row: pd.Timestamp.combine(row['actual_departure_date'], row['actual_departure_time']) 
#         if pd.notnull(row['actual_departure_date']) and pd.notnull(row['actual_departure_time']) else pd.NaT, axis=1
#     )

#     # Calculate the difference in hours between arrival and departure
#     df['ED_LOS'] = (df['departure_datetime'] - df['arrival_datetime']).dt.total_seconds() / 3600

#     # If any datetime fields are NaT, set ED_LOS to NaN
#     df.loc[df['arrival_datetime'].isna() | df['departure_datetime'].isna(), 'ED_LOS'] = np.nan

#     # Optionally, remove the intermediate datetime columns if not needed
#     df = df.drop(columns=['arrival_datetime', 'departure_datetime'])

#     return df


def output_analytics(df):
    # Count number of instances containing missing values
    if df.isnull().values.any():
        n_missing = count_rows_containing_nan(df)
        n_rows = len(df)
        print(f'{n_missing} rows out of {n_rows} rows '
              f'({n_missing / n_rows * 100:.2f}%) contain missing values.\n')
        df = df.fillna('missing')
    # Cross-tabulate each attribute against class attribute
    for col in df.columns:
        if col == TARGET_VAR:
            continue
        tab = pd.crosstab(
            df[col], df[TARGET_VAR], dropna=False, margins=True)
        print(tab, '\n')
        
def main():
	pd.set_option('display.max_rows', 30)
	df = pd.read_csv(DATA_SOURCE)
     	
	print('Original Dataset:')
	print(df.columns)
    
	df = df[SELECTED_COLUMNS]

	# print('Selected Columns:')
	# print(df.head())
	# print(df.dtypes)

	# Ensure there are no NULL rows in the data
	df = df.dropna(how = 'all')
	assert not df.isnull().values.all()
     
	# Remove all rows where diagnosis_category is 'DEAD'
	df = df[df['diagnosis_category'] != 'DEAD']

	# Coerce most columns to numeric
	numeric_cols = df.columns[df.dtypes.ne('object')]
	df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric)

	# rename columns
	df.columns = NEW_COLUMNS

	print("Renamed Columns:")
	# print(df.head())
	print(df.dtypes)

	df = df.dropna(how = 'any')
	# # Transform variables into buckets
	df['age'] = df['age'].apply(age_to_nominal)
	df['sex'] = df['sex'].apply(sex_to_nominal)
	df['source_referral'] = df['source_referral'].apply(source_of_referral_to_nominal)
	df['departure_referral'] = df['departure_referral'].apply(referred_to_on_departure_to_nominal)
	df['preferred_language'] = df['preferred_language'].apply(preferred_language_ascl_to_nominal)
	df['arrival_mode'] = df['arrival_mode'].apply(mode_of_arrival_to_nominal)
	df['separation_mode'] = df['separation_mode'].apply(mode_of_separation_to_nominal)
	df['presentation_time'] = df['presentation_time'].apply(arrival_time_to_nominal)
	df['triage_category'] = df['triage_category'].apply(triage_to_nominal)
	df['repres30days'] = df['repres30days'].apply(repres30days_to_norminal)
     
     
    
	# print("Fully Cleaned Dataset:")
	print(df.dtypes)

	# export new clean data to csv
	df.to_csv(SPECIFIC_OUTPUT_DIR + 'no_FS' + SUFFIX + '.csv', index=False)

	# cross tabulate all new variables
	with open(SPECIFIC_OUTPUT_DIR + 'summary' + SUFFIX + '.txt', 'w') as f:
		with redirect_stdout(f):
			output_analytics(df)
    
main()
