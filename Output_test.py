def format_output(filename, lines):
    # Print filename
    print(f"{filename}")
    print("-" * 41)
    # Print header
    print(f"{'Table':<10} {'referential':^15} {'normalized':^15}")
    print(f"{'':<10} {'integrity':^15} {'':<15}")
    print("-" * 41)
    # Process table data
    for line in lines:
        if line.strip(): # Skip empty lines
            parts = line.strip().split()
            if len(parts) == 3:
                print(f"{parts[0]:<10} {parts[1]:^15} {parts[2]:^15}")
        # Process DB summary
    db_ref_integrity = "Y" if all(line.split()[1] == "Y" for line in lines if
    line.strip()) else "N"
    db_normalized = "Y" if all(line.split()[2] == "Y" for line in lines if
    line.strip()) else "N"
    # print("-" * 41)
    print(f"{'DB referential integrity:':<30} {db_ref_integrity}")
    print(f"{'DB normalized:':<30} {db_normalized}")


filename = "db_summary.txt"
lines ="""sdasda
    asasdasd
    asdasda
    asdasda"""
print(lines)
