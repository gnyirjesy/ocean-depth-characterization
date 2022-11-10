def get_season(row, month_seasons_dict):
    '''
    Description: Function to extract season from dataframe using the latitude and month
        Southern and Northern hemisphere have differing seasons so this function uses
        a dictionary to correctly map the season for the row of data.
    Input: row of dataframe, month_seasons_dict (dictionary mapping month to season)
    Output: season of the row
    '''
    if row['latitude'] <0:
        season = month_seasons_dict.get(row['month'])[1]
    else:
        season = month_seasons_dict.get(row['month'])[0]
    return(season)