from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from get_dataframe import sorted_dataframe, full_dataframe
import datetime


app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/plugins")
async def index(request: Request):
    try:
        date_time = datetime.datetime.now().strftime('%d.%m.%Y %H:%M')
        sorted_data = sorted_dataframe()
        full_data = full_dataframe()
        row_for_sorted_data = list(range(1, len(sorted_data) + 1))
        sorted_data['row_num'] = row_for_sorted_data

        # пагинация
        page = 1
        counter1 = 0
        counter2 = 0
        length = len(sorted_data)
        num_page = []

        while counter1 != length:
            counter1 += 1
            counter2 += 1
            if counter2 < 11:
                num_page.append(page)
            else:
                page += 1
                counter2 = 1
                num_page.append(page)

        sorted_data['page'] = num_page
        pages = list(set(num_page))
        total_pages = len(pages)
        total_calls = sum(list(sorted_data['count']))

        min_date = datetime.datetime.strftime(full_data['date_time_tech'].min(), '%d.%m.%Y')
        max_date = datetime.datetime.strftime(full_data['date_time_tech'].max(), '%d.%m.%Y')

        return templates.TemplateResponse("index.html", {
            "request": request,
            "sorted_data": sorted_data,
            "date_time": date_time,
            "pages": pages,
            "total_pages": total_pages,
            "total_calls": total_calls,
            "min_date": min_date,
            "max_date": max_date
        })
    except Exception as _ex:
        return f"Ошибка:\n{_ex}"


@app.get("/plugins/dashboard")
async def dashboard(request: Request):
    try:
        sorted_data = sorted_dataframe()
        full_data = full_dataframe()
        sorted_data['per'] = [round(100 / len(full_data) * i, 2) if i != 0 else 0 for i in list(sorted_data['count'])]
        sorted_data_without_unused = sorted_data[sorted_data['count'] != 0]
        row_for_sorted_data = list(range(1, len(sorted_data_without_unused) + 1))
        sorted_data_without_unused['row_num'] = row_for_sorted_data

        # пагинация
        page = 1
        counter1 = 0
        counter2 = 0
        length = len(sorted_data_without_unused)
        num_page = []

        while counter1 != length:
            counter1 += 1
            counter2 += 1
            if counter2 < 11:
                num_page.append(page)
            else:
                page += 1
                counter2 = 1
                num_page.append(page)

        pages = list(set(num_page))
        sorted_data_without_unused['page'] = num_page
        total_pages = len(pages)

        total_plugins = len(sorted_data)
        total_calls = len(full_data)
        total_unused = len(sorted_data[sorted_data['count'] == 0])
        total_backend = len(sorted_data[sorted_data['plugin_type_rus'] == 'Бэкенд'])
        total_frontend = len(sorted_data[sorted_data['plugin_type_rus'] == 'Фронтенд'])

        tmp_df = full_dataframe()
        tmp_df['month'] = [datetime.datetime.strftime(date, '%m.%Y') for date in list(full_data['date_time_tech'])]
        tmp_df['count'] = [1 for _ in list(full_data['date_time_tech'])]
        tmp_grouped_df = tmp_df.groupby("month").count()
        tmp_reset_index_df = tmp_grouped_df.reset_index()
        visualization_df = tmp_reset_index_df.sort_values(by='month', ascending=True, ignore_index=True)
        visualization_categories = list(visualization_df['month'])
        last_category = visualization_categories[-1]
        visualization_data = list(visualization_df['count'])

        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "sorted_data_without_unused": sorted_data_without_unused,
            "total_plugins": total_plugins,
            "total_calls": total_calls,
            "total_unused": total_unused,
            "total_backend": total_backend,
            "total_frontend": total_frontend,
            "pages": pages,
            "total_pages": total_pages,
            "visualization_categories": visualization_categories,
            "visualization_data": visualization_data,
            "last_category": last_category
        })

    except Exception as _ex:
        return f"Ошибка:\n{_ex}"





