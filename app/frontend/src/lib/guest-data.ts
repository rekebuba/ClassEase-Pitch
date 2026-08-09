export type GuestProfile = {
  firstName: string;
  lastName: string;
  email: string;
  phone: string;
  dateOfBirth: string;
  gender: string;
  photoUrl: string;
  city: string;
  address: string;
  highestEducation: string;
  fieldOfStudy: string;
  institution: string;
  yearsOfExperience: string;
  skills: string;
  certifications: string;
  summary: string;
};

export type GuestApplicationStatus
  = | "Pending"
  | "Under Review"
  | "Accepted"
  | "Rejected"
  | "Withdrawn";

export type SchoolPosition = {
  id: string;
  title: string;
  category: string;
  employmentType: string;
  status: "Open" | "Closed";
  deadline: string;
  summary: string;
  description: string;
  requirements: string[];
  responsibilities: string[];
  benefits: string[];
  location: string;
  openingsCount: number;
  allowApplications: boolean;
};

export type EnrollmentOpportunity = {
  id: string;
  academicYear: string;
  grade: string;
  status: "Open" | "Closed";
  deadline: string;
  capacity: number;
  remainingSeats: number;
  allowApplications: boolean;
};

export type GuestSchool = {
  slug: string;
  name: string;
  logo: string;
  location: string;
  city: string;
  category: string;
  description: string;
  about: string;
  applicationsOpen: boolean;
  deadline: string;
  students: string;
  curriculum: string;
  enrollmentOpportunities: EnrollmentOpportunity[];
  positions: SchoolPosition[];
};

export type GuestApplication = {
  id: string;
  kind: "Employment" | "Enrollment";
  schoolSlug: string;
  schoolName: string;
  opportunityId: string;
  opportunityTitle: string;
  submittedAt: string;
  status: GuestApplicationStatus;
  applicantName: string;
  email: string;
  phone: string;
  education: string;
  experience: string;
};

export const requiredProfileFields: Array<{
  key: keyof GuestProfile;
  label: string;
  group: "Employment Profile";
}> = [
  { key: "firstName", label: "First name", group: "Employment Profile" },
  { key: "lastName", label: "Last name", group: "Employment Profile" },
  { key: "email", label: "Email", group: "Employment Profile" },
  { key: "phone", label: "Phone number", group: "Employment Profile" },
  { key: "city", label: "City", group: "Employment Profile" },
  { key: "highestEducation", label: "Highest education", group: "Employment Profile" },
  { key: "fieldOfStudy", label: "Field of study", group: "Employment Profile" },
  { key: "yearsOfExperience", label: "Years of experience", group: "Employment Profile" },
];

export const emptyGuestProfile: GuestProfile = {
  firstName: "",
  lastName: "",
  email: "abubeker@example.com",
  phone: "",
  dateOfBirth: "",
  gender: "",
  photoUrl: "",
  city: "",
  address: "",
  highestEducation: "",
  fieldOfStudy: "",
  institution: "",
  yearsOfExperience: "",
  skills: "",
  certifications: "",
  summary: "",
};

export const demoGuestProfile: GuestProfile = {
  firstName: "Abubeker",
  lastName: "Abdullahi",
  email: "abubeker@example.com",
  phone: "+251 91 234 5678",
  dateOfBirth: "1998-04-12",
  gender: "Male",
  photoUrl: "",
  city: "Addis Ababa",
  address: "Bole, Addis Ababa",
  highestEducation: "Bachelor's degree",
  fieldOfStudy: "Software Engineering",
  institution: "Addis Ababa Science and Technology University",
  yearsOfExperience: "3",
  skills: "Mathematics instruction, classroom technology, lesson planning",
  certifications: "Teaching methodology certificate",
  summary: "Teacher candidate with strong technology skills and experience supporting secondary school learners.",
};

