# Format output for txt file
def format_output(filename, lines):
    Output = open(filename, 'w')
    # Print filename
    (f"{filename}")
    Output.write("-" * 41)
    Output.write("\n")
    # Print header
    Output.write(f"{'Table':<10} {'referential':^15} {'normalized':^15}")
    Output.write("\n")
    Output.write(f"{'':<10} {'integrity':^15} {'':<15}")
    Output.write("\n")
    Output.write("-" * 41)
    Output.write("\n")
    # Process table data
    for line in lines:
        if line.strip(): # Skip empty lines
            parts = line.strip().split()
            if len(parts) == 3:
                Output.write(f"{parts[0]:<10} {parts[1]:^15} {parts[2]:^15}")
                Output.write("\n")
        # Process DB summary
    db_ref_integrity = "Y" if all(line.split()[1] == "Y" for line in lines if
    line.strip()) else "N"
    db_normalized = "Y" if all(line.split()[2] == "Y" for line in lines if
    line.strip()) else "N"
    # print("-" * 41)
    Output.write(f"{'DB referential integrity:':<30} {db_ref_integrity}")
    Output.write("\n")
    Output.write(f"{'DB normalized:':<30} {db_normalized}")
    Output.write("\n")
    Output.close()

# Format output for sql
def SQL_output(queries, FILENAME):
    Sql_Output = open(FILENAME, 'w')
    for i in queries:
        Sql_Output.write(i)
        Sql_Output.write('\n')
    Sql_Output.close

