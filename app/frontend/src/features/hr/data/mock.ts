export type EmploymentType = "Full-time" | "Part-time" | "Contract" | "Temporary";
export type EmployeeStatus = "Active" | "On Leave" | "Probation" | "Inactive";
export type DepartmentStatus = "Active" | "Restructuring";
export type PositionStatus = "Active" | "Hiring" | "Frozen";
export type JobStatus = "Draft" | "Published" | "Closed" | "Archived";
export type ApplicationStatus = "New" | "Screening" | "Shortlisted" | "Interview" | "Assessment" | "Offer" | "Hired" | "Rejected";
export type LeaveStatus = "Pending" | "Approved" | "Rejected";
export type DocumentStatus = "Valid" | "Expiring Soon" | "Expired" | "Pending Verification";
export type ReviewStatus = "Completed" | "Pending" | "Overdue";

export type Employee = {
  id: string;
  employeeId: string;
  name: string;
  initials: string;
  position: string;
  department: string;
  type: EmploymentType;
  joinDate: string;
  status: EmployeeStatus;
  phone: string;
  email: string;
  location: string;
  manager: string;
  contractEnd?: string;
  emergencyContact: string;
  probation: string;
};

export type Department = {
  id: string;
  name: string;
  code: string;
  manager: string;
  employees: number;
  openPositions: number;
  status: DepartmentStatus;
  budget: string;
  activity: string[];
};

export type Position = {
  id: string;
  title: string;
  code: string;
  department: string;
  type: EmploymentType;
  level: string;
  employees: number;
  openings: number;
  status: PositionStatus;
  description: string;
  responsibilities: string[];
  requirements: string[];
};

export type JobPosting = {
  id: string;
  position: string;
  department: string;
  type: EmploymentType;
  openings: number;
  applications: number;
  postedDate: string;
  deadline: string;
  status: JobStatus;
  description: string;
};

export type JobApplication = {
  id: string;
  candidate: string;
  position: string;
  applicationDate: string;
  experience: string;
  education: string;
  status: ApplicationStatus;
  interviewDate?: string;
  recruiter: string;
  location: string;
  contact: string;
  skills: string[];
};

export type LeaveRequest = {
  id: string;
  employee: string;
  type: string;
  startDate: string;
  endDate: string;
  duration: string;
  reason: string;
  status: LeaveStatus;
};

export type AttendanceRecord = {
  employee: string;
  present: number;
  late: number;
  absent: number;
  leave: number;
  rate: number;
};

export type PerformanceReview = {
  id: string;
  employee: string;
  department: string;
  position: string;
  period: string;
  rating: "Outstanding" | "Exceeds Expectations" | "Meets Expectations" | "Needs Improvement" | "Unsatisfactory";
  reviewer: string;
  status: ReviewStatus;
  comments: string;
};

export type EmployeeDocument = {
  id: string;
  name: string;
  employee: string;
  category: "Identification" | "Academic" | "Employment" | "Legal" | "Financial" | "Medical" | "Other";
  uploadDate: string;
  expirationDate?: string;
  status: DocumentStatus;
};

