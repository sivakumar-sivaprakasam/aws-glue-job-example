# Running AWS Glue Jobs Locally on Windows using WSL

Prerequisites: 

- Windows 10 or 11
- Ubuntu or any linux distribution on WSL
- OpenJDK 11
- Maven 3.6
- Python 3.8
- PostgreSQL 14 & Client tools on WSL
- Apache Spark 3.1.1 enabled with AWS Glue
- AWS Glue Library
- Utilities (Zip, Unzip)

# Installing Prereq

## Enabling WSL on Windows

You can visit this URL https://docs.microsoft.com/en-us/windows/wsl/install-manual to follow the step-by-step procedure on enabling WSL on Windows 10

## Install PostgreSQL 14 on your host Windows machine

Download PostgreSQL 14 from https://www.postgresql.org/download/

## Enable PostgreSQL to accept connection from WSL

WSL2 assigns IP address to the Windows host dynamically and the IP addresses can change without even rebooting Windows (see Notes below). So to reliably connect we'll need to:

### Allow Windows and Postgres to accept connections from the WSL2 IP address range (not allowed by default)

From WSL2, determine the Windows/Postgresql host's IP address (which is dynamic) when connecting via psql. We'll make this convenient via `.bashrc` and `alias`.

Unfortunately I couldn't find the exact specification for the WSL2 IP address range. From several tests/reboots it appears that WSL2 is assigning IP addresses primarily in range of 172.*.*.* but I have occasionally been assigned 192.*.*.* so we'll use these when configuring the firewall and Postgres.

### Add Windows Firewall Inbound Port Rule for WSL2 IP Addresses:

- Open `Windows Defender Firewall with Advanced Security`
- Click `New Rule`...
- Select `Port` for rule type
- Select `TCP` and for `Specific local ports` enter `5432`
- Select `Allow the connection`. Connecting from WSL2 won't be secure so don't select the secure option
- Select at least `Public`. Can select `Domain` and `Private` as well. 
- Name the rule e.g. `Postgres-WSL` and create it
- Right click newly created rule and select `Properties` then click on the `Scope` tab
- Under `Remote IP address`, select `These IP addresses` then click `Add`... and enter range `172.0.0.1` to `172.254.254.254`
- Repeat same steps to add IP address range `192.0.0.1` to `192.254.254.254`
- Click Apply then `OK`
- Make sure rule is enabled

### Configure Postgres to Accept Connections from WSL2 IP Addresses

Assuming a default install/setup of Postgresql for Windows the following files are located under C:\Program Files\PostgresSQL\<<Version>>\data

Verify that `postgresql.conf` has following set:

```
listen_addresses = '*'
```

This should already be set to `'*'` so nothing do here.

Update `pg_hba.conf` to allow connections from WSL2 range e.g. for Postgresl 14:

```
# TYPE  DATABASE        USER            ADDRESS                 METHOD

# IPv4 local connections:
host    all             all             127.0.0.1/32            scram-sha-256
host    all             all             172.0.0.0/8             scram-sha-256
host    all             all             192.0.0.0/8             scram-sha-256
```

Restart Postgres for changes to take effect. This can be done either from the Windows Services app or from cmd with Administrator privileges e.g. for Postgresql 14:

```
net stop postgresql-x64-14
net start postgresql-x64-14
```

## Connect to WSL

Once WSL is enabled, you can connect to WSL using following steps

- Launch `Microsoft Store`
- Search `Ubuntu 20.04`
- Click `Open` button

OR

Launch cmd with Administrator privileges and then run `wsl` command

## Installing Maven

Once you've got into WSL, run `sudo apt install maven` command to install Maven

Once it is done, verify maven installation by running `mvn --version`

## Installing PostgreSQL Client tools

Once you've got into WSL, run following commands to get PostgreSQL client tools

```
sudo apt install postgresql-client-common

sudo apt-get install postgresql-client
```

## Installing Apache Spark 3.1.1 enabled with AWS Glue

Once you've got into WSL, run the below commands to configure Apache Spark enabled with AWS Glue from AWS S3 bucket using this command

```
cd 
wget https://aws-glue-etl-artifacts.s3.amazonaws.com/glue-3.0/spark-3.1.1-amzn-0-bin-3.2.1-amzn-3.tgz
tar -xvf spark-3.1.1-amzn-0-bin-3.2.1-amzn-3.tgz
```

## Configure AWS Glue Library on WSL

Once you've got into WSL, run the below commands to configure AWS Glue library

```
cd
git clone https://github.com/awslabs/aws-glue-libs.git
``` 

## Configure environment variables

On WSL, run the below commands to update environment variables

Open `.bashrc` file in favorite editor and add following commands. Please make sure to specify correct path as per your local WSL

```
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/usr/lib/wsl/lib:/snap/bin
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export MAVEN_HOME=/usr/share/maven
export SPARK_HOME=/home/siva/spark-3.1.1-amzn-0-bin-3.2.1-amzn-3
```

### Running PySpark code 

On WSL, run the following command to launch PySpark Shell

```
cd /home/siva/aws-glue-libs/bin
./gluepyspark
```

After PySpark downloaded dependencies from Maven, you should see the pyspark prompt 

```
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /__ / .__/\_,_/_/ /_/\_\   version 3.1.1-amzn-0
      /_/

Using Python version 3.8.10 (default, Nov 26 2021 20:14:08)
Spark context Web UI available at http://172.25.17.34:4040
Spark context available as 'sc' (master = local[*], app id = local-1660040783879).
SparkSession available as 'spark'.
>>>
```