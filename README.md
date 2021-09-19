# **ETL Data covid from API data.covid19.go.id**

![image](https://user-images.githubusercontent.com/55681442/133692288-3e0001e1-98ff-450c-8148-e90d0cd75cbe.png)

This project contain about ETL using airflow, postgree and docker to get data covid19 in indonesia (34 province). The source data from data.covid19.go.id (API public data).But in this project i pass step off installation airflow in docker. if you want to know about installation airflow in docker check this [link](https://youtu.be/J6azvFhndLg).

## 1. Installation Instruction 

\t a. Copy file DAG_data_covid.py from folder 01.DAG to your DAG folder airflow
\t b. Make sure your python in airflow already install requirement package (see in file 03.Requirements.txt)
\t c. Import variabel from folder 02.Airflow variable (in that folder have 2 variable first variable for API component and the second for posgree variable)
![image](https://user-images.githubusercontent.com/55681442/133917842-8b6d1783-bcbb-483e-95bc-f0e80e985132.png)

