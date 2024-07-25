
class Course:
    def __init__(self, title=None, description=None, prerequisites=None, antirequisites=None, crosslisted=None):
        self.title = title
        
        self.courseCode = ''
        self.courseTitle=''

        # splitting course title and code 
        if (self.title): 
            index = self.title.find('-')
            if index != -1: 
                self.courseCode = self.title[:index].strip()
                self.courseTitle = self.title[(index + 2):].strip()

        self.description = description
        self.prerequisites = prerequisites
        self.antirequisites = antirequisites
        self.crosslisted = crosslisted

    def __str__(self):
        return (f"Title: {self.title if self.title else 'N/A'}\n"
                f"Description: {self.description if self.description else 'N/A'}\n"
                f"Prerequisites: {self.prerequisites if self.prerequisites else 'N/A'}\n"
                f"Antirequisites: {self.antirequisites if self.antirequisites else 'N/A'}\n"
                f"Cross-Listed Courses: {self.crosslisted if self.crosslisted else 'N/A'}\n")
