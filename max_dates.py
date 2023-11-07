import pandas as pd
import datetime


def get_max_date(full_data, sorted_data):
    try:
        df = pd.DataFrame()
        full_data = full_data
        df2 = sorted_data
        df['plugin_name'] = full_data['plugin_name']
        df['date_time_tech'] = full_data['date_time_tech']
        max_date_df = df.groupby('plugin_name').max()
        max_dates = [datetime.datetime.strftime(date_time, '%d.%m.%Y %H:%M') for date_time in
                     list(max_date_df['date_time_tech'])]
        max_date_df['max_dates'] = max_dates
        reset_index_df = max_date_df.reset_index()
        unused_df = pd.DataFrame()
        unused_names = []
        unused_dates = []
        for name in (df2['plugin_name']):
            if name not in list(reset_index_df['plugin_name']):
                unused_names.append(name)
                unused_dates.append('0')
        unused_df['plugin_name'] = unused_names
        unused_df['date_time_tech'] = [datetime.datetime.strptime('2023-01-01 00:00:00', '%Y-%m-%d %H:%M:%S') for _ in
                                       unused_names]
        unused_df['max_dates'] = unused_dates
        res_df = pd.concat([reset_index_df, unused_df])
        plugins_lst = []
        for i, j in enumerate(list(res_df['plugin_name'])):
            for k, v in enumerate(list(res_df['max_dates'])):
                if i == k:
                    plugins_lst.append((j, v))
        return plugins_lst
    except Exception as _ex:
        return f"Ошибка\n{_ex}"
