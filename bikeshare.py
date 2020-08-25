import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def invalid_input_message(mylist):
    # tells the user that the input is invalid and prints all possible valid inputs which were passed via 'mylist'
    print('\nInput invalid. Possible inputs are: ')
    for entry in mylist:
        print(entry)

def print_current_filter(cities, months, days):
    # prints the current filter settings
    print('Current filters:', end='')
    categories = {'Cities': cities, 'Months': months, 'Days': days}
    for cat in categories: #e.g. 'Cities'
        # check if all cities are in filter.
        all = True
        for entry in categories[cat]: # entry can be e.g. chicago, new york city, washington
            if categories[cat][entry] == False:
                all = False # if any city is missing from the filter, 'all' is set to False
        # if all cities are in the filter, print "Cities: all,"
        if all == True:
            print('\n' + cat.capitalize() + ': all', end=', ')
        # if only a part of the cities is in the filter, print only these city names
        else:
            print('\n' + cat.capitalize(), end=': ')
            for entry in categories[cat]:
                if categories[cat][entry] == True:
                    print(entry.capitalize(), end=', ')
    print('\n')

def change_filters(cities, months, days):
    """
    Lets the user manipulate the True/False dictionaries 'cities', 'months' and 'days'

    Returns:
        (dict) cities - a dictionary indicating for each city if it is in the filter (True) or not (False)
        (dict) months - a dictionary indicating for each month if it is in the filter (True) or not (False)
        (dict) days - a dictionary indicating for each day of week if it is in the filter (True) or not (False)
    """

    categories = {'cities': cities, 'months': months, 'days': days} # auxiliary dictionary to refer from string names to dictionaries
    names = {'cities': 'city', 'months': 'month', 'days': 'day'} # auxiliary dictionary just containing the singular forms

    for cat in categories: # all following examples are for cities, e.g. cat = 'cities'
        while True:
            print('Enter n to apply no {} filter.'.format(names[cat]))
            print('Enter a to add a {} to the filter.'.format(names[cat]))
            print('Enter o to omit a {} from the filter.'.format(names[cat]))
            print('Enter f to filter for one {} only.'.format(names[cat]))
            change = input('Every other input will leave the filter unchanged: \n')
            print('\n')
            if change == 'n': # apply no filter
                for entry in categories[cat]: # entry = e.g. chicago
                    categories[cat][entry] = True # set dictionary value for every city to True
            if change == 'a': # add a city to the filter
                while True:
                    add = input('To add a {} enter its name: '.format(names[cat])) # ask for city name
                    if add.lower() in categories[cat]: # check if city name is valid
                        categories[cat][add.lower()] = True # set dicitonary value for this city to True
                        break
                    else:
                        invalid_input_message(categories[cat].keys()) # give user a complete list of valid inputs, e.g. cities
            if change == 'o': # omit a city from the filter
                while True:
                    omit = input('To omit a {} enter its name: '.format(names[cat])) # ask for city name
                    if omit.lower() in categories[cat]: # check if city name is valid
                        categories[cat][omit.lower()] = False # set dictionary value for this city to False
                        allfalse = True
                        for entry in categories[cat]: # entry can be e.g. chicago, new york city, washington
                            if categories[cat][entry] == True:
                                allfalse = False # if any city is in the filter, 'allfalse' is set to False
                        if allfalse == True: # check if the omitted city was the last city in the filter
                            categories[cat][omit.lower()] = True # add the omitted city back to the filter
                            print('\nCannot omit the last {} from the filter'.format(names[cat]))
                        break
                    else:
                        invalid_input_message(categories[cat].keys()) # give user a complete list of valid inputs, e.g. cities
            if change == 'f': # allows user to change filter immediately to one city only
                while True:
                    filter = input('To filter for a {} enter its name: '.format(names[cat])) #ask for city name
                    if filter.lower() in categories[cat]: #check if city name is valid
                        for entry in categories[cat]:
                            categories[cat][entry] = False #omit all cities from the filter
                        categories[cat][filter.lower()] = True #add the specified city back to the filter
                        break
                    else:
                        invalid_input_message(categories[cat].keys())
            print('\n')
            print_current_filter(cities, months, days) #print current filter settings to give user
            proceed = input('Enter yes if you are done changing the {0} filter. Otherwise you will continue to change the {0} filter:\n'.format(names[cat]))
            print('\n')
            if proceed.lower() == 'yes':
                break

    print('-'*40)
    return cities, months, days


