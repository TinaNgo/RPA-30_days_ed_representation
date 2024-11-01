from imblearn.under_sampling import RandomUnderSampler
import pandas as pd

def generate_csv(dataframe, filepath):
	print("Generating csv file: " + filepath + "\n")
	dataframe.to_csv(filepath, index=False)

def perform_random_under_sampling(df, out_path, sampling_strategy='auto'):
	"""
	Perform random under-sampling on the given dataset.

	Parameters:
	- df: pd.DataFrame - The entire dataset including features and target.
	- target_column: str - The name of the target column.
	- sampling_strategy: str or dict (default='auto') - The sampling strategy to use for under-sampling.
	- random_state: int or None (default=None) - Random state for reproducibility.

	Returns:
	- df_resampled: pd.DataFrame - The resampled DataFrame including both features and the target column.
	"""
	target_column = 'repres30days'

	# Separate features (X) and target (y)
	X = df.drop(columns=[target_column])
	y = df[target_column]
	print(f"[{out_path}]")
	print(f"Training set size before applying random under-sampling: {X.shape}\n")

	print("Class distribution in training set before random under-sampling:")
	print(y.value_counts())

	# Initialize the RandomUnderSampler
	rus = RandomUnderSampler(sampling_strategy=sampling_strategy, random_state=42)

	# Perform the random under-sampling
	X_resampled, y_resampled = rus.fit_resample(X, y)

	# Convert the resampled data back to pandas DataFrame and Series
	X_resampled = pd.DataFrame(X_resampled, columns=X.columns)
	y_resampled = pd.Series(y_resampled, name=target_column)

	print("\nClass distribution in trainning set after random under-sampling:")
	print(y_resampled.value_counts())

	# Combine the resampled features and target into one DataFrame
	df_resampled = pd.concat([X_resampled, y_resampled], axis=1)
    
	generate_csv(df_resampled, out_path + 'train_resampled.csv')
    
	return df_resampled

def main():
	path = 'TrainTestData/NO_FS/'
	df = pd.read_csv(path + "train.csv")
	perform_random_under_sampling(df, path)

	path = 'TrainTestData/CFS/'
	df = pd.read_csv(path + "train.csv")
	perform_random_under_sampling(df, path)

	path = 'TrainTestData/InfoGain/'
	df = pd.read_csv(path + "train.csv")
	perform_random_under_sampling(df, path)

	path = 'TrainTestData/Manual_FS/'
	df = pd.read_csv(path + "train.csv")
	perform_random_under_sampling(df, path)

main()
