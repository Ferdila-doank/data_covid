from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.models import Variable

from random import randint
from datetime import datetime

import requests
from json import loads
import pandas as pd
import math
import numpy as np
from sqlalchemy import create_engine

def Set_Variable(ti):
    dag_config_API = Variable.get("API_component",deserialize_json=True)

    path_provinsi = dag_config_API["path_provinsi"]
    prefix = dag_config_API["prefix"]
    suffix = dag_config_API["suffix"]
    path_dest = dag_config_API["path_dest"]
    path_source = dag_config_API["path_source"]

    ti.xcom_push(key='path_provinsi', value=path_provinsi)
    ti.xcom_push(key='prefix', value=prefix)
    ti.xcom_push(key='suffix', value=suffix)
    ti.xcom_push(key='path_dest', value=path_dest)    
    ti.xcom_push(key='path_source', value=path_source)

    dag_config_Postgre = Variable.get("postgre_server",deserialize_json=True)
    username = dag_config_Postgre["username"]
    password = dag_config_Postgre["password"]
    server = dag_config_Postgre["server"]
    port = dag_config_Postgre["port"]
    database = dag_config_Postgre["database"]   

    ti.xcom_push(key='username', value=username)
    ti.xcom_push(key='password', value=password)
    ti.xcom_push(key='server', value=server)
    ti.xcom_push(key='port', value=port)    
    ti.xcom_push(key='database', value=database)

def Get_Link_API(ti):
    url_api = []

    path_provinsi = ti.xcom_pull(key='path_provinsi', task_ids= 'Set_Variable')
    prefix = ti.xcom_pull(key='prefix', task_ids= 'Set_Variable')
    suffix = ti.xcom_pull(key='suffix', task_ids= 'Set_Variable')

    df_prov = pd.read_json(path_provinsi, lines=True)

    for row in range (0,len(df_prov)):
        nama_provinsi = df_prov['prov_name'][row]
        url = prefix + nama_provinsi + suffix
        url_api.append(url)

    print(url_api)
    ti.xcom_push(key='url_api', value=url_api )

def convert_ts(x):

    if math.isnan(x) == True:
        your_dt = np.nan
    else:
        timestamp = abs(round(float(x)))
        your_dt = datetime.fromtimestamp(timestamp/1000)
    return (your_dt)

def Get_data(ti):

    path_dest = ti.xcom_pull(key='path_dest', task_ids= 'Set_Variable')

    data_covid = pd.DataFrame(columns=['tanggal','KASUS','MENINGGAL','SEMBUH','DIRAWAT_OR_ISOLASI','AKUMULASI_KASUS','AKUMULASI_SEMBUH','AKUMULASI_MENINGGAL','AKUMULASI_DIRAWAT_OR_ISOLASI','last_date','provinsi'])
    url_data =  ti.xcom_pull(key='url_api', task_ids= 'Get_Link_API')

    for i in url_data:
        print(i)
        response = requests.get(i)
        data = loads(response.text)
        
        last_date = data["last_date"]
        provinsi =  data["provinsi"]
        df_list_perkembangan = pd.DataFrame(data["list_perkembangan"])
        df_list_perkembangan['tanggal']=df_list_perkembangan.tanggal.apply(lambda x: convert_ts(x))
        df_list_perkembangan['last_date'] = last_date
        df_list_perkembangan['provinsi'] = provinsi
        print(df_list_perkembangan.head(1))
        data_covid = data_covid.append(df_list_perkembangan, ignore_index= True)

    print(data_covid.info())
    data_covid.to_json(path_dest, orient='records', lines=True)

def Move_to_Postgre(ti):

    username = ti.xcom_pull(key='username', task_ids= 'Set_Variable')
    password = ti.xcom_pull(key='password', task_ids= 'Set_Variable')
    server = ti.xcom_pull(key='server', task_ids= 'Set_Variable')
    port = ti.xcom_pull(key='port', task_ids= 'Set_Variable')
    database = ti.xcom_pull(key='database', task_ids= 'Set_Variable')
    path_source = ti.xcom_pull(key='path_source', task_ids= 'Set_Variable')

    data_covid = pd.read_json(path_source, lines=True)

    data_covid['tanggal']=data_covid.tanggal.apply(lambda x: convert_ts(x))
    data_covid['KASUS'] = pd.to_numeric(data_covid['KASUS'], errors='coerce')
    data_covid['MENINGGAL'] = pd.to_numeric(data_covid['MENINGGAL'], errors='coerce')
    data_covid['SEMBUH'] = pd.to_numeric(data_covid['SEMBUH'], errors='coerce')
    data_covid['DIRAWAT_OR_ISOLASI'] = pd.to_numeric(data_covid['DIRAWAT_OR_ISOLASI'], errors='coerce')
    data_covid['AKUMULASI_KASUS'] = pd.to_numeric(data_covid['AKUMULASI_KASUS'], errors='coerce')
    data_covid['AKUMULASI_SEMBUH'] = pd.to_numeric(data_covid['AKUMULASI_SEMBUH'], errors='coerce')
    data_covid['AKUMULASI_MENINGGAL'] = pd.to_numeric(data_covid['AKUMULASI_MENINGGAL'], errors='coerce')
    data_covid['AKUMULASI_DIRAWAT_OR_ISOLASI'] = pd.to_numeric(data_covid['AKUMULASI_DIRAWAT_OR_ISOLASI'], errors='coerce')
    data_covid['last_date'] = pd.to_datetime(data_covid['last_date'], format="%Y-%m-%d",errors='coerce')    

    engine = create_engine('postgresql://' + username + ':' + password + '@' + server + ':' + port + '/' + database)
    data_covid.to_sql(name='temp_data_covid',con=engine,index=False, if_exists='replace')