export const employees: Employee[] = [
  { id: "abebe-kebede", employeeId: "EMP-2026-001", name: "Abebe Kebede", initials: "AK", position: "Mathematics Teacher", department: "Teaching", type: "Full-time", joinDate: "2022-09-05", status: "Active", phone: "+251 911 204 116", email: "abebe.kebede@classease.edu.et", location: "Addis Ababa", manager: "Hanna Tesfaye", emergencyContact: "Selamawit Kebede, spouse", probation: "Completed" },
  { id: "hanna-tesfaye", employeeId: "EMP-2026-002", name: "Hanna Tesfaye", initials: "HT", position: "Vice Principal", department: "Administration", type: "Full-time", joinDate: "2020-01-13", status: "Active", phone: "+251 912 773 405", email: "hanna.tesfaye@classease.edu.et", location: "Addis Ababa", manager: "Principal Office", emergencyContact: "Tesfaye Alemu, father", probation: "Completed" },
  { id: "dawit-bekele", employeeId: "EMP-2026-003", name: "Dawit Bekele", initials: "DB", position: "IT Administrator", department: "Information Technology", type: "Full-time", joinDate: "2023-04-10", status: "Active", phone: "+251 913 501 922", email: "dawit.bekele@classease.edu.et", location: "Addis Ababa", manager: "Hanna Tesfaye", emergencyContact: "Mekdes Bekele, sister", probation: "Completed" },
  { id: "meron-alemu", employeeId: "EMP-2026-004", name: "Meron Alemu", initials: "MA", position: "HR Officer", department: "Human Resources", type: "Full-time", joinDate: "2024-02-19", status: "Active", phone: "+251 914 668 230", email: "meron.alemu@classease.edu.et", location: "Addis Ababa", manager: "Hanna Tesfaye", emergencyContact: "Alemu Tola, father", probation: "Completed" },
  { id: "samuel-girma", employeeId: "EMP-2026-005", name: "Samuel Girma", initials: "SG", position: "Science Teacher", department: "Teaching", type: "Contract", joinDate: "2025-08-25", status: "Probation", phone: "+251 911 876 301", email: "samuel.girma@classease.edu.et", location: "Addis Ababa", manager: "Abebe Kebede", contractEnd: "2027-08-24", emergencyContact: "Rahel Girma, sister", probation: "Ends Sep 2026" },
  { id: "rahel-tadesse", employeeId: "EMP-2026-006", name: "Rahel Tadesse", initials: "RT", position: "School Nurse", department: "Student Services", type: "Full-time", joinDate: "2021-11-01", status: "On Leave", phone: "+251 915 337 811", email: "rahel.tadesse@classease.edu.et", location: "Addis Ababa", manager: "Hanna Tesfaye", emergencyContact: "Tadesse Haile, father", probation: "Completed" },
  { id: "yonas-mekonnen", employeeId: "EMP-2026-007", name: "Yonas Mekonnen", initials: "YM", position: "Accountant", department: "Finance", type: "Full-time", joinDate: "2022-06-14", status: "Active", phone: "+251 916 908 712", email: "yonas.mekonnen@classease.edu.et", location: "Addis Ababa", manager: "Hanna Tesfaye", emergencyContact: "Mimi Mekonnen, spouse", probation: "Completed" },
  { id: "selamawit-fikru", employeeId: "EMP-2026-008", name: "Selamawit Fikru", initials: "SF", position: "English Teacher", department: "Teaching", type: "Part-time", joinDate: "2026-08-03", status: "Active", phone: "+251 917 119 604", email: "selamawit.fikru@classease.edu.et", location: "Addis Ababa", manager: "Abebe Kebede", emergencyContact: "Fikru Desta, father", probation: "In progress" },
  { id: "kidus-haile", employeeId: "EMP-2026-009", name: "Kidus Haile", initials: "KH", position: "Librarian", department: "Student Services", type: "Full-time", joinDate: "2023-09-11", status: "Active", phone: "+251 918 310 456", email: "kidus.haile@classease.edu.et", location: "Addis Ababa", manager: "Rahel Tadesse", emergencyContact: "Haile Negash, father", probation: "Completed" },
  { id: "eden-mulugeta", employeeId: "EMP-2026-010", name: "Eden Mulugeta", initials: "EM", position: "Administrative Assistant", department: "Administration", type: "Full-time", joinDate: "2024-10-07", status: "Active", phone: "+251 919 430 601", email: "eden.mulugeta@classease.edu.et", location: "Addis Ababa", manager: "Hanna Tesfaye", emergencyContact: "Mulugeta Worku, father", probation: "Completed" },
  { id: "bereket-solomon", employeeId: "EMP-2026-011", name: "Bereket Solomon", initials: "BS", position: "Security Officer", department: "Security", type: "Contract", joinDate: "2025-03-17", status: "Active", phone: "+251 911 420 731", email: "bereket.solomon@classease.edu.et", location: "Addis Ababa", manager: "Eden Mulugeta", contractEnd: "2027-03-16", emergencyContact: "Solomon Berhanu, father", probation: "Completed" },
  { id: "tigist-assefa", employeeId: "EMP-2026-012", name: "Tigist Assefa", initials: "TA", position: "Maintenance Supervisor", department: "Maintenance", type: "Full-time", joinDate: "2021-02-22", status: "Active", phone: "+251 912 610 338", email: "tigist.assefa@classease.edu.et", location: "Addis Ababa", manager: "Eden Mulugeta", emergencyContact: "Assefa Dinku, father", probation: "Completed" },
];

