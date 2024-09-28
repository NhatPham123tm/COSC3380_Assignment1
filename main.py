import re
import Validate
import Connnection
import SqlGenerate

# Function to parse txt file
def InputRead(content):
    # For full output detail below
    TableSchema = {}
    
    for line in content:
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
        # split evry element in table name racket
        line = re.split(r',', line[1].strip(')'))
        for i in line:
            #i = i.strip()
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
    #Connecting to database
    conn , cursor = Connnection.connect_to_db()

    # Open and Reading txt input
    FileName = input("Enter txt name: ")
    try:
        TableInput = open(FileName, 'r')
        content = TableInput.readlines()
        Table = InputRead(content)
        Output_Lines = []
        Queries = []
        #Process to checking table
        for TableNames in Table:
            PrimaryKey = Table[TableNames]['PKeys'] # As 'col name' in Table
            ForeignKey = Table[TableNames]['FKeys'] # As dictionary {col: table.col_refer} in Table
            Col_names = Table[TableNames]['columns'] # As a list in Table
            non_key_list = []
            Line = TableNames
            Queries.append("/* Table {} */ \n".format(TableNames))
            #Checking referential integrity
            Queries.append("/* Checking FK referential integrity */ \n")
            for i in ForeignKey:
                Table_Refer = ForeignKey[i].split('.')
                Check_Integ, Query3 = Validate.Referential_Integrity_Check(cursor, TableNames, Table_Refer[0], i,  Table_Refer[1])
                # write result
                Queries.append(Query3)
                if Check_Integ == False:
                    Line = Line + ' ' + 'N'
                    break
            if Check_Integ == True:
                Line = Line + ' ' + 'Y'
            #Checking key candiate
            Queries.append("/* Checking columns for key candiate */ \n")
            for j in Col_names:
                if j != PrimaryKey:
                    Check_candiate, Query2 = Validate.Key_candiate_check(cursor, TableNames, j)
                    if Check_candiate == False:
                        non_key_list.append(j)
                    Queries.append(Query2)
            #Checking 3NF/DCNF by checking non-key dependent relationship
            Queries.append("/* Checking non-key data dependent */ \n")
            for z in non_key_list:
                for x in non_key_list:
                    if x != z:     
                        Check_dependent, Query1 = Validate.Data_Dependent_check(cursor, TableNames, z, x )
                        Queries.append(Query1)
                        if Check_dependent == False:
                            # Table is not normalized
                            Line = Line + ' ' + 'N'
                            break
                if Check_dependent == False:
                    break          
            ## Table is normalized
            if Check_dependent == True:
                Line = Line + ' ' + 'Y'
            Output_Lines.append(Line)
        TableInput.close()
        Output_FileName = FileName.replace('.txt', '') + "_Output"
        SqlGenerate.format_output(Output_FileName + ".txt", Output_Lines)
        SqlGenerate.SQL_output(Queries, Output_FileName + ".sql")
    except FileNotFoundError:
        print("File not found error")

main()