def Insert_new_data(ti):
    username = ti.xcom_pull(key='username', task_ids= 'Set_Variable')
    password = ti.xcom_pull(key='password', task_ids= 'Set_Variable')
    server = ti.xcom_pull(key='server', task_ids= 'Set_Variable')
    port = ti.xcom_pull(key='port', task_ids= 'Set_Variable')
    database = ti.xcom_pull(key='database', task_ids= 'Set_Variable')

    engine = create_engine('postgresql://' + username + ':' + password + '@' + server + ':' + port + '/' + database)
    sql = engine.execute(
    'insert into data_covid("tanggal","KASUS","MENINGGAL","SEMBUH","DIRAWAT_OR_ISOLASI","AKUMULASI_KASUS","AKUMULASI_SEMBUH","AKUMULASI_MENINGGAL", '
    '"AKUMULASI_DIRAWAT_OR_ISOLASI","last_date","provinsi") '
    'select "tanggal","KASUS","MENINGGAL","SEMBUH","DIRAWAT_OR_ISOLASI","AKUMULASI_KASUS","AKUMULASI_SEMBUH","AKUMULASI_MENINGGAL", '
    '"AKUMULASI_DIRAWAT_OR_ISOLASI","last_date","provinsi" from temp_data_covid tdc '
    'where concat(tdc.tanggal,tdc.provinsi) ' 
    'not in (select concat(dc.tanggal,dc.provinsi) from data_covid dc)'
    )
    print("Row Added = ", sql.rowcount)

def Insert_last_update(ti):
    username = ti.xcom_pull(key='username', task_ids= 'Set_Variable')
    password = ti.xcom_pull(key='password', task_ids= 'Set_Variable')
    server = ti.xcom_pull(key='server', task_ids= 'Set_Variable')
    port = ti.xcom_pull(key='port', task_ids= 'Set_Variable')
    database = ti.xcom_pull(key='database', task_ids= 'Set_Variable')

    engine = create_engine('postgresql://' + username + ':' + password + '@' + server + ':' + port + '/' + database)
    sql_delete = engine.execute(
    'delete from last_update_covid'
    )
    print("Row Deleted = ", sql_delete.rowcount)

    sql_insert = engine.execute(
    'insert into last_update_covid '
    '("tanggal", "last_date","AKUMULASI_KASUS", "AKUMULASI_SEMBUH", "AKUMULASI_MENINGGAL", "AKUMULASI_DIRAWAT_OR_ISOLASI","provinsi") '
    'select "tanggal", "last_date","AKUMULASI_KASUS", "AKUMULASI_SEMBUH", "AKUMULASI_MENINGGAL", "AKUMULASI_DIRAWAT_OR_ISOLASI","provinsi" '
    'from (select *, row_number() over (partition by x.provinsi order by x.tanggal desc) as ranks '
    'from (select * from data_covid) as x) as y '
    'where y.ranks = 1 order by y.ranks '
    )
    print("Row Added = ", sql_insert.rowcount)   

def Get_provinsi(ti):
    username = ti.xcom_pull(key='username', task_ids= 'Set_Variable')
    password = ti.xcom_pull(key='password', task_ids= 'Set_Variable')
    server = ti.xcom_pull(key='server', task_ids= 'Set_Variable')
    port = ti.xcom_pull(key='port', task_ids= 'Set_Variable')
    database = ti.xcom_pull(key='database', task_ids= 'Set_Variable')
    path_provinsi = ti.xcom_pull(key='path_provinsi', task_ids= 'Set_Variable')

    engine = 'postgresql://' + username + ':' + password + '@' + server + ':' + port + '/' + database
    df = pd.read_sql('select * from provinsi', con = engine)

    df.to_json(path_provinsi, orient='records', lines=True)

with DAG("dag_data_covid", start_date=datetime(2021, 8, 21),
    schedule_interval="@daily", catchup=False) as dag:

        Set_Variable = PythonOperator(
            task_id="Set_Variable",
            python_callable= Set_Variable
        )

        Get_data = PythonOperator(
            task_id="Get_data",
            python_callable= Get_data
        )

        Move_to_Postgre = PythonOperator(
            task_id="Move_to_Postgre",
            python_callable= Move_to_Postgre
        )

        Get_Link_API = PythonOperator(
            task_id="Get_Link_API",
            python_callable= Get_Link_API
        )

        Insert_new_data = PythonOperator(
            task_id="Insert_new_data",
            python_callable= Insert_new_data
        )

        Insert_last_update = PythonOperator(
            task_id="Insert_last_update",
            python_callable= Insert_last_update
        )

        Get_provinsi = PythonOperator(
            task_id="Get_provinsi",
            python_callable= Get_provinsi
        )

        Set_Variable >> Get_provinsi >> Get_Link_API >> Get_data >> Move_to_Postgre >> Insert_new_data >> Insert_last_update
