# Running Sample Glue Job on WSL

Please go through `README.md` to configure the pre-requisities

Once it is done, in order to run the example, we need followings:

- DB (testdb) & Schema (test) created in PostgreSQL
- Tables created in test schema. Refer `country.sql` and `employee.sql` for the script
- Postgre client driver
- Raw data files `country.csv` and `employee_list.csv`
- PostgreSQL jdbc driver `postgresql-42.2.26.jar`

Import all those files into your WSL. 

## Raw data Schema

### Country.csv

- country_id
- country_name

### Employee_list.csv

- employee_id
- employee_name
- country_id
- employee_type
- employee_status

## ETL Business Function

In the `glue-etl-example.py` script, I've used the PostgreSQL host IP address and port #. Please make sure to specify the host IP address and port # from your machine.

In WSL2 you need to use host IP to connect. To get host IP

```
grep nameserver /etc/resolv.conf | awk '{print $2}'
```

### Country table standardization

- Load `country.csv` data into a dataframe which does not have proper sequence value
- Using `zipWithIndex` method to generate new sequence value (starting from 1, 2, ...)
- Save this new dataframe data into `country` table

### Employee table standardization

- Load `employee_list.csv` data into a dataframe
- Join this dataframe with dataframe from `country.csv` using `country_id` field as joining condition
- Drop duplicate country_id columns from merged result dataframe
- Load data from PostgreSQL `country` table and assign it to a dataframe
- Join merged dataframe with data retrieved from PostgreSQL db using `country_name` field as joining condition
- Now, we'll have target dataframe of employee standardized with new `country_id` 
- Push the result dataframe into `employee` table

## Any queries?

Please feel free to reach me out in case you have any queries. Happy Learning!!!
