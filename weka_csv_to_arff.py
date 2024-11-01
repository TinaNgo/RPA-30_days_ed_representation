import weka.core.jvm as jvm
from weka.core.converters import Loader, Saver
# import os

# Full dataset
# PATH = 'clean_data/no_FS_full'

# Truncated set for faster testing
PATH = 'clean_data/no_FS_truncated'

def converter(filename):
	# Start the JVM (Java Virtual Machine)
	jvm.start()

	# filepath = 'TrainTestData' + filename
	filepath = filename

	# Load CSV file
	loader = Loader(classname="weka.core.converters.CSVLoader")
	data = loader.load_file(filepath+ '.csv')

	# Save the dataset as ARFF
	saver = Saver(classname="weka.core.converters.ArffSaver")
	saver.save_file(data, filepath + '.arff')

	# Stop the JVM
	jvm.stop()

	print(f"CSV file {filename}.csv has been converted to ARFF file: {filepath + '.arff'}")

def main():
	converter(PATH)

main()
