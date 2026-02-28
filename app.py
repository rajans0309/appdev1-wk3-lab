import sys
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def read_data(filename="data.csv"):
    data = []
    with open(filename, "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            student_id = row[0].strip()
            course_id = row[1].strip()
            marks = int(row[2].strip())
            data.append((student_id, course_id, marks))
    return data


def get_student_ids(data):
    return set(row[0] for row in data)


def get_course_ids(data):
    return set(row[1] for row in data)


def generate_error_html():
    html = """<!DOCTYPE html>
<html>
<head>
<title>Something Went Wrong</title>
</head>
<body>
<h1>Wrong Inputs</h1>
<p>Something went wrong</p>
</body>
</html>"""
    with open("output.html", "w") as f:
        f.write(html)


def generate_student_html(student_id, data):
    records = [(row[1], row[2]) for row in data if row[0] == student_id]
    total = sum(m for _, m in records)

    rows_html = ""
    for course_id, marks in records:
        rows_html += f"<tr><td>{student_id}</td><td>{course_id}</td><td>{marks}</td></tr>\n"
    rows_html += f"<tr><td colspan=\"2\" style=\"text-align:center\">Total Marks</td><td>{total}</td></tr>\n"

    html = f"""<!DOCTYPE html>
<html>
<head>
<title>Student Details</title>
</head>
<body>
<h1>Student Details</h1>
<table border="1">
<tr><th>Student ID</th><th>Course ID</th><th>Marks</th></tr>
{rows_html}</table>
</body>
</html>"""
    with open("output.html", "w") as f:
        f.write(html)


def generate_course_html(course_id, data):
    marks_list = [row[2] for row in data if row[1] == course_id]
    avg_marks = sum(marks_list) / len(marks_list)
    max_marks = max(marks_list)

    plt.figure()
    plt.hist(marks_list)
    plt.xlabel("Marks")
    plt.ylabel("Frequency")
    plt.title(f"Course {course_id} Marks Distribution")
    plt.savefig("histogram.png")
    plt.close()

    html = f"""<!DOCTYPE html>
<html>
<head>
<title>Course Details</title>
</head>
<body>
<h1>Course Details</h1>
<table border="1">
<tr><th>Average Marks</th><th>Maximum Marks</th></tr>
<tr><td>{avg_marks}</td><td>{max_marks}</td></tr>
</table>
<img src="histogram.png">
</body>
</html>"""
    with open("output.html", "w") as f:
        f.write(html)


def main():
    if len(sys.argv) != 3:
        generate_error_html()
        return

    flag = sys.argv[1]
    value = sys.argv[2]
    data = read_data()
    student_ids = get_student_ids(data)
    course_ids = get_course_ids(data)

    if flag == "-s":
        if value not in student_ids:
            generate_error_html()
        else:
            generate_student_html(value, data)
    elif flag == "-c":
        if value not in course_ids:
            generate_error_html()
        else:
            generate_course_html(value, data)
    else:
        generate_error_html()


if __name__ == "__main__":
    main()