export const departments: Department[] = [
  { id: "teaching", name: "Teaching", code: "TCH", manager: "Abebe Kebede", employees: 112, openPositions: 4, status: "Active", budget: "ETB 18.4M", activity: ["Two teacher contracts renewed", "Grade 9 science vacancy approved", "New English teacher onboarded"] },
  { id: "administration", name: "Administration", code: "ADM", manager: "Hanna Tesfaye", employees: 18, openPositions: 1, status: "Active", budget: "ETB 4.2M", activity: ["Front office rota updated", "Policy acknowledgement completed"] },
  { id: "human-resources", name: "Human Resources", code: "HR", manager: "Meron Alemu", employees: 6, openPositions: 0, status: "Active", budget: "ETB 1.6M", activity: ["August leave audit completed", "Staff files reviewed"] },
  { id: "finance", name: "Finance", code: "FIN", manager: "Yonas Mekonnen", employees: 9, openPositions: 0, status: "Active", budget: "ETB 2.8M", activity: ["Payroll inputs validated", "Tax certificates collected"] },
  { id: "information-technology", name: "Information Technology", code: "IT", manager: "Dawit Bekele", employees: 7, openPositions: 1, status: "Active", budget: "ETB 2.1M", activity: ["Biometric terminal maintenance scheduled"] },
  { id: "student-services", name: "Student Services", code: "STS", manager: "Rahel Tadesse", employees: 14, openPositions: 0, status: "Active", budget: "ETB 3.5M", activity: ["Health records training completed"] },
  { id: "maintenance", name: "Maintenance", code: "MNT", manager: "Tigist Assefa", employees: 8, openPositions: 0, status: "Restructuring", budget: "ETB 1.9M", activity: ["Shift plan reviewed"] },
  { id: "security", name: "Security", code: "SEC", manager: "Bereket Solomon", employees: 10, openPositions: 0, status: "Active", budget: "ETB 2.0M", activity: ["Gate coverage report submitted"] },
];

export const positions: Position[] = [
  { id: "mathematics-teacher", title: "Mathematics Teacher", code: "POS-TCH-001", department: "Teaching", type: "Full-time", level: "Senior Teacher", employees: 18, openings: 1, status: "Hiring", description: "Leads upper-primary and secondary mathematics instruction.", responsibilities: ["Prepare weekly lesson plans", "Assess student progress", "Support exam moderation"], requirements: ["BEd or related degree", "4+ years teaching experience", "Strong classroom management"] },
  { id: "english-teacher", title: "English Teacher", code: "POS-TCH-002", department: "Teaching", type: "Part-time", level: "Teacher", employees: 12, openings: 1, status: "Hiring", description: "Delivers English language and literature classes.", responsibilities: ["Run reading interventions", "Prepare language assessments", "Coach debate club"], requirements: ["English degree", "Teaching certification", "Excellent written English"] },
  { id: "science-teacher", title: "Science Teacher", code: "POS-TCH-003", department: "Teaching", type: "Contract", level: "Teacher", employees: 14, openings: 2, status: "Hiring", description: "Teaches integrated science and lab safety.", responsibilities: ["Manage lab sessions", "Maintain equipment logs", "Prepare practical assessments"], requirements: ["Science education degree", "Lab safety knowledge", "2+ years experience"] },
  { id: "school-principal", title: "School Principal", code: "POS-ADM-001", department: "Administration", type: "Full-time", level: "Executive", employees: 1, openings: 0, status: "Active", description: "Provides academic and operational leadership.", responsibilities: ["Lead school strategy", "Manage senior staff", "Represent the school"], requirements: ["Master's preferred", "10+ years leadership", "School operations experience"] },
  { id: "accountant", title: "Accountant", code: "POS-FIN-001", department: "Finance", type: "Full-time", level: "Officer", employees: 4, openings: 0, status: "Active", description: "Handles payroll inputs, reconciliation, and statutory records.", responsibilities: ["Prepare payroll schedules", "Reconcile accounts", "Maintain financial files"], requirements: ["Accounting degree", "IFRS familiarity", "Payroll experience"] },
  { id: "it-administrator", title: "IT Administrator", code: "POS-IT-001", department: "Information Technology", type: "Full-time", level: "Officer", employees: 3, openings: 1, status: "Hiring", description: "Maintains school systems, network, and devices.", responsibilities: ["Support staff accounts", "Maintain devices", "Monitor network uptime"], requirements: ["IT diploma or degree", "Network administration", "Helpdesk experience"] },
  { id: "school-nurse", title: "School Nurse", code: "POS-STS-001", department: "Student Services", type: "Full-time", level: "Specialist", employees: 2, openings: 0, status: "Active", description: "Coordinates student health support and first aid.", responsibilities: ["Maintain health records", "Provide first aid", "Coordinate referrals"], requirements: ["Nursing license", "Pediatric care experience", "Recordkeeping skills"] },
  { id: "security-officer", title: "Security Officer", code: "POS-SEC-001", department: "Security", type: "Contract", level: "Support", employees: 10, openings: 0, status: "Active", description: "Protects campus access points and supports safety routines.", responsibilities: ["Monitor gates", "Maintain visitor logs", "Report incidents"], requirements: ["Security experience", "Shift availability", "Incident reporting"] },
];

