# normalized all examples with respect to the euphotic zone depth estimation, discarding obselete observations
import numpy as np
import pandas as pd
import os


import warnings
warnings.filterwarnings('ignore')


ABS_PATH = os.getcwd()
DATA_PATH = ABS_PATH + '/data/float_loc_data_new_vars2.csv'
SAVE_PATH = ABS_PATH + '/data/float_sat_normalized_depth.csv'

UPPER_LIM = 75     # search for euphotic depth after the maximum between this value (m) and the depth of the detected peak above LOWER_LIM (upper as in closer to surface); must be greater than 0
LOWER_LIM = 250     # the lowest depth (m) at or above which the CHLA peak can be identified (lower as in further from surface)
ERR = 0.01
WINDOW_SIZE = 5     # the number of CHLA values to consider in the rolling average in estimate_euphotic_depth

UPPER_DEPTH = 75     # the highest (nearest to surface) tolerable euphotic zone maximum depth estimate
LOWER_DEPTH = 300     # the deepest (furthest from surface) tolerable euphotic zone maximum depth estimate



class DepthNormalizer():
    
    
    def __init__(self, upper_lim, lower_lim, err, window_size, upper_depth, lower_depth):
        assert upper_lim > 0, 'upper_lim must be > 0'
        self.upper_lim = upper_lim
        self.lower_lim = lower_lim
        self.err = err
        self.window_size = window_size  
        self.upper_depth = upper_depth
        self.lower_depth = lower_depth
        
        
    def estimate_euphotic_depth(self, cycle_df):
        # ensure cycle_df is ordered by ascending PRES value with index reset
        cycle_df = cycle_df.sort_values(by='PRES', ascending=True).reset_index(drop=True)
        
        tmp_df = cycle_df[cycle_df['PRES'] <= self.lower_lim].reset_index(drop=True)
        if tmp_df.shape[0] == 0:
            return None     # no observations above 250m; disregard cycle
        max_chla = max(tmp_df['CHLA'])
        if max_chla == 0:
            return None     # cycle contains only 0 (or previously negative) CHLA observations
        
        # find the index of this maximum CHLA value in the CHLA sequence
        max_chla_idx = list(cycle_df['CHLA']).index(max_chla)
        start_idx = cycle_df[cycle_df['PRES'] < self.upper_lim].shape[0] + 1
        start_idx = max(start_idx, max_chla_idx)
        
        # obtain estimate for bottom of euphotic zone
        euphotic_depth_estimate = None
        min_chla_after_peak = min(tmp_df['CHLA'])
        chla_thresh = max(min_chla_after_peak, 0.01*(max_chla-min_chla_after_peak))
        
        err = self.err
        while max_chla <= err:
            err /= 100     # decrease error for cycles with abnormally small CHLA values

        for i in range(tmp_df.shape[0]):
            window_df = tmp_df.loc[i:i+self.window_size]
            if np.mean(window_df['CHLA']) - chla_thresh < err:
                min_chla = min(window_df['CHLA'])
                euphotic_depth_estimate = window_df[window_df['CHLA']==min_chla].reset_index(drop=True).loc[0,'PRES']
                break
        
        return euphotic_depth_estimate
    
    
    def normalize_df(self, df):
        print('Normalizing depths...')
        # initialize dataframe to keep results
        normalized_df = pd.DataFrame(columns=list(df.columns))
        normalized_df.insert(loc=list(df.columns).index('PRES')+1, column='normalized_depth', value=[])
        
        floats = np.unique(df['float'])
        for num, f in enumerate(floats):
            float_df = df[df['float'] == f]
            cycles = np.unique(float_df['cycleNumber'])
            float_results_df = pd.DataFrame(columns=list(df.columns[:-2]) + ['normalized_depth'] + list(df.columns[-2:]))

            for c in cycles:
                euphotic_depth_estimate = None
                
                cycle_df = float_df[float_df['cycleNumber'] == c].sort_values(by='PRES', ascending=True).reset_index(drop=True)
                euphotic_depth_estimate = self.estimate_euphotic_depth(cycle_df)

                if euphotic_depth_estimate is None or euphotic_depth_estimate < self.upper_depth or euphotic_depth_estimate > self.lower_depth:
                    # guess is invalid
                    continue

                # else, guess is valid; normalize and add results to dataframe
                cycle_df = cycle_df[cycle_df['PRES'] <= euphotic_depth_estimate]
                # note: normalization does not risk division by 0 because only depths beyond UPPER_LIM > 0 are considered
                cycle_df.insert(loc=list(cycle_df.columns).index('PRES')+1,
                                column='normalized_depth',
                                value=[d/euphotic_depth_estimate for d in cycle_df['PRES']])
                float_results_df = pd.concat([float_results_df, cycle_df])

            # add results to final dataframe
            normalized_df = pd.concat([normalized_df, float_results_df])
            
        return normalized_df.drop_duplicates().reset_index(drop=True)
    
        
        
if __name__ == '__main__':
    
    # read data, disregard values below 500 m (from domain knowledge), and raise negative CHLA values to 0
    df = pd.read_csv(DATA_PATH)
    df = df[~df['CHLA'].isna()].reset_index(drop=True)
    df = df[df['PRES'] <= 500]
    df.loc[df['CHLA'] < 0, 'CHLA'] = 0
    
    # instantiate EuphoticDepthEstimator instance
    depth_normalizer = DepthNormalizer(UPPER_LIM, LOWER_LIM, ERR, WINDOW_SIZE, UPPER_DEPTH, LOWER_DEPTH)
    normalized_df = depth_normalizer.normalize_df(df)
   
    # save the results
    normalized_df.to_csv(SAVE_PATH, index=False)
    print(f'Depth normalization done -- results saved to {SAVE_PATH}')



