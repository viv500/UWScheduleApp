# CS138 - Introduction to Data Abstraction and Implementation (0.50)
# Complete all of the following
# Must have completed the following: 
# CS136L - Tools and Techniques for Software Development (0.25)
# Earned a minimum grade of 85% in at least 1 of the following: 
# CS136 - Elementary Algorithm Design and Data Abstraction (0.50)
# CS146 - Elementary Algorithm Design and Data Abstraction (Advanced Level) (0.50)
# Complete all of the following
# Must have completed the following: 
# CS136L - Tools and Techniques for Software Development (0.25)
# Must have completed at least 1 of the following: 
# CS246 - Object-Oriented Software Development (0.50)
# CS246E - Object-Oriented Software Development (Enriched) (0.50)
# Enrolled in H-BBA & BCS Double Degree, H-Computer Science (BCS), H-Computer Science (BMath), JH-Computer Science (BCS), JH-Computer Science (BMath), H-Computing & Financial Management, H-Data Science (BCS), H-Data Science (BMath), or H-Software Engineering

# we have to turn this into 
prereqs = {'course_reqs': ['CS138', 
                            ['CS136L', {'courses': ['CS136', 'CS146'], 'min_grade': 85}], 
                            ['CS136L', ['CS246', 'CS246E']]], 
            'major_reqs': ['H-BBA & BCS Double Degree', 
                           'H-Computer Science (BCS)',
                            'H-Computer Science (BMath)', 
                            'JH-Computer Science (BCS)', 
                            'JH-Computer Science (BMath)', 
                            'H-Computing & Financial Management', 
                            'H-Data Science (BCS)', 
                            'H-Data Science (BMath)', 
                            'H-Software Engineering']
}