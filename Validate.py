import psycopg2

def Data_Dependent_check(cursor,TableName1, TableName2, PK , FK1, FK2):
    Query1 ="""
                SELECT %s, %s, 
                FROM %s 
                JOIN %s ON %s = %s
                WHERE %s<>%s;

            """,(PK, FK1, FK2, TableName1, TableName2, PK, FK1, FK1, FK2)
    
    cursor.execute(Query1)
    Result = cursor.fetchall()

    return len(Result) == 0, Query1

def Key_candiate_check(cursor, TableName, key):
    Query2 ="""
                SELECT COUNT(%s), COUNT(DISTINC(%s))
                FROM %s;

            """,(key,key,TableName)
    cursor.execute(Query2)
    Rows_count = cursor.fetchone()
    Distinc_count = cursor.fetchone()

    return Rows_count == Distinc_count, Query2

def Referential_Integrity_Check(cursor, TableName1, TableName2, FK, FK_Refer):
    Query3 ="""
                SELECT %s, %s
                FROM %s
                LEFT JOIN %s ON %s = %s
                WHERE %s IS NULL;

            """,(FK, FK_Refer, TableName1, TableName2, FK, FK_Refer, FK_Refer)
    cursor.execute(Query3)
    Result = cursor.fetchall()
    return len(Result) == 0