export const guestSchools: GuestSchool[] = [
  {
    slug: "addis-ababa-high-school",
    name: "Addis Ababa High School",
    logo: "AA",
    location: "Addis Ababa, Ethiopia",
    city: "Addis Ababa",
    category: "Private Secondary School",
    description: "A secondary school building strong academic habits through structured teaching and modern classroom tools.",
    about: "Addis Ababa High School serves lower and upper secondary students with a focus on mathematics, science, languages, and digital learning. The school is expanding its academic team for the coming term.",
    applicationsOpen: true,
    deadline: "2026-08-30",
    students: "1,200 students",
    curriculum: "National curriculum with STEM enrichment",
    enrollmentOpportunities: [
      {
        id: "grade-5-2026",
        academicYear: "2026/2027",
        grade: "Grade 5",
        status: "Open",
        deadline: "2026-08-30",
        capacity: 60,
        remainingSeats: 12,
        allowApplications: true,
      },
      {
        id: "grade-9-2026",
        academicYear: "2026/2027",
        grade: "Grade 9",
        status: "Open",
        deadline: "2026-08-30",
        capacity: 90,
        remainingSeats: 18,
        allowApplications: true,
      },
    ],
    positions: [
      {
        id: "math-teacher",
        title: "Mathematics Teacher",
        category: "Teaching",
        employmentType: "Full-time",
        status: "Open",
        deadline: "2026-08-30",
        summary: "Teach grades 9-12 mathematics and support exam preparation with practical, student-centered lessons.",
        description: "Addis Ababa High School is hiring a mathematics teacher to lead secondary classes, prepare learners for national exams, and contribute to a structured STEM program.",
        requirements: ["Bachelor's degree in Mathematics, Education, Engineering, or a related field", "At least 2 years of classroom or tutoring experience", "Strong lesson planning and assessment skills"],
        responsibilities: ["Prepare daily lessons and weekly assessments", "Track learner progress and communicate concerns early", "Collaborate with the science department on STEM activities"],
        benefits: ["Structured academic calendar", "Professional development support", "Collaborative STEM department"],
        location: "Addis Ababa",
        openingsCount: 2,
        allowApplications: true,
      },
      {
        id: "english-teacher",
        title: "English Teacher",
        category: "Teaching",
        employmentType: "Full-time",
        status: "Open",
        deadline: "2026-09-05",
        summary: "Lead English language classes with emphasis on reading, writing, and confident communication.",
        description: "The English department is looking for a teacher who can build strong reading, writing, speaking, and exam preparation routines.",
        requirements: ["Degree in English, Literature, Linguistics, or Education", "Clear spoken and written English", "Experience preparing students for national exams"],
        responsibilities: ["Design reading and writing assignments", "Facilitate speaking practice", "Maintain clear feedback records"],
        benefits: ["Mentorship from senior teachers", "Exam preparation resources", "Family engagement support"],
        location: "Addis Ababa",
        openingsCount: 1,
        allowApplications: true,
      },
    ],
  },
  {
    slug: "unity-stem-academy",
    name: "Unity STEM Academy",
    logo: "US",
    location: "Adama, Ethiopia",
    city: "Adama",
    category: "STEM Preparatory School",
    description: "A technology-forward academy hiring educators who enjoy labs, projects, and measurable student growth.",
    about: "Unity STEM Academy combines the national curriculum with project-based learning. The school is seeking staff who can connect theory to practical problem solving.",
    applicationsOpen: true,
    deadline: "2026-09-12",
    students: "860 students",
    curriculum: "STEM preparatory program",
    enrollmentOpportunities: [
      {
        id: "grade-7-2026",
        academicYear: "2026/2027",
        grade: "Grade 7",
        status: "Open",
        deadline: "2026-09-12",
        capacity: 48,
        remainingSeats: 9,
        allowApplications: true,
      },
    ],
    positions: [
      {
        id: "science-teacher",
        title: "Science Teacher",
        category: "Teaching",
        employmentType: "Full-time",
        status: "Open",
        deadline: "2026-09-12",
        summary: "Teach integrated science and coordinate safe, engaging laboratory sessions for middle school learners.",
        description: "Unity STEM Academy needs a science teacher who can connect classroom theory to labs, student projects, and measurable progress.",
        requirements: ["Degree in Biology, Chemistry, Physics, or Education", "Laboratory safety knowledge", "Comfort with digital classroom tools"],
        responsibilities: ["Run weekly lab activities", "Create practical assessments", "Support the annual science fair"],
        benefits: ["Lab access", "Project-based learning resources", "STEM event budget"],
        location: "Adama",
        openingsCount: 1,
        allowApplications: true,
      },
      {
        id: "ict-instructor",
        title: "ICT Instructor",
        category: "Technology",
        employmentType: "Part-time",
        status: "Open",
        deadline: "2026-09-15",
        summary: "Introduce students to productivity software, coding basics, and responsible technology use.",
        description: "The academy is adding part-time ICT instruction for beginner-friendly productivity, coding, and digital citizenship classes.",
        requirements: ["Diploma or degree in Computer Science, IT, or a related field", "Strong practical computer skills", "Ability to teach beginner-friendly classes"],
        responsibilities: ["Maintain ICT lesson plans", "Guide project work", "Coordinate with academic staff on digital assignments"],
        benefits: ["Flexible teaching schedule", "Computer lab access", "Curriculum planning support"],
        location: "Adama",
        openingsCount: 1,
        allowApplications: true,
      },
    ],
  },
  {
    slug: "blue-nile-community-school",
    name: "Blue Nile Community School",
    logo: "BN",
    location: "Bahir Dar, Ethiopia",
    city: "Bahir Dar",
    category: "Community School",
    description: "A community-centered school looking for organized academic and student support professionals.",
    about: "Blue Nile Community School is known for close family engagement and a calm learning environment. Current openings support both academics and student services.",
    applicationsOpen: true,
    deadline: "2026-08-24",
    students: "640 students",
    curriculum: "National curriculum",
    enrollmentOpportunities: [
      {
        id: "grade-1-2026",
        academicYear: "2026/2027",
        grade: "Grade 1",
        status: "Open",
        deadline: "2026-08-24",
        capacity: 40,
        remainingSeats: 6,
        allowApplications: true,
      },
    ],
    positions: [
      {
        id: "guidance-counselor",
        title: "Guidance Counselor",
        category: "Student Support",
        employmentType: "Full-time",
        status: "Open",
        deadline: "2026-08-24",
        summary: "Support students with academic planning, personal development, and family communication.",
        description: "Blue Nile Community School is hiring a counselor to support academic planning, student wellbeing, and family communication.",
        requirements: ["Degree in Psychology, Counseling, Education, or Social Work", "Strong listening and documentation skills", "Experience working with adolescents"],
        responsibilities: ["Hold student support sessions", "Coordinate referrals when needed", "Maintain confidential support records"],
        benefits: ["Confidential counseling space", "Supportive leadership team", "Community engagement program"],
        location: "Bahir Dar",
        openingsCount: 1,
        allowApplications: true,
      },
    ],
  },
  {
    slug: "future-leaders-primary",
    name: "Future Leaders Primary",
    logo: "FL",
    location: "Hawassa, Ethiopia",
    city: "Hawassa",
    category: "Primary School",
    description: "A growing primary school hiring patient classroom educators and early-grade specialists.",
    about: "Future Leaders Primary focuses on foundational literacy, numeracy, and positive classroom routines. The school values teachers who create structured and warm learning spaces.",
    applicationsOpen: false,
    deadline: "2026-08-18",
    students: "520 students",
    curriculum: "Primary national curriculum",
    enrollmentOpportunities: [
      {
        id: "grade-3-2026",
        academicYear: "2026/2027",
        grade: "Grade 3",
        status: "Closed",
        deadline: "2026-08-18",
        capacity: 35,
        remainingSeats: 0,
        allowApplications: false,
      },
    ],
    positions: [
      {
        id: "primary-teacher",
        title: "Primary Teacher",
        category: "Teaching",
        employmentType: "Full-time",
        status: "Closed",
        deadline: "2026-08-18",
        summary: "Teach core subjects for upper-primary learners and maintain strong parent communication.",
        description: "Future Leaders Primary keeps this position visible for reference, but applications are currently closed.",
        requirements: ["Diploma or degree in Primary Education", "Experience with child-centered classroom management", "Strong Amharic and English communication"],
        responsibilities: ["Plan daily literacy and numeracy lessons", "Monitor student behavior and progress", "Prepare simple parent updates"],
        benefits: ["Primary teaching resources", "Parent communication tools", "Supportive grade-level team"],
        location: "Hawassa",
        openingsCount: 1,
        allowApplications: false,
      },
    ],
  },
];

