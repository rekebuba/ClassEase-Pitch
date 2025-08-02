type SubjectInfo = {
    name: string;
    code: string;
    grade: string | number;
    stream?: "Natural" | "Social";
};

export const allSubjectsData: SubjectInfo[] = [
    // Grade 1
    { name: "Arts and Physical Education", code: "ART1", grade: 1 },
    { name: "Environmental Science", code: "ENV1", grade: 1 },
    { name: "English", code: "ENG1", grade: 1 },
    { name: "Mathematics", code: "MAT1", grade: 1 },
    { name: "Mother Tongue", code: "MOT1", grade: 1 },
    { name: "Amharic", code: "AMH1", grade: 1 },

    // Grade 2
    { name: "Arts and Physical Education", code: "ART2", grade: 2 },
    { name: "Environmental Science", code: "ENV2", grade: 2 },
    { name: "English", code: "ENG2", grade: 2 },
    { name: "Mathematics", code: "MAT2", grade: 2 },
    { name: "Mother Tongue", code: "MOT2", grade: 2 },
    { name: "Amharic", code: "AMH2", grade: 2 },

    // Grade 3
    { name: "Arts and Physical Education", code: "ART3", grade: 3 },
    { name: "Environmental Science", code: "ENV3", grade: 3 },
    { name: "English", code: "ENG3", grade: 3 },
    { name: "Mathematics", code: "MAT3", grade: 3 },
    { name: "Mother Tongue", code: "MOT3", grade: 3 },
    { name: "Amharic", code: "AMH3", grade: 3 },

    // Grade 4
    { name: "Arts and Physical Education", code: "ART4", grade: 4 },
    { name: "Environmental Science", code: "ENV4", grade: 4 },
    { name: "English", code: "ENG4", grade: 4 },
    { name: "Mathematics", code: "MAT4", grade: 4 },
    { name: "Mother Tongue", code: "MOT4", grade: 4 },
    { name: "Amharic", code: "AMH4", grade: 4 },

    // Grade 5
    { name: "Integrated Science", code: "INT5", grade: 5 },
    { name: "Visual Arts and Music", code: "VIS5", grade: 5 },
    { name: "English", code: "ENG5", grade: 5 },
    { name: "Mathematics", code: "MAT5", grade: 5 },
    { name: "Mother Tongue", code: "MOT5", grade: 5 },
    { name: "Amharic", code: "AMH5", grade: 5 },
    { name: "Physical Education", code: "PHY5", grade: 5 },
    { name: "Civics and Ethical Education", code: "CIV5", grade: 5 },

    // Grade 6
    { name: "Integrated Science", code: "INT6", grade: 6 },
    { name: "Visual Arts and Music", code: "VIS6", grade: 6 },
    { name: "English", code: "ENG6", grade: 6 },
    { name: "Mathematics", code: "MAT6", grade: 6 },
    { name: "Mother Tongue", code: "MOT6", grade: 6 },
    { name: "Amharic", code: "AMH6", grade: 6 },
    { name: "Physical Education", code: "PHY6", grade: 6 },
    { name: "Civics and Ethical Education", code: "CIV6", grade: 6 },

    // Grade 7
    { name: "Social Study", code: "SOC7", grade: 7 },
    { name: "Visual Arts and Music", code: "VIS7", grade: 7 },
    { name: "English", code: "ENG7", grade: 7 },
    { name: "Mathematics", code: "MAT7", grade: 7 },
    { name: "Mother Tongue", code: "MOT7", grade: 7 },
    { name: "Amharic", code: "AMH7", grade: 7 },
    { name: "Physical Education", code: "PHY7", grade: 7 },
    { name: "Civics and Ethical Education", code: "CIV7", grade: 7 },
    { name: "Biology", code: "BIO7", grade: 7 },
    { name: "Physics", code: "PHY7", grade: 7 },
    { name: "Chemistry", code: "CHE7", grade: 7 },

    // Grade 8
    { name: "Social Study", code: "SOC8", grade: 8 },
    { name: "Visual Arts and Music", code: "VIS8", grade: 8 },
    { name: "English", code: "ENG8", grade: 8 },
    { name: "Mathematics", code: "MAT8", grade: 8 },
    { name: "Mother Tongue", code: "MOT8", grade: 8 },
    { name: "Amharic", code: "AMH8", grade: 8 },
    { name: "Physical Education", code: "PHY8", grade: 8 },
    { name: "Civics and Ethical Education", code: "CIV8", grade: 8 },
    { name: "Biology", code: "BIO8", grade: 8 },
    { name: "Physics", code: "PHY8", grade: 8 },
    { name: "Chemistry", code: "CHE8", grade: 8 },

    // Grade 9
    { name: "Amharic as second language", code: "AMH9", grade: 9 },
    { name: "English", code: "ENG9", grade: 9 },
    { name: "Mathematics", code: "MAT9", grade: 9 },
    { name: "Mother Tongue", code: "MOT9", grade: 9 },
    { name: "Physical Education", code: "PHY9", grade: 9 },
    { name: "Civics and Ethical Education", code: "CIV9", grade: 9 },
    { name: "Biology", code: "BIO9", grade: 9 },
    { name: "Physics", code: "PHY9", grade: 9 },
    { name: "Chemistry", code: "CHE9", grade: 9 },
    { name: "Geography", code: "GEO9", grade: 9 },
    { name: "History", code: "HIS9", grade: 9 },
    { name: "Information Technology", code: "INF9", grade: 9 },

    // Grade 10
    { name: "English", code: "ENG10", grade: 10 },
    { name: "Mathematics", code: "MAT10", grade: 10 },
    { name: "Mother Tongue", code: "MOT10", grade: 10 },
    { name: "Amharic", code: "AMH10", grade: 10 },
    { name: "Physical Education", code: "PHY10", grade: 10 },
    { name: "Civics and Ethical Education", code: "CIV10", grade: 10 },
    { name: "Information Technology", code: "INF10", grade: 10 },
    { name: "Biology", code: "BIO10", grade: 10 },
    { name: "Physics", code: "PHY10", grade: 10 },
    { name: "Chemistry", code: "CHE10", grade: 10 },
    { name: "Geography", code: "GEO10", grade: 10 },
    { name: "History", code: "HIS10", grade: 10 },

    // Grade 11
    { name: "Biology", code: "BIO11-N", grade: 11, stream: "Natural" },
    { name: "Physics", code: "PHY11-N", grade: 11, stream: "Natural" },
    { name: "Chemistry", code: "CHE11-N", grade: 11, stream: "Natural" },
    { name: "Geography", code: "GEO11-S", grade: 11, stream: "Social" },
    { name: "History", code: "HIS11-S", grade: 11, stream: "Social" },
    { name: "Economics", code: "ECO11-S", grade: 11, stream: "Social" },
    { name: "Technical Drawing", code: "TEC11-N", grade: 11, stream: "Natural" },
    { name: "General Business", code: "GEN11-S", grade: 11, stream: "Social" },
    { name: "English", code: "ENG11", grade: 11 },
    { name: "Mathematics", code: "MAT11", grade: 11 },
    { name: "Mother Tongue", code: "MOT11", grade: 11 },
    { name: "Amharic", code: "AMH11", grade: 11 },
    { name: "Physical Education", code: "PHY11", grade: 11 },
    { name: "Civics and Ethical Education", code: "CIV11", grade: 11 },
    { name: "Information Technology", code: "INF11", grade: 11 },

    // Grade 12
    { name: "Biology", code: "BIO12-N", grade: 12, stream: "Natural" },
    { name: "Physics", code: "PHY12-N", grade: 12, stream: "Natural" },
    { name: "Chemistry", code: "CHE12-N", grade: 12, stream: "Natural" },
    { name: "Geography", code: "GEO12-S", grade: 12, stream: "Social" },
    { name: "History", code: "HIS12-S", grade: 12, stream: "Social" },
    { name: "Economics", code: "ECO12-S", grade: 12, stream: "Social" },
    { name: "Technical Drawing", code: "TEC12-N", grade: 12, stream: "Natural" },
    { name: "General Business", code: "GEN12-S", grade: 12, stream: "Social" },
    { name: "English", code: "ENG12", grade: 12 },
    { name: "Mathematics", code: "MAT12", grade: 12 },
    { name: "Mother Tongue", code: "MOT12", grade: 12 },
    { name: "Amharic", code: "AMH12", grade: 12 },
    { name: "Physical Education", code: "PHY12", grade: 12 },
    { name: "Civics and Ethical Education", code: "CIV12", grade: 12 },
    { name: "Information Technology", code: "INF12", grade: 12 },
];

