import { z } from "zod";

export function pickFields<T extends z.ZodRawShape, K extends keyof T>(
  schema: z.ZodObject<T>,
  fields: readonly K[],
): z.ZodObject<Pick<T, K>> {
  const shape = fields.reduce(
    (acc, key) => {
      acc[key] = schema.shape[key];
      return acc;
    },
    {} as Pick<T, K>,
  );

  return z.object(shape);
}
