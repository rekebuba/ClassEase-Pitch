import { z, ZodError } from "zod";
import axios from "axios";
import { ApiHandlerResponse } from "@/lib/types";

/**
 * Handles API calls with Zod validation and error handling
 * @param request - API call function (e.g., axios.get, axios.post)
 * @param schema - Zod schema for validation
 * @param options - Custom error messages or status codes
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

        // Validate response data
        const parsedData = schema.parse(response.data);

        return {
            success: true,
            data: parsedData,
        };

    } catch (error) {
        // Zod validation error
        if (error instanceof ZodError) {
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
            return {
                success: false,
                error: {
                    type: "api",
                    status: error.response?.status || 500,
                    message:
                        options?.apiErrorMsg ||
                        error.response?.data?.message ||
                        error.message ||
                        "API request failed",
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
