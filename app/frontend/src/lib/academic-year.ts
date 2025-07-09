export interface AcademicYear {
    id: string
    name: string
    startDate: string
    endDate: string
    termSystem: "quarterly" | "semesterly"
    status: "draft" | "active" | "completed"
    grades: Grade[]
    subjects: Subject[]
    createdAt: string
    updatedAt: string
}

export interface Grade {
    id: string
    name: string
    level: number
    hasStreams: boolean
    streams: Stream[]
    maxSections: number
    sections: string[]
    subjects: string[]
}

export interface Stream {
    id: string
    name: string
    code: string
    description: string
    subjects: string[]
}

export interface Subject {
    id: string
    name: string
    code: string
    category: "core" | "elective" | "language" | "arts" | "physical" | "technical"
    description: string
    grades: string[]
    isRequired: boolean
}

export interface Term {
    id: string
    name: string
    startDate: string
    endDate: string
    order: number
}

export const SUGGESTED_SUBJECTS: Subject[] = [
    // Core Subjects
    {
        id: "1",
        name: "Mathematics",
        code: "MATH",
        category: "core",
        description: "Basic and advanced mathematics",
        grades: [],
        isRequired: true,
    },
    {
        id: "2",
        name: "English Language",
        code: "ENG",
        category: "language",
        description: "English language and literature",
        grades: [],
        isRequired: true,
    },
    {
        id: "3",
        name: "Science",
        code: "SCI",
        category: "core",
        description: "General science concepts",
        grades: [],
        isRequired: true,
    },
    {
        id: "4",
        name: "Social Studies",
        code: "SOC",
        category: "core",
        description: "History, geography, and civics",
        grades: [],
        isRequired: true,
    },

    // Advanced Sciences
    {
        id: "5",
        name: "Physics",
        code: "PHY",
        category: "core",
        description: "Physics principles and applications",
        grades: [],
        isRequired: false,
    },
    {
        id: "6",
        name: "Chemistry",
        code: "CHEM",
        category: "core",
        description: "Chemical principles and reactions",
        grades: [],
        isRequired: false,
    },
    {
        id: "7",
        name: "Biology",
        code: "BIO",
        category: "core",
        description: "Life sciences and biological processes",
        grades: [],
        isRequired: false,
    },

    // Languages
    {
        id: "8",
        name: "Spanish",
        code: "SPA",
        category: "language",
        description: "Spanish language and culture",
        grades: [],
        isRequired: false,
    },
    {
        id: "9",
        name: "French",
        code: "FRE",
        category: "language",
        description: "French language and culture",
        grades: [],
        isRequired: false,
    },
    {
        id: "10",
        name: "Arabic",
        code: "ARA",
        category: "language",
        description: "Arabic language and literature",
        grades: [],
        isRequired: false,
    },

    // Arts and Creative
    {
        id: "11",
        name: "Art",
        code: "ART",
        category: "arts",
        description: "Visual arts and creative expression",
        grades: [],
        isRequired: false,
    },
    {
        id: "12",
        name: "Music",
        code: "MUS",
        category: "arts",
        description: "Music theory and performance",
        grades: [],
        isRequired: false,
    },
    {
        id: "13",
        name: "Drama",
        code: "DRA",
        category: "arts",
        description: "Theater and dramatic arts",
        grades: [],
        isRequired: false,
    },

    // Physical Education
    {
        id: "14",
        name: "Physical Education",
        code: "PE",
        category: "physical",
        description: "Physical fitness and sports",
        grades: [],
        isRequired: true,
    },
    {
        id: "15",
        name: "Health Education",
        code: "HEALTH",
        category: "physical",
        description: "Health and wellness education",
        grades: [],
        isRequired: false,
    },

    // Technical and Vocational
    {
        id: "16",
        name: "Computer Science",
        code: "CS",
        category: "technical",
        description: "Programming and computer literacy",
        grades: [],
        isRequired: false,
    },
    {
        id: "17",
        name: "Information Technology",
        code: "IT",
        category: "technical",
        description: "IT skills and digital literacy",
        grades: [],
        isRequired: false,
    },
    {
        id: "18",
        name: "Business Studies",
        code: "BUS",
        category: "technical",
        description: "Business principles and economics",
        grades: [],
        isRequired: false,
    },

    // Additional Electives
    {
        id: "19",
        name: "Psychology",
        code: "PSY",
        category: "elective",
        description: "Introduction to psychology",
        grades: [],
        isRequired: false,
    },
    {
        id: "20",
        name: "Philosophy",
        code: "PHIL",
        category: "elective",
        description: "Philosophical thinking and ethics",
        grades: [],
        isRequired: false,
    },
    {
        id: "21",
        name: "Environmental Science",
        code: "ENV",
        category: "core",
        description: "Environmental awareness and sustainability",
        grades: [],
        isRequired: false,
    },
    {
        id: "22",
        name: "Geography",
        code: "GEO",
        category: "core",
        description: "Physical and human geography",
        grades: [],
        isRequired: false,
    },
    {
        id: "23",
        name: "History",
        code: "HIST",
        category: "core",
        description: "World and local history",
        grades: [],
        isRequired: false,
    },
]

