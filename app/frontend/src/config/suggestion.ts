type SubjectInfo = {
    subject: string;
    code: string;
    grade: string | number;
    stream?: "Natural" | "Social";
};

export const allSubjectsData: SubjectInfo[] = [
    // Grade 1
    { subject: "Arts and Physical Education", code: "ART1", grade: 1 },
    { subject: "Environmental Science", code: "ENV1", grade: 1 },
    { subject: "English", code: "ENG1", grade: 1 },
    { subject: "Mathematics", code: "MAT1", grade: 1 },
    { subject: "Mother Tongue", code: "MOT1", grade: 1 },
    { subject: "Amharic", code: "AMH1", grade: 1 },

    // Grade 2
    { subject: "Arts and Physical Education", code: "ART2", grade: 2 },
    { subject: "Environmental Science", code: "ENV2", grade: 2 },
    { subject: "English", code: "ENG2", grade: 2 },
    { subject: "Mathematics", code: "MAT2", grade: 2 },
    { subject: "Mother Tongue", code: "MOT2", grade: 2 },
    { subject: "Amharic", code: "AMH2", grade: 2 },

    // Grade 3
    { subject: "Arts and Physical Education", code: "ART3", grade: 3 },
    { subject: "Environmental Science", code: "ENV3", grade: 3 },
    { subject: "English", code: "ENG3", grade: 3 },
    { subject: "Mathematics", code: "MAT3", grade: 3 },
    { subject: "Mother Tongue", code: "MOT3", grade: 3 },
    { subject: "Amharic", code: "AMH3", grade: 3 },

    // Grade 4
    { subject: "Arts and Physical Education", code: "ART4", grade: 4 },
    { subject: "Environmental Science", code: "ENV4", grade: 4 },
    { subject: "English", code: "ENG4", grade: 4 },
    { subject: "Mathematics", code: "MAT4", grade: 4 },
    { subject: "Mother Tongue", code: "MOT4", grade: 4 },
    { subject: "Amharic", code: "AMH4", grade: 4 },

    // Grade 5
    { subject: "Integrated Science", code: "INT5", grade: 5 },
    { subject: "Visual Arts and Music", code: "VIS5", grade: 5 },
    { subject: "English", code: "ENG5", grade: 5 },
    { subject: "Mathematics", code: "MAT5", grade: 5 },
    { subject: "Mother Tongue", code: "MOT5", grade: 5 },
    { subject: "Amharic", code: "AMH5", grade: 5 },
    { subject: "Physical Education", code: "PHY5", grade: 5 },
    { subject: "Civics and Ethical Education", code: "CIV5", grade: 5 },

    // Grade 6
    { subject: "Integrated Science", code: "INT6", grade: 6 },
    { subject: "Visual Arts and Music", code: "VIS6", grade: 6 },
    { subject: "English", code: "ENG6", grade: 6 },
    { subject: "Mathematics", code: "MAT6", grade: 6 },
    { subject: "Mother Tongue", code: "MOT6", grade: 6 },
    { subject: "Amharic", code: "AMH6", grade: 6 },
    { subject: "Physical Education", code: "PHY6", grade: 6 },
    { subject: "Civics and Ethical Education", code: "CIV6", grade: 6 },

    // Grade 7
    { subject: "Social Study", code: "SOC7", grade: 7 },
    { subject: "Visual Arts and Music", code: "VIS7", grade: 7 },
    { subject: "English", code: "ENG7", grade: 7 },
    { subject: "Mathematics", code: "MAT7", grade: 7 },
    { subject: "Mother Tongue", code: "MOT7", grade: 7 },
    { subject: "Amharic", code: "AMH7", grade: 7 },
    { subject: "Physical Education", code: "PHY7", grade: 7 },
    { subject: "Civics and Ethical Education", code: "CIV7", grade: 7 },
    { subject: "Biology", code: "BIO7", grade: 7 },
    { subject: "Physics", code: "PHY7", grade: 7 },
    { subject: "Chemistry", code: "CHE7", grade: 7 },

    // Grade 8
    { subject: "Social Study", code: "SOC8", grade: 8 },
    { subject: "Visual Arts and Music", code: "VIS8", grade: 8 },
    { subject: "English", code: "ENG8", grade: 8 },
    { subject: "Mathematics", code: "MAT8", grade: 8 },
    { subject: "Mother Tongue", code: "MOT8", grade: 8 },
    { subject: "Amharic", code: "AMH8", grade: 8 },
    { subject: "Physical Education", code: "PHY8", grade: 8 },
    { subject: "Civics and Ethical Education", code: "CIV8", grade: 8 },
    { subject: "Biology", code: "BIO8", grade: 8 },
    { subject: "Physics", code: "PHY8", grade: 8 },
    { subject: "Chemistry", code: "CHE8", grade: 8 },

    // Grade 9
    { subject: "Amharic as second language", code: "AMH9", grade: 9 },
    { subject: "English", code: "ENG9", grade: 9 },
    { subject: "Mathematics", code: "MAT9", grade: 9 },
    { subject: "Mother Tongue", code: "MOT9", grade: 9 },
    { subject: "Physical Education", code: "PHY9", grade: 9 },
    { subject: "Civics and Ethical Education", code: "CIV9", grade: 9 },
    { subject: "Biology", code: "BIO9", grade: 9 },
    { subject: "Physics", code: "PHY9", grade: 9 },
    { subject: "Chemistry", code: "CHE9", grade: 9 },
    { subject: "Geography", code: "GEO9", grade: 9 },
    { subject: "History", code: "HIS9", grade: 9 },
    { subject: "Information Technology", code: "INF9", grade: 9 },

    // Grade 10
    { subject: "English", code: "ENG10", grade: 10 },
    { subject: "Mathematics", code: "MAT10", grade: 10 },
    { subject: "Mother Tongue", code: "MOT10", grade: 10 },
    { subject: "Amharic", code: "AMH10", grade: 10 },
    { subject: "Physical Education", code: "PHY10", grade: 10 },
    { subject: "Civics and Ethical Education", code: "CIV10", grade: 10 },
    { subject: "Information Technology", code: "INF10", grade: 10 },
    { subject: "Biology", code: "BIO10", grade: 10 },
    { subject: "Physics", code: "PHY10", grade: 10 },
    { subject: "Chemistry", code: "CHE10", grade: 10 },
    { subject: "Geography", code: "GEO10", grade: 10 },
    { subject: "History", code: "HIS10", grade: 10 },

    // Grade 11
    { subject: "Biology", code: "BIO11-N", grade: 11, stream: "Natural" },
    { subject: "Physics", code: "PHY11-N", grade: 11, stream: "Natural" },
    { subject: "Chemistry", code: "CHE11-N", grade: 11, stream: "Natural" },
    { subject: "Geography", code: "GEO11-S", grade: 11, stream: "Social" },
    { subject: "History", code: "HIS11-S", grade: 11, stream: "Social" },
    { subject: "Economics", code: "ECO11-S", grade: 11, stream: "Social" },
    { subject: "Technical Drawing", code: "TEC11-N", grade: 11, stream: "Natural" },
    { subject: "General Business", code: "GEN11-S", grade: 11, stream: "Social" },
    { subject: "English", code: "ENG11", grade: 11 },
    { subject: "Mathematics", code: "MAT11", grade: 11 },
    { subject: "Mother Tongue", code: "MOT11", grade: 11 },
    { subject: "Amharic", code: "AMH11", grade: 11 },
    { subject: "Physical Education", code: "PHY11", grade: 11 },
    { subject: "Civics and Ethical Education", code: "CIV11", grade: 11 },
    { subject: "Information Technology", code: "INF11", grade: 11 },

    // Grade 12
    { subject: "Biology", code: "BIO12-N", grade: 12, stream: "Natural" },
    { subject: "Physics", code: "PHY12-N", grade: 12, stream: "Natural" },
    { subject: "Chemistry", code: "CHE12-N", grade: 12, stream: "Natural" },
    { subject: "Geography", code: "GEO12-S", grade: 12, stream: "Social" },
    { subject: "History", code: "HIS12-S", grade: 12, stream: "Social" },
    { subject: "Economics", code: "ECO12-S", grade: 12, stream: "Social" },
    { subject: "Technical Drawing", code: "TEC12-N", grade: 12, stream: "Natural" },
    { subject: "General Business", code: "GEN12-S", grade: 12, stream: "Social" },
    { subject: "English", code: "ENG12", grade: 12 },
    { subject: "Mathematics", code: "MAT12", grade: 12 },
    { subject: "Mother Tongue", code: "MOT12", grade: 12 },
    { subject: "Amharic", code: "AMH12", grade: 12 },
    { subject: "Physical Education", code: "PHY12", grade: 12 },
    { subject: "Civics and Ethical Education", code: "CIV12", grade: 12 },
    { subject: "Information Technology", code: "INF12", grade: 12 },
];