const getSubjectsByGrade = (grade: number) => {
    return allSubjectsData
        .filter((s) => s.grade === grade)
        .map(({ name, code, grade, stream }) => ({ name, code, grade, hasStreams: !!stream, stream }));
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
        .reduce((acc, { name, code, grade }) => {
            if (!acc[name]) {
                acc[name] = { name, codes: [], grades: [] };
            }
            acc[name].codes.push(code);
            acc[name].grades.push(grade.toString());
            return acc;
        }, {} as Record<string, { name: string; codes: string[]; grades: string[] }>)
);

export const NaturalStreamSubjects = Object.values(
    allSubjectsData.filter((s) => s.stream === "Natural")
        .reduce((acc, { name, code, grade }) => {
            if (!acc[name]) {
                acc[name] = { name, codes: [], grades: [] };
            }
            acc[name].codes.push(code);
            acc[name].grades.push(grade.toString());
            return acc;
        }, {} as Record<string, { name: string; codes: string[]; grades: string[] }>)
);

export const allSubjects = Object.values(
    allSubjectsData.reduce((acc, { name, code, grade }) => {
        if (!acc[name]) {
            acc[name] = { id: crypto.randomUUID(), name, code };
        }
        return acc;
    }, {} as Record<string, { id: string, name: string; code: string; }>)
);

export const Stream = ["Natural", "Social"];
export const Grade = Array.from({ length: 12 }, (_, i) => (i + 1).toString());
export const Section = ["A", "B", "C"];