export const GRADE_SUGGESTIONS = [
    {
        name: "Kindergarten",
        level: 0,
        hasStreams: false,
        defaultSubjects: ["English Language", "Mathematics", "Science", "Art", "Music", "Physical Education"],
    },
    {
        name: "Grade 1",
        level: 1,
        hasStreams: false,
        defaultSubjects: [
            "English Language",
            "Mathematics",
            "Science",
            "Social Studies",
            "Art",
            "Music",
            "Physical Education",
        ],
    },
    {
        name: "Grade 2",
        level: 2,
        hasStreams: false,
        defaultSubjects: [
            "English Language",
            "Mathematics",
            "Science",
            "Social Studies",
            "Art",
            "Music",
            "Physical Education",
        ],
    },
    {
        name: "Grade 3",
        level: 3,
        hasStreams: false,
        defaultSubjects: [
            "English Language",
            "Mathematics",
            "Science",
            "Social Studies",
            "Art",
            "Music",
            "Physical Education",
        ],
    },
    {
        name: "Grade 4",
        level: 4,
        hasStreams: false,
        defaultSubjects: [
            "English Language",
            "Mathematics",
            "Science",
            "Social Studies",
            "Art",
            "Music",
            "Physical Education",
        ],
    },
    {
        name: "Grade 5",
        level: 5,
        hasStreams: false,
        defaultSubjects: [
            "English Language",
            "Mathematics",
            "Science",
            "Social Studies",
            "Art",
            "Music",
            "Physical Education",
        ],
    },
    {
        name: "Grade 6",
        level: 6,
        hasStreams: false,
        defaultSubjects: [
            "English Language",
            "Mathematics",
            "Science",
            "Social Studies",
            "Art",
            "Music",
            "Physical Education",
        ],
    },
    {
        name: "Grade 7",
        level: 7,
        hasStreams: false,
        defaultSubjects: [
            "English Language",
            "Mathematics",
            "Science",
            "Social Studies",
            "Art",
            "Music",
            "Physical Education",
            "Computer Science",
        ],
    },
    {
        name: "Grade 8",
        level: 8,
        hasStreams: false,
        defaultSubjects: [
            "English Language",
            "Mathematics",
            "Science",
            "Social Studies",
            "Art",
            "Music",
            "Physical Education",
            "Computer Science",
        ],
    },
    {
        name: "Grade 9",
        level: 9,
        hasStreams: false,
        defaultSubjects: [
            "English Language",
            "Mathematics",
            "Physics",
            "Chemistry",
            "Biology",
            "History",
            "Geography",
            "Physical Education",
        ],
    },
    {
        name: "Grade 10",
        level: 10,
        hasStreams: false,
        defaultSubjects: [
            "English Language",
            "Mathematics",
            "Physics",
            "Chemistry",
            "Biology",
            "History",
            "Geography",
            "Physical Education",
        ],
    },
    { name: "Grade 11", level: 11, hasStreams: true, defaultSubjects: ["English Language", "Mathematics"] },
    { name: "Grade 12", level: 12, hasStreams: true, defaultSubjects: ["English Language", "Mathematics"] },
]

export const STREAM_SUGGESTIONS = [
    {
        name: "Natural Science",
        code: "NS",
        description: "Focus on sciences and mathematics",
        subjects: ["Physics", "Chemistry", "Biology", "Mathematics"],
    },
    {
        name: "Social Science",
        code: "SS",
        description: "Focus on humanities and social studies",
        subjects: ["History", "Geography", "Psychology", "Business Studies"],
    },
    {
        name: "Arts",
        code: "ART",
        description: "Focus on creative and performing arts",
        subjects: ["Art", "Music", "Drama", "English Language"],
    },
    {
        name: "Technical",
        code: "TECH",
        description: "Focus on technical and vocational skills",
        subjects: ["Computer Science", "Information Technology", "Business Studies"],
    },
]
