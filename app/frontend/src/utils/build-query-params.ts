import { QueryParams } from "@/lib/types";

export const buildQueryParams = (options?: QueryParams) => {
    // Build URL with query parameters
    const params: Record<string, string> = {};

    if (!options) return params;

    // Add fields
    if (options?.fields?.length) {
        params.fields = options.fields.join(",");
    }

    // Add expands
    if (options?.expand?.length) {
        params.expand = options.expand.join(",");
    }

    // Add nested fields
    if (options?.nestedFields) {
        for (const [key, fields] of Object.entries(options.nestedFields)) {
            params[`${key}_fields`] = fields.join(",");
        }
    }

    // Add additional params
    if (options?.params) {
        for (const [key, value] of Object.entries(options.params)) {
            params[key] = String(value);
        }
    }

    return params;
};
