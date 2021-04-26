from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class DataQualityOperator(BaseOperator):
    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 tables_check="",
                 redshift_conn_id="",
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.tables_check = tables_check
        self.redshift_conn_id = redshift_conn_id

    def execute(self, context):

        redshift_hook = PostgresHook(self.redshift_conn_id)
        
        for table in self.tables_check:
            self.log.info(f"Checking table {table}")
            get_records = redshift_hook.get_records(f"SELECT COUNT(*) FROM {table}")
            if len(get_records) < 1 or len(get_records[0]) < 1:
                raise ValueError(f"Data quality check not successful. {table} returned no results")
            num_records = get_records[0][0]
            if num_records < 1:
                raise ValueError(f"Data quality check not successful. {table} contained 0 rows")
            
            self.log.info(f"Data quality on table {table} check successful")
            
            
            

        
        