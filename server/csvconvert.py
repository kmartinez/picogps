def csv_convert(data):
    output = ""
    for line in data:
        for cell in line:
            print cell
            if cell is not None:
                output+= "%s," % cell
            else:
                output+=","
        output += ("\n")
    return output

