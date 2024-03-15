# MariaDB MaxScale Docker image

This Docker image runs the latest 2.4 version of MariaDB MaxScale.

Project Overview:
In this project, I demonstrate the implementation of a sharded SQL database using Docker-compose containers running MaxScale. 
The goal is to showcase how to query a sharded database as if it were a single database, thereby enhancing performance and reliability, especially as data volume increases.

Prerequisites
Before proceeding, ensure the following dependencies are installed:

Docker on Ubuntu 23.10 Codename: Mantic
MySQL Connector  
sudo apt install python3-pip
pip3 install mysql-connector

Docker Compose  
sudo apt install docker-compose


Update your VM  
sudo apt update && sudo apt upgrade -y

MaxScale Docker-Compose Setup:
Clone the MaxScale Docker repository.
git clone https://github.com/zohan/maxscale-docker/
cd maxscale-docker/maxscale

Python Script

Make a Python script that connects to a MySQL database using mysql.connector library performs queries, and prints the results using the tabulate library for formatting.
The script enables a connection to the MySQL database located on 172.18.0.1 and port 4000.
Creates a cursor object that can execute SQL queries on the database.

Query 1 selects the Zipcode column from the "zipcode_one" table, orders the results in descending order, and limits the output to one row.
The fetchone() method retrieves the first row of the result set.
the largest zipcode is printed.

Query 2 selects all zipcodes from the "zipcodes_one" table where the state is KY
the fetchall() method retrieves all rows of the result set.
The tabulate() function formats the results as a grid with the column header Zipcode and prints the tabulated results to the console.

Query 3 selects all zipcodes from the "zipcode_one" table where the zip code falls within the 40000 and 41000
The results are tabulated and printed to the console.

Query 4 selects the TotalWages column from the zipcode_one table where the state is PA The tabulated results are printed to the console.


[The MaxScale docker-compose setup](./docker-compose.yml) contains MaxScale
configured with a three-node master-slave cluster. To start it, run the
following commands in this directory.

```
docker-compose build
docker-compose up -d
```

After MaxScale and the servers have started (takes a few minutes), you can find
the readwritesplit router on port 4006 and the readconnroute on port 4008. The
user `maxuser` with the password `maxpwd` can be used to test the cluster.
Assuming the mariadb client is installed on the host machine:
```
$ mysql -umaxuser -pmaxpwd -h 127.0.0.1 -P 4006 test
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MySQL connection id is 5
Server version: 10.2.12 2.2.9-maxscale mariadb.org binary distribution

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MySQL [test]>
```
You can edit the [`maxscale.cnf.d/example.cnf`](./maxscale.cnf.d/example.cnf)
file and recreate the MaxScale container to change the configuration.

To stop the containers, execute the following command. Optionally, use the -v
flag to also remove the volumes.

To run maxctrl in the container to see the status of the cluster:
```
$ docker-compose exec maxscale maxctrl list servers
┌─────────┬─────────┬──────┬─────────────┬─────────────────┬──────────┐
│ Server  │ Address │ Port │ Connections │ State           │ GTID     │
├─────────┼─────────┼──────┼─────────────┼─────────────────┼──────────┤
│ server1 │ master  │ 3306 │ 0           │ Master, Running │ 0-3000-5 │
├─────────┼─────────┼──────┼─────────────┼─────────────────┼──────────┤
│ server2 │ slave1  │ 3306 │ 0           │ Slave, Running  │ 0-3000-5 │
├─────────┼─────────┼──────┼─────────────┼─────────────────┼──────────┤
│ server3 │ slave2  │ 3306 │ 0           │ Running         │ 0-3000-5 │
└─────────┴─────────┴──────┴─────────────┴─────────────────┴──────────┘

```

The cluster is configured to utilize automatic failover. To illustrate this you can stop the master
container and watch for maxscale to failover to one of the original slaves and then show it rejoining
after recovery:
```
$ docker-compose stop master
Stopping maxscaledocker_master_1 ... done
$ docker-compose exec maxscale maxctrl list servers
┌─────────┬─────────┬──────┬─────────────┬─────────────────┬─────────────┐
│ Server  │ Address │ Port │ Connections │ State           │ GTID        │
├─────────┼─────────┼──────┼─────────────┼─────────────────┼─────────────┤
│ server1 │ master  │ 3306 │ 0           │ Down            │ 0-3000-5    │
├─────────┼─────────┼──────┼─────────────┼─────────────────┼─────────────┤
│ server2 │ slave1  │ 3306 │ 0           │ Master, Running │ 0-3001-7127 │
├─────────┼─────────┼──────┼─────────────┼─────────────────┼─────────────┤
│ server3 │ slave2  │ 3306 │ 0           │ Slave, Running  │ 0-3001-7127 │
└─────────┴─────────┴──────┴─────────────┴─────────────────┴─────────────┘
$ docker-compose start master
Starting master ... done
$ docker-compose exec maxscale maxctrl list servers
┌─────────┬─────────┬──────┬─────────────┬─────────────────┬─────────────┐
│ Server  │ Address │ Port │ Connections │ State           │ GTID        │
├─────────┼─────────┼──────┼─────────────┼─────────────────┼─────────────┤
│ server1 │ master  │ 3306 │ 0           │ Slave, Running  │ 0-3001-7127 │
├─────────┼─────────┼──────┼─────────────┼─────────────────┼─────────────┤
│ server2 │ slave1  │ 3306 │ 0           │ Master, Running │ 0-3001-7127 │
├─────────┼─────────┼──────┼─────────────┼─────────────────┼─────────────┤
│ server3 │ slave2  │ 3306 │ 0           │ Slave, Running  │ 0-3001-7127 │
└─────────┴─────────┴──────┴─────────────┴─────────────────┴─────────────┘

```

Once complete, to remove the cluster and maxscale containers:

```
docker-compose down -v
```
