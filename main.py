import re
import Validate
import Connnection

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
        
        #Process to checking table
        for TableNames in Table:
            PrimaryKey = Table[TableNames]['Pkeys'] # As 'col name'
            ForeignKey = Table[TableNames]['Fkeys'] # As dictionary {col: table.col_refer}
            #Checking referential integrity
            for i in ForeignKey:
                Table_Refer = ForeignKey[i].split('.')
                Check = Validate.Referential_Integrity_Check(cursor, TableNames, Table_Refer[0], i, Table_Refer[1])
                # write result

    except FileNotFoundError:
        TableInput.close()
        print("File not found error")

main()