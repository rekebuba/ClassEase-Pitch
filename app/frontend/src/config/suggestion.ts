import type { GradeLevelType } from "@/lib/enums";

type SubjectInfo = {
  id: string;
  name: string;
  code: string;
  grade: string | number;
  stream?: "Natural Science" | "Social Science";
};

export const allSubjectsData: SubjectInfo[] = [
  // Grade 1
  {
    id: crypto.randomUUID(),
    name: "Arts and Physical Education",
    code: "ART1",
    grade: 1,
  },
  {
    id: crypto.randomUUID(),
    name: "Environmental Science",
    code: "ENV1",
    grade: 1,
  },
  { id: crypto.randomUUID(), name: "English", code: "ENG1", grade: 1 },
  { id: crypto.randomUUID(), name: "Mathematics", code: "MAT1", grade: 1 },
  { id: crypto.randomUUID(), name: "Mother Tongue", code: "MOT1", grade: 1 },
  { id: crypto.randomUUID(), name: "Amharic", code: "AMH1", grade: 1 },

  // Grade 2
  {
    id: crypto.randomUUID(),
    name: "Arts and Physical Education",
    code: "ART2",
    grade: 2,
  },
  {
    id: crypto.randomUUID(),
    name: "Environmental Science",
    code: "ENV2",
    grade: 2,
  },
  { id: crypto.randomUUID(), name: "English", code: "ENG2", grade: 2 },
  { id: crypto.randomUUID(), name: "Mathematics", code: "MAT2", grade: 2 },
  { id: crypto.randomUUID(), name: "Mother Tongue", code: "MOT2", grade: 2 },
  { id: crypto.randomUUID(), name: "Amharic", code: "AMH2", grade: 2 },

  // Grade 3
  {
    id: crypto.randomUUID(),
    name: "Arts and Physical Education",
    code: "ART3",
    grade: 3,
  },
  {
    id: crypto.randomUUID(),
    name: "Environmental Science",
    code: "ENV3",
    grade: 3,
  },
  { id: crypto.randomUUID(), name: "English", code: "ENG3", grade: 3 },
  { id: crypto.randomUUID(), name: "Mathematics", code: "MAT3", grade: 3 },
  { id: crypto.randomUUID(), name: "Mother Tongue", code: "MOT3", grade: 3 },
  { id: crypto.randomUUID(), name: "Amharic", code: "AMH3", grade: 3 },

  // Grade 4
  {
    id: crypto.randomUUID(),
    name: "Arts and Physical Education",
    code: "ART4",
    grade: 4,
  },
  {
    id: crypto.randomUUID(),
    name: "Environmental Science",
    code: "ENV4",
    grade: 4,
  },
  { id: crypto.randomUUID(), name: "English", code: "ENG4", grade: 4 },
  { id: crypto.randomUUID(), name: "Mathematics", code: "MAT4", grade: 4 },
  { id: crypto.randomUUID(), name: "Mother Tongue", code: "MOT4", grade: 4 },
  { id: crypto.randomUUID(), name: "Amharic", code: "AMH4", grade: 4 },

  // Grade 5
  {
    id: crypto.randomUUID(),
    name: "Integrated Science",
    code: "INT5",
    grade: 5,
  },
  {
    id: crypto.randomUUID(),
    name: "Visual Arts and Music",
    code: "VIS5",
    grade: 5,
  },
  { id: crypto.randomUUID(), name: "English", code: "ENG5", grade: 5 },
  { id: crypto.randomUUID(), name: "Mathematics", code: "MAT5", grade: 5 },
  { id: crypto.randomUUID(), name: "Mother Tongue", code: "MOT5", grade: 5 },
  { id: crypto.randomUUID(), name: "Amharic", code: "AMH5", grade: 5 },
  {
    id: crypto.randomUUID(),
    name: "Physical Education",
    code: "PHY5",
    grade: 5,
  },
  {
    id: crypto.randomUUID(),
    name: "Civics and Ethical Education",
    code: "CIV5",
    grade: 5,
  },

  // Grade 6
  {
    id: crypto.randomUUID(),
    name: "Integrated Science",
    code: "INT6",
    grade: 6,
  },
  {
    id: crypto.randomUUID(),
    name: "Visual Arts and Music",
    code: "VIS6",
    grade: 6,
  },
  { id: crypto.randomUUID(), name: "English", code: "ENG6", grade: 6 },
  { id: crypto.randomUUID(), name: "Mathematics", code: "MAT6", grade: 6 },
  { id: crypto.randomUUID(), name: "Mother Tongue", code: "MOT6", grade: 6 },
  { id: crypto.randomUUID(), name: "Amharic", code: "AMH6", grade: 6 },
  {
    id: crypto.randomUUID(),
    name: "Physical Education",
    code: "PHY6",
    grade: 6,
  },
  {
    id: crypto.randomUUID(),
    name: "Civics and Ethical Education",
    code: "CIV6",
    grade: 6,
  },

  // Grade 7
  { id: crypto.randomUUID(), name: "Social Study", code: "SOC7", grade: 7 },
  {
    id: crypto.randomUUID(),
    name: "Visual Arts and Music",
    code: "VIS7",
    grade: 7,
  },
  { id: crypto.randomUUID(), name: "English", code: "ENG7", grade: 7 },
  { id: crypto.randomUUID(), name: "Mathematics", code: "MAT7", grade: 7 },
  { id: crypto.randomUUID(), name: "Mother Tongue", code: "MOT7", grade: 7 },
  { id: crypto.randomUUID(), name: "Amharic", code: "AMH7", grade: 7 },
  {
    id: crypto.randomUUID(),
    name: "Physical Education",
    code: "PHY7",
    grade: 7,
  },
  {
    id: crypto.randomUUID(),
    name: "Civics and Ethical Education",
    code: "CIV7",
    grade: 7,
  },
  { id: crypto.randomUUID(), name: "Biology", code: "BIO7", grade: 7 },
  { id: crypto.randomUUID(), name: "Physics", code: "PHY7", grade: 7 },
  { id: crypto.randomUUID(), name: "Chemistry", code: "CHE7", grade: 7 },

  // Grade 8
  { id: crypto.randomUUID(), name: "Social Study", code: "SOC8", grade: 8 },
  {
    id: crypto.randomUUID(),
    name: "Visual Arts and Music",
    code: "VIS8",
    grade: 8,
  },
  { id: crypto.randomUUID(), name: "English", code: "ENG8", grade: 8 },
  { id: crypto.randomUUID(), name: "Mathematics", code: "MAT8", grade: 8 },
  { id: crypto.randomUUID(), name: "Mother Tongue", code: "MOT8", grade: 8 },
  { id: crypto.randomUUID(), name: "Amharic", code: "AMH8", grade: 8 },
  {
    id: crypto.randomUUID(),
    name: "Physical Education",
    code: "PHY8",
    grade: 8,
  },
  {
    id: crypto.randomUUID(),
    name: "Civics and Ethical Education",
    code: "CIV8",
    grade: 8,
  },
  { id: crypto.randomUUID(), name: "Biology", code: "BIO8", grade: 8 },
  { id: crypto.randomUUID(), name: "Physics", code: "PHY8", grade: 8 },
  { id: crypto.randomUUID(), name: "Chemistry", code: "CHE8", grade: 8 },

  // Grade 9
  {
    id: crypto.randomUUID(),
    name: "Amharic as second language",
    code: "AMH9",
    grade: 9,
  },
  { id: crypto.randomUUID(), name: "English", code: "ENG9", grade: 9 },
  { id: crypto.randomUUID(), name: "Mathematics", code: "MAT9", grade: 9 },
  { id: crypto.randomUUID(), name: "Mother Tongue", code: "MOT9", grade: 9 },
  {
    id: crypto.randomUUID(),
    name: "Physical Education",
    code: "PHY9",
    grade: 9,
  },
  {
    id: crypto.randomUUID(),
    name: "Civics and Ethical Education",
    code: "CIV9",
    grade: 9,
  },
  { id: crypto.randomUUID(), name: "Biology", code: "BIO9", grade: 9 },
  { id: crypto.randomUUID(), name: "Physics", code: "PHY9", grade: 9 },
  { id: crypto.randomUUID(), name: "Chemistry", code: "CHE9", grade: 9 },
  { id: crypto.randomUUID(), name: "Geography", code: "GEO9", grade: 9 },
  { id: crypto.randomUUID(), name: "History", code: "HIS9", grade: 9 },
  {
    id: crypto.randomUUID(),
    name: "Information Technology",
    code: "INF9",
    grade: 9,
  },

  // Grade 10
  { id: crypto.randomUUID(), name: "English", code: "ENG10", grade: 10 },
  { id: crypto.randomUUID(), name: "Mathematics", code: "MAT10", grade: 10 },
  { id: crypto.randomUUID(), name: "Mother Tongue", code: "MOT10", grade: 10 },
  { id: crypto.randomUUID(), name: "Amharic", code: "AMH10", grade: 10 },
  {
    id: crypto.randomUUID(),
    name: "Physical Education",
    code: "PHY10",
    grade: 10,
  },
  {
    id: crypto.randomUUID(),
    name: "Civics and Ethical Education",
    code: "CIV10",
    grade: 10,
  },
  {
    id: crypto.randomUUID(),
    name: "Information Technology",
    code: "INF10",
    grade: 10,
  },
  { id: crypto.randomUUID(), name: "Biology", code: "BIO10", grade: 10 },
  { id: crypto.randomUUID(), name: "Physics", code: "PHY10", grade: 10 },
  { id: crypto.randomUUID(), name: "Chemistry", code: "CHE10", grade: 10 },
  { id: crypto.randomUUID(), name: "Geography", code: "GEO10", grade: 10 },
  { id: crypto.randomUUID(), name: "History", code: "HIS10", grade: 10 },

  // Grade 11
  {
    id: crypto.randomUUID(),
    name: "Biology",
    code: "BIO11-N",
    grade: 11,
    stream: "Natural Science",
  },
  {
    id: crypto.randomUUID(),
    name: "Physics",
    code: "PHY11-N",
    grade: 11,
    stream: "Natural Science",
  },
  {
    id: crypto.randomUUID(),
    name: "Chemistry",
    code: "CHE11-N",
    grade: 11,
    stream: "Natural Science",
  },
  {
    id: crypto.randomUUID(),
    name: "Geography",
    code: "GEO11-S",
    grade: 11,
    stream: "Social Science",
  },
  {
    id: crypto.randomUUID(),
    name: "History",
    code: "HIS11-S",
    grade: 11,
    stream: "Social Science",
  },
  {
    id: crypto.randomUUID(),
    name: "Economics",
    code: "ECO11-S",
    grade: 11,
    stream: "Social Science",
  },
  {
    id: crypto.randomUUID(),
    name: "Technical Drawing",
    code: "TEC11-N",
    grade: 11,
    stream: "Natural Science",
  },
  {
    id: crypto.randomUUID(),
    name: "General Business",
    code: "GEN11-S",
    grade: 11,
    stream: "Social Science",
  },
  { id: crypto.randomUUID(), name: "English", code: "ENG11", grade: 11 },
  { id: crypto.randomUUID(), name: "Mathematics", code: "MAT11", grade: 11 },
  { id: crypto.randomUUID(), name: "Mother Tongue", code: "MOT11", grade: 11 },
  { id: crypto.randomUUID(), name: "Amharic", code: "AMH11", grade: 11 },
  {
    id: crypto.randomUUID(),
    name: "Physical Education",
    code: "PHY11",
    grade: 11,
  },
  {
    id: crypto.randomUUID(),
    name: "Civics and Ethical Education",
    code: "CIV11",
    grade: 11,
  },
  {
    id: crypto.randomUUID(),
    name: "Information Technology",
    code: "INF11",
    grade: 11,
  },

  // Grade 12
  {
    id: crypto.randomUUID(),
    name: "Biology",
    code: "BIO12-N",
    grade: 12,
    stream: "Natural Science",
  },
  {
    id: crypto.randomUUID(),
    name: "Physics",
    code: "PHY12-N",
    grade: 12,
    stream: "Natural Science",
  },
  {
    id: crypto.randomUUID(),
    name: "Chemistry",
    code: "CHE12-N",
    grade: 12,
    stream: "Natural Science",
  },
  {
    id: crypto.randomUUID(),
    name: "Geography",
    code: "GEO12-S",
    grade: 12,
    stream: "Social Science",
  },
  {
    id: crypto.randomUUID(),
    name: "History",
    code: "HIS12-S",
    grade: 12,
    stream: "Social Science",
  },
  {
    id: crypto.randomUUID(),
    name: "Economics",
    code: "ECO12-S",
    grade: 12,
    stream: "Social Science",
  },
  {
    id: crypto.randomUUID(),
    name: "Technical Drawing",
    code: "TEC12-N",
    grade: 12,
    stream: "Natural Science",
  },
  {
    id: crypto.randomUUID(),
    name: "General Business",
    code: "GEN12-S",
    grade: 12,
    stream: "Social Science",
  },
  { id: crypto.randomUUID(), name: "English", code: "ENG12", grade: 12 },
  { id: crypto.randomUUID(), name: "Mathematics", code: "MAT12", grade: 12 },
  { id: crypto.randomUUID(), name: "Mother Tongue", code: "MOT12", grade: 12 },
  { id: crypto.randomUUID(), name: "Amharic", code: "AMH12", grade: 12 },
  {
    id: crypto.randomUUID(),
    name: "Physical Education",
    code: "PHY12",
    grade: 12,
  },
  {
    id: crypto.randomUUID(),
    name: "Civics and Ethical Education",
    code: "CIV12",
    grade: 12,
  },
  {
    id: crypto.randomUUID(),
    name: "Information Technology",
    code: "INF12",
    grade: 12,
  },
];

