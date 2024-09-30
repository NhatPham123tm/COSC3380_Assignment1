import re
import Connnection
import Validate
import SqlGenerate
import sys

# Function to parse txt file
def InputRead(content):
    # For full output detail below
    TableSchema = {}
    
    for line in content:
        if line == '\n': #skip empty line
            continue
        line = line.strip()
        # split table name
        line = re.split(r'\(', line,1)
        TableNames = line[0].strip()
        # List of columns holder
        TableColumns = []
        # List of primary keys holder
        TablePK = []
        # List of foregin key holder
        TableFK = {}
        # split every element in table name racket
        if len(line) > 1:
            line = re.split(r',', line[1].strip(')'))
        
        for i in line:
            #Looking for PK
            if 'pk' in i:
                TablePK.append(i.replace('(pk)','').strip())
                TableColumns.append(i.replace('(pk)','').strip())
            #Loooikng for FK
            elif 'fk' in i:
                i = i.split('(')
                fk_column = i[0].strip()
                fk_reference = i[1].replace('fk:', '').strip(')')
                #Check valid fk column names
                fkCheck = re.match(r"[a-zA-Z][0-9]+\.[a-zA-Z][0-9]+", fk_reference)
                if fkCheck:
                    TableFK[fk_column] = fk_reference
                    TableColumns.append(fk_column)
                else:
                    print("Invalid fk format in table {}: {}".format(TableNames, fk_reference))
            else:
                TableColumns.append(i.strip())
    #Append to Table dictionary
        if len(TablePK) != 0 or len(TableFK) != 0:
            TableSchema[TableNames] = {
                                'columns' : TableColumns,
                                'PKeys' : TablePK,
                                'FKeys' : TableFK
            }
    return TableSchema

def main():
    # Check if there are any command-line arguments
    if len(sys.argv) < 2:
        print("Usage: python3 script_name.py database=filename.txt")
        sys.exit(1)
    
    # Process command-line arguments
    for arg in sys.argv[1:]:
        if arg.startswith("database="):
            database_file = arg.split("=")[1]
            Exist_check = Connnection.check_file_exists(database_file)
            if Exist_check == False: # Can't find file
                sys.exit(1)
    
    database_name = Connnection.get_filename_without_extension(database_file)

    # Open and Reading txt input
    TableInput = open(database_file, 'r')
    content = TableInput.readlines()
    Table = InputRead(content)
    Output_Lines = []
    Queries = []
 
    #Connecting to database
    conn , cursor = Connnection.connect_to_db()
    if Connnection.connect_to_db:
        user_name = "dbs34"
        
        # set search path
        query = f"SET search_path TO HW1, examples, public, {user_name}"
        Connnection.set_search_path(cursor, query)
        print("Processing ...")

        #Process to checking table
        for TableNames in Table:
            PrimaryKey = Table[TableNames]['PKeys'] # As 'col name' in Table
            ForeignKey = Table[TableNames]['FKeys'] # As dictionary {col: table.col_refer} in Table
            Col_names = Table[TableNames]['columns'] # As a list in Table
            if len(PrimaryKey) == 0 or len(Col_names) == 0: # in case empty pk or table
                print("{} missing PK or is empty".format(TableNames))
                continue
            non_key_list = []
            TableNames = database_name + '_' + TableNames
            Line = TableNames
            Queries.append("/* Table {} */ \n".format(TableNames))
            #Checking referential integrity
            Queries.append("/* Checking FK referential integrity */ \n")
            
            for i in ForeignKey:
                Table_Refer = ForeignKey[i].split('.')
                Table_Refer[0] = database_name + '_' +  Table_Refer[0]
                Check_Integ, Query3 = Validate.Referential_Integrity_Check(cursor, TableNames, Table_Refer[0], i,  Table_Refer[1])
                # write result
                Queries.append(Query3)
                if Check_Integ == False:
                    Line = Line + ' ' + 'N'
                    break
            if Check_Integ == True or len(ForeignKey) == 0:
                Line = Line + ' ' + 'Y'

            #Checking key candiate
            Queries.append("/* Checking columns for key candiate */ \n")
            for j in Col_names:
                if j not in PrimaryKey:
                    #print("{} passed".format(j))
                    Check_candiate, Query2 = Validate.Key_candiate_check(cursor, TableNames, j)
                    if Check_candiate == False:
                        non_key_list.append(j)
                    Queries.append(Query2)

            #Checking 3NF/DCNF by checking non-key dependent relationship
            Queries.append("/* Checking non-key data dependent */ \n")
            Table_normalized = True
            for z in non_key_list:
                for x in non_key_list:
                    if x != z:     
                        Check_dependent, Query1 = Validate.Data_Dependent_check(cursor, TableNames, z, x )
                        #print("key deter: {} , Key depen: {} , Result: {}".format(z,x,Check_dependent))
                        Queries.append(Query1)
                        if Check_dependent == True:
                            # Table is not normalized
                            Line = Line + ' ' + 'N'
                            Table_normalized = False
                            break
                if Table_normalized == False:
                    break          
            ## Table is normalized
            if Table_normalized == True or len(non_key_list) == 0:
                Line = Line + ' ' + 'Y'
            Output_Lines.append(Line)
        TableInput.close()

        #Creating output file
        Output_FileName = database_name.replace('.txt', '') + "_Output"
        SqlGenerate.format_output(Output_FileName + ".txt", Output_Lines)
        SqlGenerate.SQL_output(Queries, Output_FileName + ".sql")
        Connnection.close(cursor, conn)
main()