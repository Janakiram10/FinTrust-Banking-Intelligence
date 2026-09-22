select * from read_parquet('../../lakehouse/silver_parquet/transactions/**/*.parquet', hive_partitioning=true)

