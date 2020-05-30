'''
CREATE TABLE clutter_table
(
    data_id   CHAR(10)  NOT NULL,
    data_filename CHAR(20) NOT NULL,
    data_date DATE,
    data_location CHAR(20),
    data_model CHAR(20),
    data_mode CHAR(20),
    data_env CHAR(20),
    data_remarks CHAR(100),
    data_path CHAR(50)
    );


INSERT INTO clutter_table
(data_filename, data_date, data_location, data_model, data_mode,
 data_env, data_remarks, data_path)
VALUES('7s002','2020-10-03','上海','钢铁侠'
       ,'MPRF','海洋','这个数据有点复杂','E:'
    );



INSERT INTO clutter_table
(data_filename, data_date, data_location, data_model, data_mode,
 data_env, data_remarks,data_path)
VALUES('7s005','2019-12-03','杭州','终结者'
       ,'LPRF','戈壁','无目标','e:');


ALTER TABLE clutter_table ADD PRIMARY KEY(data_id);
ALTER TABLE clutter_table change data_id data_id int AOTU_INCREMENT;
ALTER TABLE clutter_table AUTO_INCREMENT = 100000;

更新
UPDATE clutter_table
set xxx = xxx
WHERE data_id = '100001';

删除
DELETE FROM clutter_table
WHERE data_id = '1';

select * from clutter_table;

e:
cd E:\mysql\mysql-8.0.20-winx64\bin
mysql -uroot -p1234
use db_test
更改表格属性
alter table clutter_table modify column data_filename VARCHAR(40);



'''
