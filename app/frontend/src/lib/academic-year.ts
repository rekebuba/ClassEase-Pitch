import { AllSubjects, allSubjectsData, GradeOneSubjects } from "@/config/suggestion"

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
    code: string[]
    grades: string[]
}

export interface Term {
    id: string
    name: string
    startDate: string
    endDate: string
    order: number
}



type Suggestion = {
    name: string;
    level: string;
    hasStreams: boolean;
    defaultSubjects: string[];
};

export const GRADE_SUGGESTIONS: Suggestion[] = Object.values(
    allSubjectsData.reduce((acc, subject) => {
        const gradeKey = subject.grade.toString();

        if (!acc[gradeKey]) {
            acc[gradeKey] = {
                name: `Grade ${subject.grade}`,
                level: gradeKey,
                hasStreams: false,
                defaultSubjects: [],
            };
        }

        if (subject.stream) {
            acc[gradeKey].hasStreams = true;
        } else {
            acc[gradeKey].defaultSubjects.push(subject.subject);
        }

        return acc;
    }, {} as Record<string, Suggestion>)
);


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
