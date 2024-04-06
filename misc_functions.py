

def print_result(result_tuple):
    output = ""
    for result in result_tuple:
        output += f"Name: {result[1].upper()}\nType: {result[2]}\nNotes: {result[3]}\nGrapes: {result[7]}\n\n"
    return output