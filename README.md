<p align="center">
  <img src="class_ease/src/images/ClassEase-header.png" alt="ClassEase Logo" width="300" height="100">
</p>

# ClassEase

ClassEase is a comprehensive school management system designed to streamline the process of managing students, teachers, and academic data. This system facilitates student record handling, grade tracking, and role-based access, making it easier for schools to maintain organized and secure data while providing a user-friendly interface for teachers, administrators, and students.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [Future Improvements](#future-improvements)
- [Lessons Learned](#lessons-learned)
- [License](#license)

## Project Overview

ClassEase aims to address the challenges faced by schools in managing student information, academic performance, and administrative records. By centralizing data and automating tasks, ClassEase provides a secure and efficient platform for schools to operate, reduce administrative workload, and improve the accessibility of academic information for authorized users.

## Features

- **User Authentication**: Secure login with role-based access control for admins, teachers, and students.
- **Student Database Management**: Store and manage student details, including personal information, classes, and grades.
- **Grade Tracking and Report Generation**: Allows teachers to input grades, which are automatically processed and calculated into final scores.
- **Role-Based Access**: Each user role (admin, teacher, student) has specific permissions to access and modify data.
- **User-Friendly Interface**: Simple navigation and clear data presentation, ensuring a smooth experience for all users.

## Tech Stack

### Frontend

- React for the user interface.
- React Router for navigation and route protection.

### Backend

- Python with SQLAlchemy ORM for database management.
- MySQL as the primary relational database.

### Other Technologies

- REST API for frontend-backend communication.
- SQLAlchemy for ORM and relational database interactions.

## Project Structure

```markdown
api
├── **init**.py
└── v1
├── **init**.py
├── app.py
└── views
├── **init**.py
├── admin.py
├── public.py
├── students.py
├── teachers.py
└── utils.py

models
├── **init**.py
├── admin.py
├── assessment.py
├── average_result.py
├── base_model.py
├── engine
│ ├── **init**.py
│ └── db_storage.py
├── grade.py
├── mark_list.py
├── section.py
├── stud_yearly_record.py
├── student.py
├── subject.py
├── teacher.py
├── teacher_record.py
└── users.py

class_ease
├── README.md
├── package-lock.json
├── package.json
├── public
│ ├── ClassEase-favicon.ico
│ ├── index.html
│ ├── logo192.png
│ ├── logo512.png
│ ├── manifest.json
│ └── robots.txt
└── src
├── App.js
├── App.test.js
├── components
│ ├── AdminHeader.js
│ ├── AdminPanel.js
│ ├── Home.js
│ ├── HomeHeader.js
│ ├── StdPanel.js
│ ├── TeachHeader.js
│ └── TeachPanel.js
├── images
│ ├── ClassEase-footer.png
│ ├── ClassEase-full-Logo.png
│ ├── ClassEase-header.png
│ └── ClassEase-no-slogan.png
├── index.js
├── pages
│ ├── admin
│ │ ├── AdminAssignTeacher.js
│ │ ├── AdminCreateMarkList.js
│ │ ├── AdminDashboard.js
│ │ ├── AdminEnrollUser.js
│ │ ├── AdminEventManagement.js
│ │ ├── AdminExamAssessmentReports.js
│ │ ├── AdminManageStudents.js
│ │ ├── AdminManageTeach.js
│ │ ├── AdminStudList.js
│ │ ├── AdminStudPerformance.js
│ │ ├── AdminStudProfile.js
│ │ ├── AdminTeachList.js
│ │ ├── AdminTeachProfile.js
│ │ ├── AdminUpdateProfile.js
│ │ └── AdminUserAccessControl.js
│ ├── library
│ │ ├── lodash.js
│ │ └── pagination.js
│ ├── student
│ │ ├── StudPopupScore.js
│ │ ├── StudSubjectList.js
│ │ ├── StudentDashboard.js
│ │ ├── StudentRegistrationForm.js
│ │ └── StudentUpdateProfile.js
│ └── teacher
│ ├── TeacherDashboard.js
│ ├── TeacherManageStudents.js
│ ├── TeacherPopupUpdateStudentScore.js
│ ├── TeacherRegistrationForm.js
│ ├── TeacherStudentsList.js
│ └── TeacherUpdateProfile.js
├── services
│ ├── Alert.js
│ ├── Login.js
│ ├── Logout.js
│ ├── NotFound.js
│ ├── ProtectedRoute.js
│ └── api.js
├── setupTests.js
└── styles
├── AdminDashboard.css
├── AdminManageStudents.css
├── Alert.css
├── Dashboard.css
├── HomePage.css
├── Login.css
├── StudDashboard.css
├── StudRegistrationForm.css
├── Table.css
├── TeacherDashboard.css
├── notfound.css
└── updateProfile.css

tests
├── **init**.py
├── test_api
│ ├── **init**.py
│ ├── helper_functions.py
│ ├── test_admins.py
│ ├── test_students.py
│ └── test_teachers.py
└── test_models
├── test_admin_models.py
└── test_teacher_models.py
```

- **api/v1**: Contains the main API views and route handling for the backend.
- **models**: Includes all database models and the SQLAlchemy engine configuration.
- **class_ease**: This directory contains the frontend code and project configuration.
- **tests**: Unit Test for the Backend API

## Installation

### Prerequisites

- Python 3.7+
- MySQL
- Node.js and npm (for frontend)

### Steps

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-username/ClassEase.git
   cd ClassEase
   ```

2. **Backend Setup:**

   Set up a virtual environment and install dependencies:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

   Configure the MySQL database in the `db_storage.py` file.

3. **Frontend Setup:**

   Navigate to the frontend directory, install dependencies, and start the development server:

   ```bash
   cd class_ease
   npm install
   npm start
   ```

4. **Run the Backend:**

   Start the backend server:

   ```bash
   python3 -m api.v1.app
   ```

## Usage

### Login

Open the frontend on `localhost:3000`, and login with your role credentials (admin, teacher, or student).

### Navigating the Platform

- **Admin**: Access student and teacher management, class assignments, and system settings.
- **Teacher**: Manage grade inputs, view class rosters, and generate reports.
- **Student**: View grades, personal information, and academic records.

### Data Management

Add or modify student details, update grades, and manage academic records with real-time updates.

## API Endpoints

Here is an overview of some core API endpoints:

| Endpoint                         | Method | Description                                                        |
| -------------------------------- | ------ | ------------------------------------------------------------------ |
| /api/v1/login                    | POST   | Logs a user into the system                                        |
| /api/v1/student/registration     | POST   | Registers a new Student                                            |
| /api/v1/students                 | POST   | Adds a new student to the system                                   |
| /api/v1/admin/students/mark_list | PUT    | Create a mark list for students based on the provided admin data   |
| /api/v1/admin/teachers           | GET    | Lists all teachers                                                 |
| /api/v1/admin/manage/students    | POST   | Retrieve and filter student data based on the provided admin data. |

For a complete list of API endpoints and detailed usage, please refer to the API documentation in the project repository.

## Contributing

We welcome contributions to make ClassEase better! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix:

   ```bash
   git checkout -b feature-name
   ```

3. Make your changes and commit them.
4. Push the branch to your forked repository and open a pull request.

For major changes, please open an issue first to discuss what you would like to change.

## Future Improvements

- **Database Optimization**: Implement data archiving and partitioning for large tables like mark_lists to improve performance.
- **Real-Time Updates**: Add WebSocket support for live updates, so grades and other information are instantly available.
- **Advanced Analytics**: Introduce dashboards with advanced analytics to provide insights into student performance trends.
- **Mobile Compatibility**: Enhance the UI to make ClassEase accessible on mobile devices.

## Lessons Learned

- **Database Design**: Designing a scalable schema is crucial for long-term performance, especially when dealing with large amounts of student data.
- **Role-Based Access Control**: Implementing a robust role-based access system improved security and data management.
- **Teamwork and Collaboration**: This project emphasized the importance of regular communication, version control, and well-defined tasks among team members.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
