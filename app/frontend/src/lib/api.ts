import { adminApi, zodApiHandler } from "@/api";
import { z } from "zod";
import { studentSchema } from "@/lib/validations";
import { toast } from "sonner";
import { StudentsData } from "./types";


export const getStudentsData = async (input?): Promise<StudentsData | {}> => {
    const response = await zodApiHandler(
        () => adminApi.getStudents(),
        studentSchema.array(),
    );

    if (!response.success) {
        toast.error(response.error.message, {
            style: { color: "red" },
        });
        throw new Error("Failed to fetch students data");
    }

    
    return response.data;
}
