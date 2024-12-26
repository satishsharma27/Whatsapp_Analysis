import re
import pandas as pd

def preprocess(data):
    pattern = r"\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[AP]M\s-\s(.*)"

    messages = re.split(pattern, data)[1:]
    # Regular expression pattern to match only the date and time
    pattern = r"^\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[AP]M"

    dates = []

    # Split the data into lines
    lines = data.split('\n')

    # Loop through each line, find matches, and print them
    for line in lines:
        matches = re.findall(pattern, line)
        if matches:
            for match in matches:
                dates.append(match)

    min_length = min(len(messages), len(dates))
    messages = messages[:min_length]
    dates = dates[:min_length]

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M %p')

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df.rename(columns={"message_date": 'date'}, inplace=True)
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute


    return df
