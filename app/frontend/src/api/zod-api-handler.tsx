import { z, ZodError, ZodTypeAny } from "zod";
import axios from "axios";
import { ApiHandlerResponse } from "@/lib/types";

export const MetaSchema = z.record(z.any()).optional();
export const LinksSchema = z.record(z.any()).optional();

export function createSuccessResponseSchema<T extends ZodTypeAny>(dataSchema: T) {
    return z.object({
        message: z.string().default("Success"),
        data: dataSchema,
        meta: MetaSchema,
        links: LinksSchema,
    });
}


/**
 * Enhanced API handler with URLSearchParams support
 * @param endpoint - API endpoint URL
 * @param schema - Zod schema for response validation
 * @param options - Field selection, expansion, and error handling
 */
export async function zodApiHandler<T>(
    request: () => Promise<any>,
    schema: z.ZodSchema<T>,
    options?: {
        validationErrorMsg?: string;
        apiErrorMsg?: string;
    }
): Promise<ApiHandlerResponse<T>> {
    try {
        // Execute API request
        const response = await request();

        const responseSchema = createSuccessResponseSchema(schema);
        // Validate response data
        const parsedResult = responseSchema.safeParse(response.data);

        if (!parsedResult.success) {
            throw new ZodError(parsedResult.error.errors);
        }

        if (!parsedResult.data || !parsedResult.data.data) {
            throw new Error("Data is missing in the parsed result");
        }

        return {
            success: true,
            data: parsedResult.data.data,
        };

    } catch (error) {
        // Zod validation error
        if (error instanceof ZodError) {
            console.dir(error.format(), { depth: null });
            return {
                success: false,
                error: {
                    type: "validation",
                    status: 422, // HTTP 422 Unprocessable Entity
                    message: options?.validationErrorMsg || "Validation failed",
                    details: error.flatten(), // User-friendly error format
                },
            };
        }

        // Axios API error
        if (axios.isAxiosError(error)) {
            const message = options?.apiErrorMsg ||
                error.response?.data?.message ||
                error.message ||
                "API request failed"
            return {
                success: false,
                error: {
                    type: "api",
                    status: error.response?.status || 500,
                    message: message,
                    details: error.response?.data,
                },
            };
        }

        // Network or unknown errors
        return {
            success: false,
            error: {
                type: "unknown",
                status: 500,
                message: "An unknown error occurred",
                details: error instanceof Error ? error.message : String(error),
            },
        };
    }
}
