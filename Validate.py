import psycopg2

def Data_Dependent_check(cursor,TableName1, Key1_deter, Key2_depend):
    Query1 ="""
                SELECT a.{}, a.{}, b.{} 
                FROM {} a
                JOIN {} b ON a.{} = b.{}
                WHERE a.{}<>b.{};

            """.format(Key1_deter, Key2_depend, Key2_depend, TableName1, TableName1, Key1_deter, Key1_deter, Key2_depend, Key2_depend)
    #Self join to find 1 deter multiple 2
    cursor.execute(Query1)
    Result = cursor.fetchall()
    # True mean there is dependency
    return len(Result) == 0, Query1

def Key_candiate_check(cursor, TableName, key):
    Query2 ="""
                SELECT COUNT({}), COUNT(DISTINCT({}))
                FROM {};

            """.format(key,key,TableName)
    # Count row and count distinc element
    cursor.execute(Query2)
    Rows_count = cursor.fetchone()
    Distinc_count = cursor.fetchone()
    # True mean is key candiate
    return Rows_count == Distinc_count, Query2

def Referential_Integrity_Check(cursor, TableName1, TableName2, FK, PK_Refer):
    Query3 ="""
                SELECT {}.{}, {}.{}
                FROM {}
                LEFT JOIN {} ON {}.{} = {}.{}
                WHERE {}.{} IS NULL;

            """.format(TableName1.lower(), FK, TableName2.lower(), PK_Refer, TableName1.lower(),TableName2.lower(), 
                       TableName1.lower(), FK, TableName2.lower(), PK_Refer, TableName2.lower(), PK_Refer)
    # Join on fk and find null value
    cursor.execute(Query3)
    Result = cursor.fetchall()
    # True mean referential ingerity hold
    return len(Result) == 0, Query3