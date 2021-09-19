# **ETL Data covid from API data.covid19.go.id**

![image](https://user-images.githubusercontent.com/55681442/133692288-3e0001e1-98ff-450c-8148-e90d0cd75cbe.png)

This project contain about ETL using airflow, postgree and docker to get data covid19 in indonesia (34 province). The source data from data.covid19.go.id (API public data).But in this project i pass step off installation airflow in docker. if you want to know about installation airflow in docker check this [link](https://youtu.be/J6azvFhndLg).

In this DAG have 7 task, task Set_variable contains code to import variable API component and posgree variable to airflow DAG. task Get_provinsi contains code to get data province name from table provinsi and eksport to json file. Task Get_Link_API contains code to get url api from data.covid19.go.id based on province. Task Get_data contains code to get data from API and transform to JSON file. Task Move_to_postgree contains code to import data to table temp_data_covid from JSON file. Task Insert_new_data contains code to move data from temp_data_covid to data_covid table (only new data will move to data_covid). Task insert_last_update is for get last data update and insert into table last_update_covid.

## 1. Installation Instruction 

a. Copy file DAG_data_covid.py from folder 01.DAG to your DAG folder airflow

b. Make sure your python in airflow already install requirement package (see in file 03.Requirements.txt)

c. Import variabel from folder 02.Airflow variable (in that folder have 2 variable first variable for API component and the second for posgree variable)
![image](https://user-images.githubusercontent.com/55681442/133917842-8b6d1783-bcbb-483e-95bc-f0e80e985132.png)

**Note** : in variable contains server ip postgree please edit to your server ip. if you don't konw ip server postgree please check this [link](https://stackoverflow.com/questions/53610385/docker-postgres-and-pgadmin-4-connection-refused)

d. In folder DAG create folder data and in that folder create folder covid. This folder use for processing transfer variable from postgree to ariflow (using .json file and xcom in airflow)

![image](https://user-images.githubusercontent.com/55681442/133918119-2a41b3b6-ecae-4fe4-843a-a1d79c5aa9b2.png)

e. Create table data_covid, provinsi and last_update_covid (see in file 04.Table.sql). Create that table in airflow database

![image](https://user-images.githubusercontent.com/55681442/133918911-a1197cd8-0d64-41e2-8597-2d67c1252b28.png)

## 2. Running and Testing DAG

a. For trying DAG go to DAG tab search dag_data_covid and click action run (Don't forget to unpause this DAG)

![image](https://user-images.githubusercontent.com/55681442/133918327-97c65aff-e75f-41aa-853b-d28ea15fbc98.png)

b. If the DAG running well in graph view you will see all task in green border 

![image](https://user-images.githubusercontent.com/55681442/133692288-3e0001e1-98ff-450c-8148-e90d0cd75cbe.png)

c. If DAG get error check in tree view and check red box in task, click and choose yo will get the error 

![image](https://user-images.githubusercontent.com/55681442/133918447-b648dc05-adcf-4f57-ae84-64980bb68b47.png)

d. If DAG successfuly run you can check in postgree and check in table data_covid and last_update_covid

![image](https://user-images.githubusercontent.com/55681442/133919382-30f2d26d-0439-4138-a482-1dfd6f7f4042.png)