export const initialGuestApplications: GuestApplication[] = [
  {
    id: "app-001",
    kind: "Employment",
    schoolSlug: "blue-nile-community-school",
    schoolName: "Blue Nile Community School",
    opportunityId: "guidance-counselor",
    opportunityTitle: "Guidance Counselor",
    submittedAt: "2026-08-05",
    status: "Under Review",
    applicantName: "Abubeker Abdullahi",
    email: "abubeker@example.com",
    phone: "+251 91 234 5678",
    education: "Bachelor's degree in Software Engineering",
    experience: "3 years",
  },
];

export function getProfileMissingFields(profile: GuestProfile) {
  return requiredProfileFields.filter(field => String(profile[field.key] ?? "").trim().length === 0);
}

export function getProfileCompletion(profile: GuestProfile) {
  const missing = getProfileMissingFields(profile);
  return Math.round(((requiredProfileFields.length - missing.length) / requiredProfileFields.length) * 100);
}

export function formatGuestDate(value: string) {
  return new Intl.DateTimeFormat("en", {
    month: "short",
    day: "numeric",
    year: "numeric",
  }).format(new Date(`${value}T00:00:00`));
}

export function findSchool(slug: string) {
  return guestSchools.find(school => school.slug === slug);
}

export function findPosition(schoolSlug: string, positionId: string) {
  return findSchool(schoolSlug)?.positions.find(position => position.id === positionId);
}

export function getOpenPositions() {
  return guestSchools.flatMap(school =>
    school.positions.map(position => ({ school, position })));
}

export function isPositionAcceptingApplications(position: SchoolPosition) {
  return position.status === "Open" && position.allowApplications && new Date(`${position.deadline}T23:59:59`) >= new Date();
}

export function isEnrollmentAcceptingApplications(opportunity: EnrollmentOpportunity) {
  return opportunity.status === "Open"
    && opportunity.allowApplications
    && opportunity.remainingSeats > 0
    && new Date(`${opportunity.deadline}T23:59:59`) >= new Date();
}
