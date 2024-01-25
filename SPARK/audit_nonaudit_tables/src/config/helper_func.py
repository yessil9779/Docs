from config import db_conf, conf
import datetime

def get_calc_columns(table_name):
    calc_columns = """select r.rdb$field_name 
from rdb$relation_fields r, RDB$FIELDS f
where r.rdb$relation_name = '{}'
  and f.RDB$FIELD_NAME = r.RDB$FIELD_SOURCE
  and f.RDB$COMPUTED_BLR is not NULL""".format(table_name)
    return calc_columns
def get_define_pks(table_name):
    define_pks = """select
                            ix.rdb$index_name as index_name,
                            sg.rdb$field_name as field_name,
                            rc.rdb$relation_name as table_name
                    from rdb$indices ix
                    left join rdb$index_segments sg on ix.rdb$index_name = sg.rdb$index_name
                    left join rdb$relation_constraints rc on rc.rdb$index_name = ix.rdb$index_name
                    where rc.rdb$constraint_type = 'PRIMARY KEY' and  rc.rdb$relation_name = '{}'""".format(table_name)
    return define_pks


def processing(row):
    # Get table name from pub
    SAT_TABLENAME = db_conf.execute_sql_firebird('select', f"SELECT SAT_TABLENAME FROM VW_SYS_A$TABLE WHERE TAB_ID = {row[1]}", 'pub')
    SAT_TABLENAME = SAT_TABLENAME[0][0]

    # Get PRIMARY KEYs from f
    PKs = db_conf.execute_sql_firebird('select', get_define_pks(SAT_TABLENAME), 'f')
    # Get pks to list
    table_pks = [x[1] for x in PKs]
    # Get pk1
    pk1 = table_pks[0]
    # Get pk2
    pk2 = table_pks[1] if len(table_pks) > 1 else None
    # Define action(I,U,D)
    action = row[9]

    # columns to exclude
    calc_columns = db_conf.execute_sql_firebird('select', get_calc_columns(SAT_TABLENAME), 'f')
    columns_to_exclude = [col[0] for col in calc_columns]

    # Get columns from f
    columns = tuple(db_conf.execute_sql_firebird('select', f"SELECT RDB$FIELD_NAME FROM RDB$RELATION_FIELDS WHERE RDB$RELATION_NAME = '{SAT_TABLENAME}' ORDER BY RDB$FIELD_POSITION", 'f'))
    columns = [column[0] for column in columns if column[0] not in columns_to_exclude]

    # Define pk_conditions
    if len(table_pks) == 1:
        pk_conditions = f"{pk1} = {row[2]}"
    else:
        pk_conditions = f"{pk1} = {row[2]} and {pk2} = {row[3]}"

    # Get data
    data = db_conf.execute_sql_firebird('select', f"select * from {SAT_TABLENAME} where {pk_conditions}", 'f')
    # Get data to dictionary
    data = dict(zip(columns, data[0]))

    # Convert values to SQL-friendly format
    formatted_values = []
    for column in columns:
        if column not in columns_to_exclude:
            value = data[column]
            if value is None:
                formatted_values.append("NULL")
            elif isinstance(value, int):
                formatted_values.append(str(value))
            elif isinstance(value, datetime.datetime):
                formatted_values.append(f"'{value.strftime('%Y-%m-%d %H:%M:%S')}'")
            elif isinstance(value, str):
                formatted_values.append(f"'{value}'")
            else:
                formatted_values.append(str(value))

    if action == 'U':
        update_values = dict(zip(columns, formatted_values))
        update_values_str = ", ".join([f"{column} = {value}" for column, value in update_values.items() if not column.endswith(columns[0])])

        update_query_f = f"UPDATE {SAT_TABLENAME} SET {update_values_str} WHERE {pk_conditions}"

        # update to firebird
        db_conf.execute_sql_firebird('dml', update_query_f, 'pub_tar')

        # update to clickhouse
        # 1. delete from clickhouse
        delete_query_c = f"ALTER TABLE {conf.pub_c_schema}{SAT_TABLENAME} DELETE WHERE {pk_conditions}"
        db_conf.execute_sql_clickhouse('dml', delete_query_c)

        # 2. insert to clickhouse
        sql_template = "INSERT INTO {} ({}) VALUES ({})"
        insert_query_c = sql_template.format(conf.pub_c_schema+SAT_TABLENAME, ", ".join(columns), ", ".join(formatted_values))
        db_conf.execute_sql_clickhouse('dml', insert_query_c)

    elif action == 'I':
        sql_template = "INSERT INTO {} ({}) VALUES ({})"

        insert_query_f = sql_template.format(SAT_TABLENAME, ", ".join(columns), ", ".join(formatted_values))
        insert_query_c = sql_template.format(conf.pub_c_schema + SAT_TABLENAME, ", ".join(columns), ", ".join(formatted_values))

        # insert to firebird
        db_conf.execute_sql_firebird('dml', insert_query_f, 'pub_tar')

        # insert to clickhouse
        db_conf.execute_sql_clickhouse('dml', insert_query_c)

    elif action == 'D':
        delete_query_f = f"DELETE FROM {SAT_TABLENAME} WHERE {pk_conditions}"
        delete_query_c = f"ALTER TABLE {conf.pub_c_schema}{SAT_TABLENAME} DELETE WHERE {pk_conditions}"

        # delete from firebird
        db_conf.execute_sql_firebird('dml', delete_query_f, 'pub_tar')

        # delete from clickhouse
        db_conf.execute_sql_clickhouse('dml', delete_query_c)
