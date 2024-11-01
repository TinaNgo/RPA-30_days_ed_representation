import pandas as pd

PATH = "Emergency_data.csv"

def generate_csv(dataframe, filepath):
    print("Generating csv file: " + filepath + "\n")
    dataframe.to_csv(filepath, index=False)

def extract_visits_within_30_days(group):
    count_within_30 = []
    repres30days = []
    
    for i in range(len(group)):
        current_visit_datetime = group['arrival_datetime'].iloc[i]
        # Count visits within 30 days from the current visit's arrival datetime
        count = ((group['arrival_datetime'] > current_visit_datetime) & 
                 (group['arrival_datetime'] <= current_visit_datetime + pd.Timedelta(days=30))).sum()
        count_within_30.append(count)
        repres30days.append(1 if count > 0 else 0)

    group['n_repres30days'] = count_within_30
    group['repres30days'] = repres30days

    return group


def main():
    print("Loading dataset.....")
    df = pd.read_csv(PATH)
    df = df.dropna(how='all')
    assert not df.isnull().values.all()

    # Combine arrival_date and arrival_time to create a datetime object
    df['arrival_date'] = pd.to_datetime(df['arrival_date'])
    df['arrival_time'] = pd.to_datetime(df['arrival_time']).dt.time
    df['arrival_datetime'] = pd.to_datetime(df['arrival_date'].astype(str) + ' ' + df['arrival_time'].astype(str))

    df = df.sort_values(by=['ppn', 'arrival_datetime'])

    print("Extracting.....")
    df = df.groupby('ppn').apply(extract_visits_within_30_days)

    # Drop the arrival_datetime column if not needed
    df = df.drop(columns=['arrival_datetime'])

    generate_csv(df, "Emergency_data_new.csv")


main()
