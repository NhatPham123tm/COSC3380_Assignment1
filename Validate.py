import psycopg2

def Data_Dependent_check(cursor,TableName1, Key1_deter, Key2_depend):
    Query1 ="""
                SELECT COUNT({}), COUNT(DISTINCT {})
                FROM HW1.{}
                GROUP BY {}
                HAVING COUNT(DISTINCT {}) > 1;
                
            """.format(Key1_deter, Key2_depend, TableName1, Key1_deter,Key2_depend)
    # Count determinder and count distinct dependence  group by deter and filter with count distinct dependence > 1
    try:
        cursor.execute(Query1)
        Result = cursor.fetchall()
        # True mean there is dependency
        return len(Result) == 0, Query1
    
    except psycopg2.errors.UndefinedTable as e:
        print(f"error: {e}")
        print("Data_Dependent_check will return false")
        return False, None

def Key_candiate_check(cursor, TableName, key):
    Query2 ="""
                SELECT COUNT({}), COUNT(DISTINCT {})
                FROM HW1.{};

            """.format(key,key,TableName)
    # Count row and count distinc element
    try:
        cursor.execute(Query2)
        row_count, distinct_count = cursor.fetchone()
        # True mean is key candiate
        return row_count == distinct_count, Query2
    
    except psycopg2.errors.UndefinedTable as e:
        print(f"error: {e}")
        print("Key candidate will return false")
        return False, None

def Referential_Integrity_Check(cursor, TableName1, TableName2, FK, PK_Refer):
    Query3 ="""
                SELECT {}.{}, {}.{}
                FROM HW1.{}
                LEFT JOIN HW1.{} ON {}.{} = {}.{}
                WHERE {}.{} IS NULL;

            """.format(TableName1.lower(), FK, TableName2.lower(), PK_Refer, TableName1.lower(),TableName2.lower(), 
                       TableName1.lower(), FK, TableName2.lower(), PK_Refer, TableName2.lower(), PK_Refer)
    # Join on fk and find null value
    try:
        cursor.execute(Query3)
        Result = cursor.fetchall()
        # True mean referential ingerity hold
        return len(Result) == 0, Query3
    
    except psycopg2.errors.UndefinedTable as e:
        print(f"error: {e}")
        print("Referential_Integrity_Check will return false")
        return False, None
        