export function getSubjectsByGrade(grade: number) {
  return allSubjectsData
    .filter(s => s.grade === grade)
    .map(({ id, name, code }) => ({ id, name, code }));
}

function getSubjectsForStream(grade: number, stream: "Natural Science" | "Social Science") {
  return allSubjectsData
    .filter(s => s.grade === grade && s.stream === stream)
    .map(({ id, name, code }) => ({ id, name, code }));
}

export function getStreamsByGrade(grade: number) {
  if (grade < 11) {
    return [];
  }
  // For grades 11 and 12, return the streams
  const allSubjects = getSubjectsByGrade(grade);
  if (allSubjects.length === 0) {
    return [];
  }

  const gradeSubjects = getSubjectsByGrade(grade);

  return ["Natural Science", "Social Science"].map(stream => ({
    id: crypto.randomUUID(),
    gradeId: "",
    name: stream,
    subjects: gradeSubjects.filter(
      gradeSubj =>
        !getSubjectsForStream(
          grade,
          stream as "Natural Science" | "Social Science",
        ).some(streamSubj => streamSubj.id === gradeSubj.id),
    ),
  }));
}

export function hasStreamByGrade(grade: number) {
  // Only grades 11 and 12 have streams
  return grade >= 11;
}

export function getDefaultSections() {
  return [
    { id: crypto.randomUUID(), gradeId: "", section: "A" },
    { id: crypto.randomUUID(), gradeId: "", section: "B" },
    { id: crypto.randomUUID(), gradeId: "", section: "C" },
  ];
}

