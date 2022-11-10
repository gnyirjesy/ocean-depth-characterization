### this is the final python script containing period visualizations and
### initial model testing of a depth parameter inclusive xgboost on various
### feature mappings

# import dependencies
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from geopy import distance


def get_distance_series(df):
    dist_from_last = [0]
    if df.shape[0] > 1:
            for i, r in df.iloc[1:].iterrows():
                last_loc = (df.iloc[i-1].latitude, df.iloc[i-1].longitude)
                new_loc = (r.latitude, r.longitude)
                dist_from_last.append(distance.distance(last_loc, new_loc).km)
    else:
        return 0
    return dist_from_last


def create_period_data(merged_df):
    df = merged_df.copy()
    # create datetime column
    df['date'] = pd.to_datetime(df.date, format='%Y-%m-%d %H:%M:%S')
    # find splits between cycles in DAYS
    df['delta'] = ((df.date - df.date.shift()).dt.total_seconds() / 3600).fillna(0)
    # turn all cyclenumber 1s into 0 delta
    df.loc[df.cycleNumber == 1, 'delta'] = 0
    # start cycle over if time delta is over 15 days (360 hours)
    df.loc[(df.delta > 408) | (df.delta < 0), 'delta'] = 0
    # make a flag column for row at the end of a period
    df = df.reset_index().drop('index', axis=1)
    period_ls = list()
    period = 0
    for i, r in df.iloc[:-1].iterrows():
        if r['delta'] != 0:
            period_ls.append(period)
        else:
            r1 = df.iloc[i+1]
            if r1['delta'] != 0:
                period += 1
                period_ls.append(period)
            else:
                period_ls.append(np.nan)
    if df.iloc[-1]['delta'] != 0:
        period_ls.append(period)
    else:
        period_ls.append(np.nan)
    df['period'] = period_ls
    df = df.dropna()
    return df


def gather_period_observations(df, plot=False, print_results=False):
    period_df = df.copy()
    period_df['dists_from'] = get_distance_series(period_df)
    beg_lat = period_df.iloc[0].latitude
    beg_lon = period_df.iloc[0].longitude
    info_dict = {
        'float_no': period_df.iloc[0].float,
        'period_no': period_df.iloc[0].period,
        'start_date': period_df.iloc[0].date,
        'end_date': period_df.iloc[-1].date,
        'num_cycles': period_df.shape[0],
        'avg_obsv_gap_days': period_df[1:].delta.mean() / 24,
        'total_dist_km': period_df.dists_from.sum(),
        'avg_dist_km': period_df.dists_from.sum() / period_df.shape[0]
    }

    if print_results:
        print(f'Float no: {period_df.iloc[0].float}\nPeriod no: {period_df.iloc[0].period}\nStart Date: {period_df.iloc[0].date}\nEnd Date: {period_df.iloc[-1].date}')
        print(f'Observations: {period_df.shape[0]}\nAvg Time Delta: {period_df[1:].delta.mean() / 24:.2f} Days\nTotal Distance Traveled: {period_df.dists_from.sum():.2f} km')
    
    if plot:
        fig = px.density_mapbox(period_df, lat='latitude', lon='longitude', z='float', radius=8, center=dict(lat=beg_lat, lon=beg_lon), zoom=2, mapbox_style='stamen-terrain')
        fig.show()

    return info_dict