export const jobPostings: JobPosting[] = [
  { id: "job-math-teacher", position: "Mathematics Teacher", department: "Teaching", type: "Full-time", openings: 1, applications: 9, postedDate: "2026-08-01", deadline: "2026-08-30", status: "Published", description: "Seeking a senior mathematics teacher for Grades 7-10." },
  { id: "job-science-teacher", position: "Science Teacher", department: "Teaching", type: "Contract", openings: 2, applications: 11, postedDate: "2026-08-05", deadline: "2026-09-05", status: "Published", description: "Contract science teacher role with laboratory coordination." },
  { id: "job-it-admin", position: "IT Administrator", department: "Information Technology", type: "Full-time", openings: 1, applications: 4, postedDate: "2026-07-20", deadline: "2026-08-25", status: "Published", description: "IT administrator for school systems and staff support." },
  { id: "job-english-teacher", position: "English Teacher", department: "Teaching", type: "Part-time", openings: 1, applications: 7, postedDate: "2026-07-01", deadline: "2026-08-15", status: "Closed", description: "Part-time English teacher for reading intervention groups." },
];

export const applications: JobApplication[] = [
  { id: "app-biruk-lemma", candidate: "Biruk Lemma", position: "Mathematics Teacher", applicationDate: "2026-08-04", experience: "6 years", education: "BEd Mathematics, Addis Ababa University", status: "Interview", interviewDate: "2026-08-22", recruiter: "Meron Alemu", location: "Addis Ababa", contact: "biruk.lemma@email.com", skills: ["Exam preparation", "STEM club", "Grade 10 math"] },
  { id: "app-mahitab-gebre", candidate: "Mahitab Gebre", position: "Science Teacher", applicationDate: "2026-08-06", experience: "4 years", education: "BSc Biology, Kotebe University", status: "Shortlisted", interviewDate: "2026-08-26", recruiter: "Meron Alemu", location: "Addis Ababa", contact: "mahitab.gebre@email.com", skills: ["Lab safety", "Biology", "Student projects"] },
  { id: "app-nahom-feyissa", candidate: "Nahom Feyissa", position: "IT Administrator", applicationDate: "2026-08-08", experience: "5 years", education: "BSc Computer Science, HiLCoE", status: "Screening", recruiter: "Dawit Bekele", location: "Addis Ababa", contact: "nahom.feyissa@email.com", skills: ["Networking", "Device management", "Google Workspace"] },
  { id: "app-lidya-amanuel", candidate: "Lidya Amanuel", position: "English Teacher", applicationDate: "2026-07-14", experience: "3 years", education: "BA English, Addis Ababa University", status: "Offer", recruiter: "Meron Alemu", location: "Bishoftu", contact: "lidya.amanuel@email.com", skills: ["Reading intervention", "Debate coaching", "Assessment"] },
  { id: "app-mintesnot-adesse", candidate: "Mintesnot Adesse", position: "Science Teacher", applicationDate: "2026-08-10", experience: "2 years", education: "BEd Chemistry, Bahir Dar University", status: "New", recruiter: "Meron Alemu", location: "Addis Ababa", contact: "mintesnot.adesse@email.com", skills: ["Chemistry", "Lesson planning"] },
];

export const leaveRequests: LeaveRequest[] = [
  { id: "leave-1", employee: "Rahel Tadesse", type: "Sick Leave", startDate: "2026-08-18", endDate: "2026-08-22", duration: "5 days", reason: "Medical recovery", status: "Approved" },
  { id: "leave-2", employee: "Abebe Kebede", type: "Annual Leave", startDate: "2026-09-02", endDate: "2026-09-06", duration: "5 days", reason: "Family travel", status: "Pending" },
  { id: "leave-3", employee: "Eden Mulugeta", type: "Emergency Leave", startDate: "2026-08-21", endDate: "2026-08-21", duration: "1 day", reason: "Family emergency", status: "Pending" },
  { id: "leave-4", employee: "Samuel Girma", type: "Study Leave", startDate: "2026-09-12", endDate: "2026-09-14", duration: "3 days", reason: "Certification exam", status: "Approved" },
];