def load_data(cities, months, days):
    """
    Loads data for the specified cities and filters by months and days if applicable.

    Args:
        (dict) cities - a dictionary with the names of the cities and an indication whether to analyze them (True) or not (False)
        (dict) months - a dictionary with the names of the months and an indiction whether to filter by them (True) or not (False)
        (dict) days - a dictionary with the names of the days of week and an whether to filter by them (True) or not (False)
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # create new DataFrame and add data for all requested cities from the respective files
    df = pd.DataFrame()
    for city in cities:
        if cities[city] == True:
            newdf = pd.read_csv(CITY_DATA[city])
            newdf['city'] = city #add an extra column to indicate from which city the respective lines in the DataFrame are
            df = df.append(newdf, sort=False)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week and hour of day from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour

    monthtonumber = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6}
    # instead of True/False dictionary with all month names (e.g. 'january') as keys,
    # define 'months' as list of month numbers (e.g. 1) containing only months in filter
    months = [monthtonumber[month] for month in months if months[month] == True]

    df = df[df['month'].isin(months)] # filter df to contain only entries with month in filter

    daytonumber = {'sunday': 0, 'monday': 1, 'tuesday': 2, 'wednesday': 3, 'thursday': 4, 'friday': 5, 'saturday': 6}
    # instead of True/False dictionary with all day names (e.g. 'sunday') as keys,
    # define 'days' as list of day numbers (e.g. 0) containing only days in filter
    days = [daytonumber[day] for day in days if days[day] == True]

    df = df[df['day_of_week'].isin(days)] # filter df to contain only entries with day in filter

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    numberstomonths = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June'}
    months = df['month'].value_counts() # Series containing for each month the number of entries from this month
    print('{} was the most common month with {} trips.'.format(numberstomonths[months.idxmax()], months.max()))

    numberstodays = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday'}
    days = df['day_of_week'].value_counts() # Series containing for each day of week the number of entries from this month
    print('{} was the most common day with {} trips.'.format(numberstodays[days.idxmax()], days.max()))

    hours = df['hour'].value_counts()
    print('From {}:00 to {}:00 was the most common hour with {} trips.'.format(hours.idxmax(), int(hours.idxmax()) + 1, hours.max()))

    print('\nThis took {} seconds.'.format(time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    df['start_station_city'] = df['Start Station'] + ' in ' + df['city'].str.capitalize()
    start_stations = df['start_station_city'].value_counts()
    print('{} was the most common start station with {} trips starting there.'.format(start_stations.idxmax(), start_stations.max()))

    df['end_station_city'] = df['End Station'] + ' in ' + df['city'].str.capitalize()
    end_stations = df['end_station_city'].value_counts()
    print('{} was the most common end station with {} trips ending there.'.format(end_stations.idxmax(), end_stations.max()))

    df['trip'] = 'from ' + df['Start Station'] + ' to ' + df['End Station'] + ' in ' + df['city'].str.capitalize()
    trips = df['trip'].value_counts()
    print('The most common trip was {} with a total count of {}.'.format(trips.idxmax(), trips.max()))

    print('\nThis took {} seconds.'.format(time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    print('The total travel time in seconds was {}.'.format(df['Trip Duration'].astype(float).sum()))

    print('The mean travel time in seconds was {}.'.format(df['Trip Duration'].astype(float).mean()))

    print('\nThis took {} seconds.'.format(time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print('Counts of user types (no data for Washington):\n', user_types)

    try:
        genders = df['Gender'].value_counts()
        print('Counts of gender (no data for Washington):\n', genders)
    except KeyError: # KeyError occurs when loading only washington.csv, because there is no Gender column
        pass         # just don't display the gender count

    try:
        earliest_year_of_birth = df['Birth Year'].min()
        most_recent_year_of_birth = df['Birth Year'].max()
        most_common_year_of_birth = df['Birth Year'].mode()[0]
        print('The earliest year of birth was {}.'.format(earliest_year_of_birth))
        print('The most recent year of birth was {}.'.format(most_recent_year_of_birth))
        print('The most common year of birth was {}.'.format(most_common_year_of_birth))
    except KeyError: # KeyError occurs when loading only washington.csv
        pass         # just don't display birth year statistics

    print('\nThis took {} seconds.'.format(time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displays raw data for a sample of five rows."""

    dfsample = df.sample(n=5) # draw a sample of five rows from df
    print(dfsample.index)
    for index in dfsample.index:
        row = dfsample.loc[index]
        print('\n')
        print('Index:         {},'.format(index))
        print('Start Station: {},'.format(row.loc['Start Station']))
        print('End Station:   {},'.format(row.loc['End Station']))
        print('City:          {},'.format(row.loc['city'].capitalize()))
        print('Start Time:    {},'.format(row.loc['Start Time']))
        print('End Time:      {},'.format(row.loc['End Time']))
        print('Trip Duration: {},'.format(row.loc['Trip Duration']))
        print('User Type:     {},'.format(row.loc['User Type']))
        try:
            print('Gender:        {},'.format(row.loc['Gender']))
        except KeyError:
            pass
        try:
            print('Birth Year:    {}'.format(row.loc['Birth Year']) + '}')
        except KeyError:
            pass

def main():
    all_cities = ['chicago', 'new york city', 'washington']
    all_months = ['january', 'february', 'march', 'april', 'may', 'june']
    all_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    cities = {city : True for city in all_cities}
    months = {month : True for month in all_months}
    days = {day : True for day in all_days}
    while True:
        print('Hello! Let\'s explore some US bikeshare data!\n')
        print_current_filter(cities, months, days)
        changefilters = input('\nTo change filters enter yes. Any other input will leave filters unchanged.\n')
        print('\n')
        if changefilters.lower() == 'yes':
            cities, months, days = change_filters(cities, months, days)

        print('Loading data and calculating statistics. Please wait.')

        df = load_data(cities, months, days)

        time_stats(df)          # Displays statistics on the most frequent times of travel.
        station_stats(df)       # Displays statistics on the most popular stations and trip.
        trip_duration_stats(df) # Displays statistics on the total and average trip duration.
        user_stats(df)          # Displays statistics on bikeshare users.

        while True:
            show_raw_data = input('\nTo display some raw data enter yes. Skip with any other input.\n')
            if show_raw_data.lower() == 'yes':
                raw_data(df)    # Displays raw data for a sample of five rows.
            else:
                break

        restart = input('\nWould you like to continue exploring US bikeshare data? To continue exploring enter yes.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
