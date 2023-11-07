from get_data_logs import get_logs
import pandas as pd
from plugins_conf import plugins


def full_dataframe():
    try:
        df = pd.DataFrame(get_logs())
        df = df.rename(columns={
            df.columns[0]: "date_time_tech",
            df.columns[1]: "plugin_type",
            df.columns[2]: "plugin_name",
            df.columns[3]: "plugin_description",
            df.columns[4]: "year",
            df.columns[5]: "date_time",
            df.columns[6]: "plugin_type_rus",
        })
        df['row_num'] = list(range(1, len(df) + 1))
        return df
    except Exception as _ex:
        return f"Ошибка\n{_ex}"


def sorted_dataframe():
    try:
        df = pd.DataFrame(get_logs())
        df = df.rename(columns={
            df.columns[0]: "date_time_tech",
            df.columns[1]: "plugin_type",
            df.columns[2]: "plugin_name",
            df.columns[3]: "plugin_description",
            df.columns[4]: "year",
            df.columns[5]: "date_time",
            df.columns[6]: "plugin_type_rus",
        })
        df['row_num'] = list(range(1, len(df) + 1))

        sorted_df = df.sort_values(by=['date_time_tech'], ascending=False, ignore_index=True)
        sorted_df['row_num'] = list(range(1, len(sorted_df) + 1))
        grouped_df = sorted_df.groupby(['plugin_name', 'plugin_type_rus', 'plugin_description']).count()
        reset_index_df = grouped_df.reset_index()
        sorted_df = reset_index_df.sort_values(by='row_num', ascending=False, ignore_index=True)

        res_df = pd.DataFrame()
        res_df['plugin_name'] = sorted_df['plugin_name']
        res_df['plugin_type_rus'] = sorted_df['plugin_type_rus']
        res_df['plugin_description'] = sorted_df['plugin_description']
        res_df['count'] = sorted_df['row_num']

        plugins_in_logs = [i for i in res_df['plugin_name']]
        unused_plugins = []

        for k, v in plugins.items():
            if k not in plugins_in_logs:
                unused_plugins.append([
                    k,
                    "Бэкенд",
                    v,
                    0
                ])

        unused_df = pd.DataFrame(unused_plugins)
        unused_df = unused_df.rename(columns={
            unused_df.columns[0]: "plugin_name",
            unused_df.columns[1]: "plugin_type_rus",
            unused_df.columns[2]: "plugin_description",
            unused_df.columns[3]: "count",
        })

        # concated_df = res_df
        concated_df = pd.concat([res_df, unused_df], ignore_index=True)

        return concated_df
    except Exception as _ex:
        return f"Ошибка\n{_ex}"







