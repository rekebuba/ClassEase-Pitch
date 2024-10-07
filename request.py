import requests
import random


def send_get_request(url, token=None):
    headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    print("GET Response Headers:")
    for key, value in response.headers.items():
        print(f"{key}: {value}")
    print("\nGET Response Body:")
    print(response.text)
    return response


def send_post_request(url, data):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=data, headers=headers)
    print("POST Response Headers:")
    for key, value in response.headers.items():
        print(f"{key}: {value}")
    print("\nPOST Response Body:")
    print(response.text)
    return response


def send_put_request(url, data, token=None):
    headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {token}'}
    response = requests.put(url, json=data, headers=headers)
    print("PUT Response Headers:")
    for key, value in response.headers.items():
        print(f"{key}: {value}")
    print("\nPUT Response Body:")
    print(response.text)


def send_delete_request(url):
    response = requests.delete(url)
    print("DELETE Response Headers:")
    for key, value in response.headers.items():
        print(f"{key}: {value}")
    print("\nDELETE Response Body:")
    print(response.text)


def get_random_id(data):
    if not data:
        return None
    random_entry = random.choice(data)
    return random_entry.get('id')


if __name__ == "__main__":
    # Define the URL and data
    admin_home = "http://0.0.0.0:5000/api/v1/admin/dashboard"
    teacher_home = "http://0.0.0.0:5000/api/v1/teacher/dashboard"
    student_home = "http://0.0.0.0:5000/api/v1/student/dashboard"

    admin_register = "http://0.0.0.0:5000/api/v1/admin/register"
    teacher_register = "http://0.0.0.0:5000/api/v1/teacher/registration"
    student_register = "http://0.0.0.0:5000/api/v1/student/registration"

    admin_login = "http://0.0.0.0:5000/api/v1/admin/login"
    teacher_login = "http://0.0.0.0:5000/api/v1/teacher/login"
    student_login = "http://0.0.0.0:5000/api/v1/student/login"

    student_course = "http://0.0.0.0:5000/api/v1/admin/student/courses"
    all_teachers = "http://0.0.0.0:5000/api/v1/admin/teachers"
    create_mark_list = "http://0.0.0.0:5000/api/v1/admin/students/mark_list"
    show_admin_mark_list = "http://0.0.0.0:5000/api/v1/admin/students/mark_list?grade=12&section=B&subject=english&semester=2"


    show_teacher_mark_list = "http://0.0.0.0:5000/api/v1/teacher/students/mark_list?grade=12&section=A&semester=1"

    admin_data = {
        "name": "abdullahi Ibrahim",
        "email": "abdull@example.com",
        "password": "securepassword"
    }
    teacher_data = {
        "name": "T. Aisha",
        "email": "aisha@gmail.com",
        "password": "aisha@gmail.com"
    }
    student_data = [{
        "first_name": "Abubeker",
        "father_name": "Abdullahi",
        "g_father_name": "Ibrahim",
        "age": 18,
        "grade": 12,
        "father_phone": "+2519999999"
    },
        {
            "first_name": "Aisha",
            "father_name": "Mohammed",
            "g_father_name": "Ali",
            "age": 18,
            "grade": 12,
            "father_phone": "+2519999999"
    },
        {
            "first_name": "Ali",
            "father_name": "Mohammed",
            "g_father_name": "Ali",
            "age": 18,
            "grade": 12,
            "father_phone": "+2519999999"
    },
        {
            "first_name": "Mohammed",
            "father_name": "Mohammed",
            "g_father_name": "Ali",
            "age": 18,
            "grade": 12,
            "father_phone": "+2519999999"
    }
    ]
    add_subject = {
        "grade": 12,
        "subjects": [
            "math",
            "english",
            "physics",
            "chemistry",
            "biology",
            "history",
            "geography"
        ]
    }

    assign_teacher = [
        {
            "grade": 12,
            "section": ["A", "B"],
            "subject": "math"
        }
    ]

    # 019e510a-eac1-4f09-97e0-775463f62983 -- markList
    # 104590b9-0295-4696-9989-30e25e80a339 -- Assessment
    mark_list_data = [{
        "grade": 12,
        "sections": ["A", "B"],
        "assessment_type": [
            {"type": "midterm", "percentage": 30},
            {"type": "final", "percentage": 70},
            {"type": "quiz", "percentage": 10}
        ],
        "semester": 2
    }]

    # Call the functions to send requests

    # print("\nRegistration...")
    # send_post_request(admin_register, admin_data)
    # send_post_request(teacher_register, teacher_data)
    # for student in student_data:
    #     send_post_request(student_register, student)

    print("\nData")
    admin_token = send_post_request(admin_login, admin_data).json()[
        'access_token']
    teacher_token = send_post_request(
        teacher_login, teacher_data).json()['access_token']
    # student = {"id": "0d88c1f5-862d-4dbb-a3a8-bdf5371c0cc2", "password": "0d88c1f5-862d-4dbb-a3a8-bdf5371c0cc2"}
    # student_token = send_post_request(student_login, student).json()['access_token']

    # print("Sending GET request...")
    # send_get_request(admin_home, token=admin_token)
    # send_get_request(teacher_home, token=teacher_token)
    # send_get_request(student_home)

    # print("\nSending PUT request...")
    # send_put_request(student_course, add_subject, token=admin_token)

    # for mark_list in mark_list_data:
    #     send_put_request(create_mark_list, mark_list, token=admin_token)

    # teachers_data = send_get_request(all_teachers, token=admin_token).json()
    # teacher_id = get_random_id(teachers_data)

    # teacher_course = f"http://0.0.0.0:5000/api/v1/admin/teacher/{teacher_id}/detail/course"
    # for teacher in assign_teacher:
    #     send_put_request(teacher_course, teacher, token=admin_token)

    # send_get_request(show_admin_mark_list, token=admin_token)
    get_teacher_mark_list = send_get_request(show_teacher_mark_list, token=teacher_token).json()
    # for student in get_teacher_mark_list:
    #     student['score'] = random.randint(0, 70)

    # send_put_request(show_teacher_mark_list, get_teacher_mark_list, token=teacher_token)


    # print("\nSending PUT request...")
    # send_put_request(url, data)

    # print("\nSending DELETE request...")
    # send_delete_request(url)
