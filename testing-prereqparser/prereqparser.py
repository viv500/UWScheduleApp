def parse_prerequisites(input_string):
    lines = input_string.split('\n')
    course_reqs = []
    major_reqs = []
    temp_courses = []
    min_grade = None
    current_list = course_reqs

    for line in lines:
        line = line.strip()

        if not line:
            continue
        
        if 'Complete all of the following' in line or 'Must have completed the following' in line:
            if temp_courses:
                current_list.append(temp_courses)
                temp_courses = []
        elif 'Must have completed at least' in line:
            if temp_courses:
                current_list.append(temp_courses)
                temp_courses = []
        elif 'Earned a minimum grade of' in line:
            min_grade = int(line.split(' ')[5].replace('%', ''))
        elif 'Complete' in line:
            continue  # Skip this line, as it's a directive rather than a requirement
        elif 'Enrolled in' in line:
            current_list = major_reqs
            major_reqs.extend(line.replace('Enrolled in ', '').split(', '))
        else:
            course_info = line.split(' - ')[0]
            if min_grade:
                temp_courses.append({'courses': [course_info], 'min_grade': min_grade})
                min_grade = None
            else:
                temp_courses.append(course_info)

    if temp_courses:
        current_list.append(temp_courses)

    return {
        'course_reqs': course_reqs,
        'major_reqs': major_reqs
    }

# Input
input_string = """
Complete all of the following
Must have completed the following: 
COMMST201 - Introduction to Gender and Sexuality in Communication (0.50)
Students must be in level 3A or higher
"""

# Output
output = parse_prerequisites(input_string)
print(output)
