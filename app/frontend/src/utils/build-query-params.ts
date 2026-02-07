import { ZodArray, ZodObject } from "zod";

import type { QueryParams } from "@/lib/types";
import type { ZodTypeAny } from "zod";

function toSnakeCase(str: string): string {
  return str
    .replace(/([a-z0-9])([A-Z])/g, "$1_$2")
    .replace(/([A-Z])([A-Z][a-z])/g, "$1_$2")
    .replace(/[-\s]+/g, "_")
    .replace(/_{2,}/g, "_")
    .toLowerCase();
}

function toSnakeCasePath(str: string): string {
  return str.split(".").map(toSnakeCase).join(".");
}

export function buildQueryParams(schema: ZodTypeAny, options?: QueryParams) {
  const params: Record<string, string> = {};
  if (!options) {
    options = parseZodSchema(schema);
  }

  // Flatten nested fields into fields array
  const fields: string[] = [];

  if (options.fields?.length) {
    fields.push(...options.fields.map(toSnakeCasePath));
  }

  if (options.nestedFields) {
    for (const [key, nested] of Object.entries(options.nestedFields)) {
      const skey = toSnakeCase(key);
      fields.push(...nested.map(f => `${skey}.${toSnakeCase(f)}`));
    }
  }

  if (fields.length) {
    params.fields = fields.join(",");
  }

  if (options.expand?.length) {
    params.expand = options.expand.map(toSnakeCasePath).join(",");
  }

  if (options.params) {
    for (const [key, value] of Object.entries(options.params)) {
      params[key] = String(value);
    }
  }

  return params;
}

// Recursively build query params from Zod schema
function parseZodSchema(
  schema: ZodTypeAny,
  parentKey?: string,
  expand: string[] = [],
  nestedFields: Record<string, string[]> = {},
): {
  fields: string[];
  expand: string[];
  nestedFields: Record<string, string[]>;
} {
  const fields: string[] = [];

  if (schema instanceof ZodArray) {
    return parseZodSchema(schema.element, parentKey, expand, nestedFields);
  }

  if (schema instanceof ZodObject) {
    const shape = schema.shape;
    for (const key of Object.keys(shape)) {
      const subSchema = shape[key];

      // If it's an object or array => treat as relationship
      if (subSchema instanceof ZodObject || subSchema instanceof ZodArray) {
        expand.push(parentKey ? `${parentKey}.${key}` : key);
        const nested = parseZodSchema(subSchema, key, expand, nestedFields);

        // Assign nested fields
        nestedFields[key] = nested.fields;
      }
      else {
        fields.push(key);
      }
    }
  }

  return { fields, expand, nestedFields };
}
