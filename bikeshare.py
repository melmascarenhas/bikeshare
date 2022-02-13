import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # creating cities list to search for during input
    cities = ['chicago','new york city','washington']
    # will return a city's data and an acceptance command if the input is equal to one of the items in cities
    while True:
        city = input("Which data set would you like to explore? Please select from chicago, new york city, or washington.\n").lower()
        if city in cities:
            print("Great! Let's continue.")
            break
        else:
            print("Sorry, try again. Please input one from the following: chicago, new york city, washington.\n")

    # TO DO: get user input for month (all, january, february, ... , june)
    # creating month list to search for during input
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    # will return a month's data and an acceptance command if the input is equal to one of the items in months
    while True:
        month = input("What month would you like to look at? Please select a month from january through june. If you want to look at all months, please input 'all'.\n").lower()
        if month in months:
            print("Great! Let's continue.")
            break
        else:
            print("Sorry, try again. Please input a month from january through june or all.\n")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    # creating days list to search for during input
    days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']
    # will return a day of week's data and an acceptance command if the input is equal to one of the items in days
    while True:
        day = input("What month would you like to look at? Please select a day of the week from monday through sunday. If you want to look at all days of the week, please input 'all'\n").lower()
        if day in days:
            print("Great! Let's continue.")
            break
        else:
            print("Sorry, try again. Please input a day from monday through sunday or all.\n")
    
    
    print('-'*40)
    return city, month, day
    
    
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
# load file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # seperate month and day of week from Start Time to create new columns

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
   	 	# use the index of the months list to get the corresponding integer
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

    	# filter by month to create the new dataframe
        df = df[df['month'] == month]

        # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # mode method finds most common month
    
    popular_month = df['month'].mode()[0]
    print('Most Common Month:', popular_month)

    # mode method finds most common day of week
    
    popular_day = df['day_of_week'].mode()[0]
    print('Most Common day:', popular_day)

    # mode method finds most hour of start travel time
    
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Common Hour:', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # mode method finds most common start travel station
    start_station = df['Start Station'].mode()[0]
    print('Most Common Start Station:', start_station)

    # mode method finds most common start travel station
    end_station = df['End Station'].mode()[0]
    print('Most Common End Station:', end_station)

    # create combination travel column by concatenating start and end stations with +
    df['combo station'] = df['Start Station'] +  " TO " + df['End Station']
    
    # mode method finds most common combination of travel stations from start to end
    
    combo_station = df['combo station'].mode()[0]
    print('Most Common Combination Station Trip:', combo_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # sum trip duration in seconds and divide by 3,600 to convert to hours
    Total_Travel_Time = sum(df['Trip Duration'])
    print('Total travel time:', Total_Travel_Time, "Seconds", "or", Total_Travel_Time/3600, "Hours")

    # use mean method to receive the average and convert seconds into minutes
    Mean_Travel_Time = df['Trip Duration'].mean()
    print('Mean travel time:', Mean_Travel_Time, "Seconds", "or", Mean_Travel_Time/60, "Minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # count different values within User Type
    user_types = df['User Type'].value_counts()
    print('User Types:\n',user_types)

    # trying for gender when available and counting values per gender
    try:
        gender = df['Gender'].value_counts()
        print("\nThe types of users by gender are given below:\n", gender)
    except:
        print("\nThere is no 'gender' column in this file.")

    # trying for birth year when available and returning earlier with minimum method, latest with maximum method, and common birth year with     # mode method
    try:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print(f"\nThe earliest year of birth: {earliest}\n\nThe most recent year of birth: {recent}\n\nThe most common year of birth: {common_year}")
    except:
        print("There are no birth year details in this file.")

    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*80)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
    #starting position of rows
    start_loc = 0
    #display raw data based on select city, month, and day above
    view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no?/n")
    #while loop to reiterate through 5 rows of data until user says no
    while True:
        if view_data in ('yes'):
            print(df.iloc[start_loc:start_loc+5])
            start_loc += 5
            more_data = input("Would you like to see the next 5 lines? Yes or No: ").lower()
            #ask user if they want additional data with opportunity to break out of loop
            if more_data not in ('yes'):
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
