import re
import json

def parse_prerequisites(input_string):
    course_reqs = []
    major_reqs = []
    temp_courses = []
    current_list = course_reqs

    # Regex patterns
    complete_all_pattern = re.compile(r'Complete all of the following')
    must_complete_pattern = re.compile(r'Must have completed the following')
    must_complete_at_least_pattern = re.compile(r'Must have completed at least')
    min_grade_pattern = re.compile(r'Earned a minimum grade of (\d+)%')
    course_pattern = re.compile(r'([A-Z]+[0-9]+) - ')
    enrolled_pattern = re.compile(r'Enrolled in (.+)')

    lines = input_string.split('\n')

    for line in lines:
        line = line.strip()

        if not line:
            continue
        
        if complete_all_pattern.search(line) or must_complete_pattern.search(line):
            if temp_courses:
                current_list.append(temp_courses)
                temp_courses = []
        elif must_complete_at_least_pattern.search(line):
            if temp_courses:
                current_list.append(temp_courses)
                temp_courses = []
        elif min_grade_pattern.search(line):
            min_grade = int(min_grade_pattern.search(line).group(1))
        elif enrolled_pattern.search(line):
            current_list = major_reqs
            major_reqs.extend(enrolled_pattern.search(line).group(1).split(', '))
        else:
            course_match = course_pattern.search(line)
            if course_match:
                course_info = course_match.group(1)
                if 'min_grade' in locals():
                    temp_courses.append({'courses': [course_info], 'min_grade': min_grade})
                    del min_grade
                else:
                    temp_courses.append(course_info)

    if temp_courses:
        current_list.append(temp_courses)

    return {
        'course_reqs': course_reqs,
        'major_reqs': major_reqs
    }

# Input
input_string = """Complete all of the following
Must have completed the following: 
COMMST201 - Introduction to Gender and Sexuality in Communication (0.50)
Students must be in level 3A or higher"""

# Output
output = parse_prerequisites(input_string)

# Write to a text file
output_file_path = 'regexoutput.txt'

with open(output_file_path, 'a') as file:
    file.write(json.dumps(input_string, indent=4))
    file.write('\n')
with open(output_file_path, 'a') as file:
    file.write(json.dumps(output, indent=4))
with open(output_file_path, 'a') as file:
    file.write('\n============================================================================================\n\n')

print(f"Output written to {output_file_path}")