const getSubjectsByGrade = (grade: number) => {
    return allSubjectsData
        .filter((s) => s.grade === grade)
        .map(({ subject, code, grade, stream }) => ({ subject, code, grade, hasStreams: !!stream, stream }));
};

export const GradeOneSubjects = getSubjectsByGrade(1);
export const GradeTwoSubjects = getSubjectsByGrade(2);
export const GradeThreeSubjects = getSubjectsByGrade(3);
export const GradeFourSubjects = getSubjectsByGrade(4);
export const GradeFiveSubjects = getSubjectsByGrade(5);
export const GradeSixSubjects = getSubjectsByGrade(6);
export const GradeSevenSubjects = getSubjectsByGrade(7);
export const GradeEightSubjects = getSubjectsByGrade(8);
export const GradeNineSubjects = getSubjectsByGrade(9);
export const GradeTenSubjects = getSubjectsByGrade(10);
export const GradeElevenSubjects = getSubjectsByGrade(11);
export const GradeTwelveSubjects = getSubjectsByGrade(12);

export const SocialStreamSubjects = Object.values(
    allSubjectsData.filter((s) => s.stream === "Natural")
        .reduce((acc, { subject, code, grade }) => {
            if (!acc[subject]) {
                acc[subject] = { subject, codes: [], grades: [] };
            }
            acc[subject].codes.push(code);
            acc[subject].grades.push(grade.toString());
            return acc;
        }, {} as Record<string, { subject: string; codes: string[]; grades: string[] }>)
);

export const NaturalStreamSubjects = Object.values(
    allSubjectsData.filter((s) => s.stream === "Natural")
        .reduce((acc, { subject, code, grade }) => {
            if (!acc[subject]) {
                acc[subject] = { subject, codes: [], grades: [] };
            }
            acc[subject].codes.push(code);
            acc[subject].grades.push(grade.toString());
            return acc;
        }, {} as Record<string, { subject: string; codes: string[]; grades: string[] }>)
);

export const AllSubjects = Object.values(
    allSubjectsData.reduce((acc, { subject, code, grade }) => {
        if (!acc[subject]) {
            acc[subject] = { subject, codes: [], grades: [] };
        }
        acc[subject].codes.push(code);
        acc[subject].grades.push(grade.toString());
        return acc;
    }, {} as Record<string, { subject: string; codes: string[]; grades: string[] }>)
);

export const Stream = ["Natural", "Social"];
export const Grade = Array.from({ length: 12 }, (_, i) => (i + 1).toString());
export const Section = ["A", "B", "C"];