export function getGradeLevel(grade: number): GradeLevelType {
  if (grade >= 1 && grade <= 5) {
    return "primary";
  }
  else if (grade >= 6 && grade <= 8) {
    return "middle school";
  }
  else {
    return "high school";
  }
}

export const SocialStreamSubjects = Object.values(
  allSubjectsData
    .filter(s => s.stream === "Natural Science")
    .reduce(
      (acc, { name, code, grade }) => {
        if (!acc[name]) {
          acc[name] = { name, codes: [], grades: [] };
        }
        acc[name].codes.push(code);
        acc[name].grades.push(grade.toString());
        return acc;
      },
      {} as Record<string, { name: string; codes: string[]; grades: string[] }>,
    ),
);

export const NaturalStreamSubjects = Object.values(
  allSubjectsData
    .filter(s => s.stream === "Natural Science")
    .reduce(
      (acc, { name, code, grade }) => {
        if (!acc[name]) {
          acc[name] = { name, codes: [], grades: [] };
        }
        acc[name].codes.push(code);
        acc[name].grades.push(grade.toString());
        return acc;
      },
      {} as Record<string, { name: string; codes: string[]; grades: string[] }>,
    ),
);

export const allSubjects = Object.values(
  allSubjectsData.reduce(
    (acc, { id, name, code }) => {
      if (!acc[name]) {
        acc[name] = { id, name, code };
      }
      return acc;
    },
    {} as Record<string, { id: string; name: string; code: string }>,
  ),
);

export const Stream = ["Natural", "Social"];
export const Grade = Array.from({ length: 12 }, (_, i) => (i + 1).toString());
export const Section = ["A", "B", "C"];