if __name__ == '__main__':
    # read in data
    PROFILE_DATA_PATH = "c:/Users/johnc/Documents/Python Scripts/ocean-depth-characterization/data/profileData.csv"
    SAT_DATA_PATH = "c:/Users/johnc/Documents/Python Scripts/ocean-depth-characterization/data/satData.csv"

    profile_df = pd.read_csv(PROFILE_DATA_PATH)
    sat_df = pd.read_csv(SAT_DATA_PATH)


    # filter curated float data based on location
    location_dict = {
        6901486 : 'North Atlantic', 
        5905071 : 'Southern Ocean',
        6901775 : 'Mediterranean',
        5906039 : 'Equatorial (Hawaii)',
        2902156 : 'Indian Ocean'
        }
    worldwide_sample_df = profile_df[profile_df.float.isin(location_dict.keys())]
    worldwide_sample_df['Location'] = worldwide_sample_df.float.apply(lambda x: location_dict[x])

    # plot the created sample
    fig, ax = plt.subplots(1, 1, figsize=(10,5))
    sns.lineplot(data=worldwide_sample_df[(worldwide_sample_df.cycleNumber == 8) & (worldwide_sample_df.PRES < 300)], x='PRES', y='CHLA', hue='Location', ax=ax)
    ax.set_title('Depth vs CHLA Measured by various gloabl floats')
    ax.set_xlabel('Depth')
    plt.savefig('c:/Users/johnc/Documents/Python Scripts/ocean-depth-characterization/visualizations/worldwide_float_distributions.png')

    # Aggregate profile data using the mean value of chlorophyll a and bbp700 nm in the sunlit portion of the ocean
    sunlit_profiles = profile_df[profile_df.PRES < 60][['float', 'cycleNumber', 'CHLA', 'BBP700']] \
        .groupby(['float', 'cycleNumber']).mean().reset_index()
    mean_chla_merged_df = sat_df.merge(sunlit_profiles, on=['float', 'cycleNumber']).drop(['LT_SAT_SST_SD', 'LT_SAT_SST_MED'], axis=1).dropna()

    # create period flags for every cycle in the float data
    period_df = create_period_data(mean_chla_merged_df)

    # create summary data within each cycle
    periods = np.unique(period_df.period)
    summary_data = [gather_period_observations(period_df[period_df.period == p].reset_index()) for p in periods]
    summary_df = pd.DataFrame(summary_data)
    summary_df = summary_df[summary_df.avg_dist_km < 150]


    # plot summary data for floats based on period data
    fig, ax = plt.subplots(2, 3, figsize=(15, 5), gridspec_kw={"height_ratios": (.8, .2)})

    ax[0, 0].set_title(f'Periods Represented: {summary_df.shape[0]}')

    sns.histplot(data=summary_df, x='num_cycles', ax=ax[0, 0])
    sns.boxplot(data=summary_df, x='num_cycles', ax=ax[1, 0])
    ax[1, 0].set_xlabel('')
    ax[0, 0].tick_params(bottom=False, labelbottom=False)
    ax[0, 0].set_xlabel('Number of subsequent cycles')

    sns.histplot(data=summary_df, x='avg_dist_km', ax=ax[0, 1])
    sns.boxplot(data=summary_df, x='avg_dist_km', ax=ax[1, 1])
    ax[1, 1].set_xlabel('')
    ax[0, 1].tick_params(bottom=False, labelbottom=False)
    ax[0, 1].set_xlabel('Total distance travelled (km)')

    sns.histplot(data=summary_df, x='avg_obsv_gap_days', ax=ax[0, 2])
    sns.boxplot(data=summary_df, x='avg_obsv_gap_days', ax=ax[1, 2])
    ax[1, 2].set_xlabel('')
    ax[0, 2].tick_params(bottom=False, labelbottom=False)
    ax[0, 2].set_xlabel('Average gap between observation cycle')

    plt.savefig('c:/Users/johnc/Documents/Python Scripts/ocean-depth-characterization/visualizations/period_summary_stats.png')

    # merge periods into depth data
    df_period_merge = profile_df.merge(period_df[['float', 'cycleNumber', 'period', 'latitude', 'longitude', 'MO_SAT_CHL']], on=['float', 'cycleNumber'])

    single_period_ill = 1701
    high_len_df = df_period_merge[df_period_merge.period == single_period_ill]

    heatmap = {}
    for date in np.unique(high_len_df.date):
        heatmap[date] = high_len_df[high_len_df.date == date].sort_values('PRES').CHLA.to_numpy()[:300]
    df_heat = pd.DataFrame(heatmap)

    long_period_df = period_df[period_df.period == single_period_ill].reset_index().drop('index', axis=1).reset_index()
    _ = gather_period_observations(long_period_df, plot=True, print_results=True)
    fig, ax = plt.subplots(1, 1, figsize=(25, 6))
    sns.heatmap(df_heat, cmap="YlGnBu", ax=ax)
    plt.savefig(f'c:/Users/johnc/Documents/Python Scripts/ocean-depth-characterization/visualizations/chla_dist_period_{single_period_ill}')