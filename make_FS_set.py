import pandas as pd

def generate_csv(dataframe, filepath):
	print("Generating csv file: " + filepath + "\n")
	dataframe.to_csv(filepath, index=False)

def load_and_filter_dataframe(directory_in, directory_out, col_list):
    """
    Loads a DataFrame from a CSV file and keeps only the specified columns.
    
    :param csv_filepath: Path to the CSV file.
    :param col_list: List of columns to keep.
    :return: Filtered DataFrame containing only the specified columns.
    """
    # Load the CSV into a DataFrame
    test_df = pd.read_csv(directory_in + 'test.csv')
    # train_df = pd.read_csv(directory_in + 'train.csv')
    
    # Keep only the specified columns
    filtered_test_df = test_df[col_list]
    # filtered_train_df = train_df[col_list]
    
    generate_csv(filtered_test_df, directory_out + 'test.csv')
    # generate_csv(filtered_train_df, directory_out + 'train.csv')

def main():
    # Define the file path and the columns to keep
    directory_in = "TrainTestData/NO_FS/"
    TARGET = 'repres30days'
    
	# Manual Feature Selection by Michael
    # manual_directory_out = "TrainTestData/Manual_FS/"
    # manual_col_list = ["sex", "separation_mode", "diagnosis_category", "age", "triage_category", TARGET]
    # load_and_filter_dataframe(directory_in, manual_directory_out, manual_col_list)

    cfs_directory_out = "TrainTestData/CFS/"
    cfs_col_list = ["departure_referral", "diagnosis_category", TARGET]
    load_and_filter_dataframe(directory_in, cfs_directory_out, cfs_col_list)

    info_gain_directory_out = "TrainTestData/InfoGain/"
    info_gain_col_list = ["diagnosis_category", "departure_referral", "age", "triage_category", "separation_mode", TARGET]
    load_and_filter_dataframe(directory_in, info_gain_directory_out, info_gain_col_list)
    

if __name__ == "__main__":
    main()
