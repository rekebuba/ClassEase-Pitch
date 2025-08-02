export interface Grade {
    id: string
    name: string
    level: string | number
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
]
