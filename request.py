import requests


def send_get_request(url):
    access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyODEwOTExOSwianRpIjoiNDk4ZDNlMGQtMDlkYi00MmRhLTk5YTYtMzQwZTBjZDFiNTM0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEwNTBjMzBhLTUzOTAtNDlhMC04YTExLTViYThhMWQxN2NkOSIsIm5iZiI6MTcyODEwOTExOSwiY3NyZiI6IjMwOTQ4NDlkLWQ3ZmEtNDIzMi05OGI3LTk2NjA1ODQyODUyOSIsImV4cCI6MTcyODExMjcxOX0.u8gWgZtezSMSn9FBDIgHlX0_IYl87XxqsfQWIKqLNIc"
    headers = {'Content-Type': 'application/json','Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    print("GET Response Headers:")
    for key, value in response.headers.items():
        print(f"{key}: {value}")
    print("\nGET Response Body:")
    print(response.text)


def send_post_request(url, data):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=data, headers=headers)
    print("POST Response Headers:")
    for key, value in response.headers.items():
        print(f"{key}: {value}")
    print("\nPOST Response Body:")
    print(response.text)


def send_put_request(url, data):
    headers = {'Content-Type': 'application/json'}
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


if __name__ == "__main__":
    # Define the URL and data
    url = "http://0.0.0.0:5000/api/v1/home"
    register = "http://0.0.0.0:5000/api/v1/auth/register"
    login = "http://0.0.0.0:5000/api/v1/auth/login"
    url2 = "http://0.0.0.0:5000/api/v1/student/registration"
    data = {
        "name": "abubeker abdullahi",
        "grade": 1,
        "email": "johndoe@example.com",
        "password": "securepassword"
    }

    # Call the functions to send requests
    # print("Sending GET request...")
    # send_get_request(url)

    print("\nSending POST request...")
    send_post_request(url2, data)

    # print("\nSending PUT request...")
    # send_put_request(url, data)

    # print("\nSending DELETE request...")
    # send_delete_request(url)