export const attendanceRecords: AttendanceRecord[] = [
  { employee: "Abebe Kebede", present: 18, late: 1, absent: 0, leave: 0, rate: 99 },
  { employee: "Hanna Tesfaye", present: 19, late: 0, absent: 0, leave: 0, rate: 100 },
  { employee: "Rahel Tadesse", present: 14, late: 0, absent: 0, leave: 5, rate: 100 },
  { employee: "Samuel Girma", present: 17, late: 2, absent: 0, leave: 0, rate: 98 },
  { employee: "Bereket Solomon", present: 18, late: 0, absent: 1, leave: 0, rate: 95 },
];

export const performanceReviews: PerformanceReview[] = [
  { id: "review-1", employee: "Abebe Kebede", department: "Teaching", position: "Mathematics Teacher", period: "2026 Mid-Year", rating: "Exceeds Expectations", reviewer: "Hanna Tesfaye", status: "Completed", comments: "Strong exam preparation outcomes and mentoring for new teachers." },
  { id: "review-2", employee: "Dawit Bekele", department: "Information Technology", position: "IT Administrator", period: "2026 Mid-Year", rating: "Meets Expectations", reviewer: "Hanna Tesfaye", status: "Completed", comments: "Reliable support; next goal is faster incident response reporting." },
  { id: "review-3", employee: "Samuel Girma", department: "Teaching", position: "Science Teacher", period: "Probation Review", rating: "Meets Expectations", reviewer: "Abebe Kebede", status: "Pending", comments: "Probation review scheduled after first assessment cycle." },
  { id: "review-4", employee: "Tigist Assefa", department: "Maintenance", position: "Maintenance Supervisor", period: "2026 Mid-Year", rating: "Outstanding", reviewer: "Eden Mulugeta", status: "Completed", comments: "Preventive maintenance schedule reduced classroom service requests." },
];

export const documents: EmployeeDocument[] = [
  { id: "doc-1", name: "Employment Contract", employee: "Samuel Girma", category: "Employment", uploadDate: "2025-08-25", expirationDate: "2027-08-24", status: "Valid" },
  { id: "doc-2", name: "Teaching Certificate", employee: "Abebe Kebede", category: "Academic", uploadDate: "2024-09-01", expirationDate: "2026-10-10", status: "Expiring Soon" },
  { id: "doc-3", name: "National ID", employee: "Rahel Tadesse", category: "Identification", uploadDate: "2023-01-12", expirationDate: "2026-07-30", status: "Expired" },
  { id: "doc-4", name: "Tax Registration", employee: "Yonas Mekonnen", category: "Financial", uploadDate: "2026-01-08", status: "Valid" },
  { id: "doc-5", name: "Medical Clearance", employee: "Bereket Solomon", category: "Medical", uploadDate: "2026-08-02", expirationDate: "2027-08-02", status: "Pending Verification" },
];

export const workforceByDepartment = [
  { department: "Teaching", employees: 112 },
  { department: "Administration", employees: 18 },
  { department: "Finance", employees: 9 },
  { department: "Human Resources", employees: 6 },
  { department: "IT", employees: 7 },
  { department: "Student Services", employees: 14 },
  { department: "Maintenance", employees: 8 },
  { department: "Security", employees: 10 },
];

export const employmentTypes = [
  { type: "Full-time", count: 138 },
  { type: "Part-time", count: 18 },
  { type: "Contract", count: 24 },
  { type: "Temporary", count: 4 },
];

export const pipeline = [
  { stage: "Applications", count: 24 },
  { stage: "Screening", count: 10 },
  { stage: "Shortlisted", count: 7 },
  { stage: "Interview", count: 4 },
  { stage: "Offer", count: 2 },
  { stage: "Hired", count: 1 },
];

export const attendanceTrend = [
  { day: "Mon", rate: 96 },
  { day: "Tue", rate: 97 },
  { day: "Wed", rate: 95 },
  { day: "Thu", rate: 98 },
  { day: "Fri", rate: 94 },
];
