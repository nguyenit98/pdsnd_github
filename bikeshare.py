import time
import pandas as pd
import numpy as np

# Create CITY_DATA to store 3 datasets
CITY_DATA = { 'chicago': 'chicago.csv', 
             'new york': 'new_york_city.csv', 
             'washington': 'washington.csv' 
            }

def get_filters():
    '''
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or 'all' to apply no month filter
        (str) day - name of the day of week to filter by, or 'all' to apply no day filter
    '''
    print('Hello! Let\'s explore some US bikeshare data!')
    
    #Init city variable
    city = ''
    
    #Define WHILE loop to get the valid user's output
    while city not in CITY_DATA.keys():
        print('\nWould you like to see data for Chicago, New York, or Washington?')
        
        #Standardize the input
        city = input().lower()

        if city not in CITY_DATA.keys():
            print('\nPlease check your input and try again!')
            print('\nRestarting...')

    #Create MONTH_DATA to mapping month to index
    MONTH_DATA = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12, 'all': 7}
    
    #Init month variable
    month = ''
    while month not in MONTH_DATA.keys():
        print('\nWhich month would you like to filter? Please type name of month or type "all" if no filter.')
        
        #Standardize the input
        month = input().lower()

        if month not in MONTH_DATA.keys():
            print('\nPlease check your input and try again!')
            print('\nRestarting...')

    #Create DAY_LIST to store valid day value and 'all' option
    DAY_LIST = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    
    #Init day variable
    day = ''
    while day not in DAY_LIST:
        print('\nWhich day would you like to filter? Please type the fullname of weekday or "all" if no filter!')
        
        #Standardize the input
        day = input().lower()

        if day not in DAY_LIST:
            print('\nPlease check your input and try again!')
            print('\nRestarting...')

    print('-'*40)
    #Return values
    return city, month, day

#Function to load data from .csv files
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
    #Load data file into a dataframe
    print('\nLoading data...')
    df = pd.read_csv(CITY_DATA[city])

    #Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    #Filter by month if applicable
    if month != 'all':
        #Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
        month = months.index(month) + 1

        #Filter by month to create the new dataframe
        df = df[df['month'] == month]

    #Filter by day of week if applicable
    if day != 'all':
        #Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    #Returns the dataframe
    return df

#Function to calculate all the time-related statistics for the chosen data
def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.

    Args: a dataframe

    Returns: time taken to perform a calculation (in seconds)
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #Uses mode method to find the most popular month
    popular_month = df['month'].mode()[0]

    print(f'Most Popular Month: {popular_month}')

    #Uses mode method to find the most popular day
    popular_day = df['day_of_week'].mode()[0]

    print(f'\nMost Popular Day: {popular_day}')

    #Extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    #Uses mode method to find the most popular hour
    popular_hour = df['hour'].mode()[0]

    print(f'\nMost Popular Hour: {popular_hour}')

    #Prints the time taken to perform the calculation
    print(f'\nThat took {(time.time() - start_time)} seconds.')
    print('-'*40)


def station_stats(df):
    """
        Displays statistics on the most popular stations and trip.

        Args: a dataframe

        Returns: Return the station statics
    
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #Uses mode method to find the most common start station
    common_start_station = df['Start Station'].mode()[0]

    print(f'The most common start station: {common_start_station}')

    #Uses mode method to find the most common end station
    common_end_station = df['End Station'].mode()[0]

    print(f'\nThe most common end station: {common_end_station}')

    #Uses str.cat to combine two columsn in the df
    #Assigns the result to a new column 'Start To End'
    #Uses mode on this new column to find out the most common combination
    #of start and end stations
    df['Start To End'] = df['Start Station'].str.cat(df['End Station'], sep=' - ')
    combination_station = df['Start To End'].mode()[0]

    print(f'\nThe most frequent combination of trips are {combination_station}.')

    print(f'\nThat took {(time.time() - start_time)} seconds.')
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #Calculate the total duration
    total_duration = df['Trip Duration'].sum()
    print(f'The total trip duration: {total_duration}')

    #Calculating the average duration
    avg_duration = round(df['Trip Duration'].mean())
    print(f'The average trip duration: {avg_duration}')
    
    print(f'\nThat took {(time.time() - start_time)} seconds.')
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Count values group by User Type
    user_type = df['User Type'].value_counts()

    print(f'What is the breakdown of users?\n{user_type}')

    #Use try..except to handle if no gender column
    try:
        gender = df['Gender'].value_counts()
        print(f'\nWhat is the breakdown of gender?\n{gender}')
    except:
        print('\nThere is no gender.')

    #Use try..except to handle if no birth year column
    try:
        youngest = int(df['Birth Year'].min())
        oldest = int(df['Birth Year'].max())
        most_popular_year = int(df['Birth Year'].mode()[0])
        print(f'\nWhat is the oldest, youngest, and most popular year of birth?\n({oldest},{youngest},{most_popular_year})')
    except:
        print('There are no birth year details in this file.')

    print(f'\nThat took {(time.time() - start_time)} seconds.')
    print('-'*40)


def show_data(df):
    '''
    Show 5 rows of given city dataset.
    '''
    RESPONSE_LIST = ['yes', 'no']
    respond = ''
    #Init cnt variable
    cnt = 0
    while respond not in RESPONSE_LIST:
        print('\nWould you like to preview dataset?')
        respond = input().lower()
        #the raw data from the df is displayed if user opts for it
        if respond == 'yes':
            print(df.head())
        elif respond not in RESPONSE_LIST:
            print('\nPlease check your input and try again!')
            print('\nRestarting...')

    #Continue with a WHILE loop if user want to see next 5 rows data
    while respond == 'yes':
        print('\nWould you like to see more?')
        cnt += 5
        respond = input().lower()
        #If user opts for it, this displays next 5 rows of data
        if respond == 'yes':
             print(df[cnt:cnt+5])
        elif respond != 'yes':
             break

    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        show_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df) 

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == '__main__':
	main()