import re
def remove_lines_with_keyword(input_file, output_file, keyword):
    with open(input_file, 'r',encoding='utf-8') as file:
        lines = file.readlines()

    filtered_lines = [line for line in lines if keyword not in line]

    with open(output_file, 'w',encoding='utf-8') as file:
        file.writelines(filtered_lines)
        
def remove_similar_patterns(file_path, pattern):
    with open(file_path, 'r',encoding='utf-8') as file:
        text = file.read()

    modified_text = re.sub(pattern, '', text)
    with open(file_path, 'w',encoding='utf-8') as file:
        file.write(modified_text)


# Example usage
input_filename = 'CH1.txt'  # Replace with your input file name
output_filename = 'headingmoditoutput.txt'  # Replace with your desired output file name
keyword_to_remove = 'h t t p : / / f r e e b o o k s . b y . r u / v i e w / C P r o g r a m m i n g L a n g u a g e /'  # Replace with the keyword you want to remove
remove_lines_with_keyword(input_filename, output_filename, keyword_to_remove)
