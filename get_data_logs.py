import os
import datetime
from plugins_conf import plugins, plugin_types


# Путь к файлам логов бэка
backend_logs_path = os.listdir('RegistryService/')

# Путь к файлам логов фронта
frontend_logs_path = os.listdir('RegistryService/LoggerRecordCommand')


def get_logs():
    logs_list_backend = []
    logs_list_frontend = []
    description = None
    try:
        # Запись логов бэка
        for log_file in backend_logs_path:
            if log_file != 'LoggerRecordCommand':
                with open(f"RegistryService/{log_file}", 'r') as f:
                    registry_log = f.read()
                for row in registry_log.split('\n'):
                    if row != '':
                        date_time_call = datetime.datetime.strptime(row[1:row.index(']')], '%d.%m.%Y %H:%M:%S')
                        date_time = row[1:row.index(']')]
                        date = row[7:11]
                        plugin_type = row[(row.index(']')) + 2:(row.index(': '))]
                        plugin_name = row[(row.index(': ')) + 2:]

                        names_mapping = [v for k, v in plugins.items() if k == plugin_name]
                        if names_mapping:
                            description = names_mapping[0]
                        # elif plugin_name == 'ExonTokenQuery':
                        #     description = 'Получение токена Exon'
                        else:
                            description = 'Описание отсутствует'

                        types_mapping = [v for k, v in plugin_types.items() if k == plugin_type]
                        if types_mapping:
                            plugin_type_rus = types_mapping[0]
                        else:
                            plugin_type_rus = 'undefined'

                        logs_list_backend.append([date_time_call, plugin_type, plugin_name, description, date, date_time, plugin_type_rus])

        # Запись логов фронта
        for log_file in frontend_logs_path:
            with open(f"RegistryService/LoggerRecordCommand/{log_file}", 'r') as f:
                log = f.read()
            for row in log.split('\n'):
                if row != '':
                    date_time_call = datetime.datetime.strptime(row[1:row.index(']')], '%d.%m.%Y %H:%M:%S')
                    date_time = row[1:row.index(']')]
                    date = row[7:11]
                    plugin_type = row[(row.index(']')) + 2:(row.index(': '))]
                    plugin_name = row[(row.index(': ')) + 2:]

                    names_mapping = [v for k, v in plugins.items() if k == plugin_name]
                    if names_mapping:
                        description = names_mapping[0]
                    # elif plugin_name == 'ExonTokenQuery':
                    #     description = 'Получение токена Exon'
                    else:
                        description = 'Описание отсутствует'

                    types_mapping = [v for k, v in plugin_types.items() if k == plugin_type]
                    if types_mapping:
                        plugin_type_rus = types_mapping[0]
                    else:
                        plugin_type_rus = 'undefined'

                    logs_list_frontend.append([date_time_call, plugin_type, plugin_name, description, date, date_time, plugin_type_rus])

        concated = logs_list_backend + logs_list_frontend
        # df = pd.DataFrame(concated)
        # df_sorted = df.sort_values(by=[0], ascending=False)
        # df_sorted[6] = list(range(1, len(df_sorted) + 1))
        # res = df_sorted
        # return res
        return concated
    except Exception as _ex:
        return f'Ошибка:\n {_ex}'


