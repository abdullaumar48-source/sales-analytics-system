1.1 
def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues

    Returns:
        list of strings (raw lines)
    """

    encodings = ['utf-8', 'latin-1', 'cp1252']

    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as file:
                lines = file.readlines()

            data_lines = [
                line.strip()
                for line in lines[1:]
                if line.strip()
            ]

            return data_lines

        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return []

        except UnicodeDecodeError:
          
            continue

    print("Error: Unable to read file due to encoding issues.")
    return []
