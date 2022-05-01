import time
import pandas as pd


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

week_data = {'mon':0, 'tue':1, 'wed':2, 'thu':3, 'fri':4, 'sat':5, 'sun':6}

week_data_int = {0:'monday', 1:'tuesday', 2:'wednesday', 3:'thursday', 4:'friday', 5:'saturday', 6:'sunday'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    month_input = False
    day_input = False
    city_input = False
    while(city_input == False):
        city = input ("Which city would you like to analyze? (chicago, new york city or washington) :")
        if(city.lower() =='chicago' or city.lower() =='new york city' or city.lower() =='washington'):  
            city_input = True
    ## get user input for month (all, january, february, ... , june)
    while(month_input == False):
        month = input ("Which month would you like to analyze? (jan, feb, mar, apr, may, jun or all for no month filter) : ")
        if(month.lower() == 'jan' or month.lower() == 'feb' or month.lower() == 'mar' or month.lower() == 'apr' or month.lower() == 'may' or month.lower() == 'jun' or month.lower()  == 'all')  :  
            month_input = True
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while(day_input == False):
        day = input ("Which day would you like to analyze? (mon, tue, wed, thu, fri, sat, sun or all for no day filter) : ")
        if(day.lower() == 'mon' or day.lower() == 'tue' or day.lower() == 'wed' or day.lower() == 'thu' or day.lower() == 'fri' or day.lower() == 'sat' or day.lower() == 'sun' or day.lower() == 'all')  :  
            day_input = True

    print('-'*40)
    return city.lower(), month.lower(), day.lower()


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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    #df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    if day !='all':
        day_filter = df['Start Time'].dt.dayofweek == week_data[day]
        df = df.loc[day_filter]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print('Most Popular Month:', popular_month)


    # display the most common day of week
    df['week'] = df['Start Time'].dt.weekday
    popular_week_day = df['week'].mode()[0]
    print('Most Popular Day of the week:', week_data_int[popular_week_day])

    # find the most popular hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_types = df['Start Station'].mode()
    print("Most Popular Start Station: " + start_types[0])

    # display most commonly used end station
    end_types = df['End Station'].mode()
    print("Most Popular End Station: " + end_types[0])

    # display most frequent combination of start station and end station trip
    trip_df = (df['Start Station'] + ',' + df['End Station']).mode()
    print("Most Popular Combination of Start/End Trip: " + trip_df[0])
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_types = df['Trip Duration'].sum()
    print("Trip Duration:" + str(travel_types))


    # display mean travel time
    avg_time = df['Trip Duration'].mean()
    print("Trip Average Time: " + str(avg_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Subscribers:" + str(user_types[0]))
    print("Customers:" + str(user_types[1]) + "\n")
    
    #Display the counts of the gender if in the data frame
    if('Gender' in df):
        # Display counts of gender
        gender_types = df['Gender'].value_counts()
        print(gender_types)
        print("\n")
    else:
        print("Unfortunately there is no gender data associated with this city...\n")

    #Display if the birth year is in the data frame
    if('Birth Year' in df):
        # Display earliest, most recent, and most common year of birth
        birth_common = df['Birth Year'].mode()
        birth_early = df['Birth Year'].min()
        birth_recent = df['Birth Year'].max()
        print("Birth Year Statistics:")
        print("Most Common Year:" + str(int(birth_common)))
        print("Earliest:" + str(int(birth_early)))
        print("Most Recent:" + str(int(birth_recent)))
    else:
        print("Unfortunately there is no birth year data associated with this city...")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def process_output(df):
    """Displays the output df 5 lines at a time if the user decides to."""
    line_check = 0;
    for i in range(0, len(df), 5):
        if(line_check % 5 == 0):
            more_inp = input ("Do you wish to see the raw data results 5 lines at a time? (y/n): \n")
            if(more_inp == 'y'):
                print(df.iloc[i:i+5].to_string())
            else:
                break;


def main():
    """Runs the main application, assumes csv files are in working directory"""
    while True:
        #determine the city, month and day to filter
        city, month, day = get_filters()
        #filter the data based on the input city, month and day
        df = load_data(city, month, day)
        #apply the stats for the given df
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        #process the output df if user requests
        process_output(df)

        restart = input('\nWould you like to restart the program? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
