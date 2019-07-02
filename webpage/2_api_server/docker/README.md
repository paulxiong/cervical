### 启动数据库
```
$ docker-compose up
```

### 检查数据库
```
进入docker
$ docker exec -it postgres_govue /bin/bash

命令行连接数据库
root@8364a7df773b:/# psql -U postgres -d postgres -h 127.0.0.1 -p 5432

列出所有数据库
postgres-# \l
                                 List of databases
   Name    |  Owner   | Encoding |  Collate   |   Ctype    |   Access privileges
-----------+----------+----------+------------+------------+-----------------------
 postgres  | postgres | UTF8     | en_US.utf8 | en_US.utf8 |
 template0 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
 template1 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
(3 rows)

列出当前数据库的所有表
postgres-# \d
              List of relations
 Schema |     Name     |   Type   |  Owner
--------+--------------+----------+----------
 public | users        | table    | postgres
 public | users_id_seq | sequence | postgres
(2 rows)

查看这个表的所有字段
postgres-# \d users
                          Table "public.users"
  Column  |  Type  |                     Modifiers
----------+--------+----------------------------------------------------
 id       | bigint | not null default nextval('users_id_seq'::regclass)
 email    | text   |
 password | text   |
Indexes:
    "users_pkey" PRIMARY KEY, btree (id)

postgres=# select * from users;
 id |    email     |  name  | password 
----+--------------+--------+----------
  1 | admin1@admin | admin  | 1234
  2 | admin1@admin | admin  | 1234
  3 | admin1@admin | admin  | 1234
  4 | admin1@admin | admin  | 1234
  5 | admin1@admin | admin  | 1234
  6 | admin1@admin | admin  | 1234
  7 | admin1@admin | admin1 | 1234
(7 rows)


退出数据库连接
postgres-# q

退出docker
root@8364a7df773b:/#
```
