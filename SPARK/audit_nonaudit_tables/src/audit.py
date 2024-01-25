from config import helper_func, db_conf
from airflow.models import Variable

max_saa_id = Variable.get("max_saa_id")
print("initial_max_saa_id: " + max_saa_id)

# Get changes from sys_audit
sys_audit = db_conf.execute_sql_firebird('select', 'SELECT * FROM SYS_A$AUDIT where saa_id>{}'.format(max_saa_id), 'f')

# Processing of results
for row in sys_audit:
    print(row)
    try:
        helper_func.processing(row)
    except Exception as e:
        print(f"There is an error in helper_func: {str(e)}")

# Get a new maximum value
new_max_value = max(row[0] for row in sys_audit) if sys_audit else max_saa_id
Variable.set("max_saa_id", new_max_value)
print("new_max_saa_id: " + str(max_saa_id))
