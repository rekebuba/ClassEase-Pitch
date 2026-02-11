import { useFormContext } from "react-hook-form";

import {
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";

import type { InputHTMLAttributes } from "react";
import type { FieldValues, Path } from "react-hook-form";

type InputWithLabelProps<T extends FieldValues> = {
  fieldTitle?: string;
  nameInSchema: Path<T>;
  className?: string;
  description?: string;
} & InputHTMLAttributes<HTMLInputElement>;

export function InputWithLabel<T extends FieldValues>({
  fieldTitle,
  nameInSchema,
  className,
  description,
  ...props
}: InputWithLabelProps<T>) {
  const form = useFormContext<T>();

  return (
    <FormField
      control={form.control}
      name={nameInSchema}
      render={({ field }) => (
        <FormItem>
          {fieldTitle && (
            <FormLabel htmlFor={nameInSchema}>
              {fieldTitle}
            </FormLabel>
          )}

          <FormControl>
            <Input
              id={nameInSchema}
              className={cn(
                "disabled:text-blue-500 dark:disabled:text-yellow-300 disabled:opacity-75",
                className,
              )}
              {...props}
              {...field}
              onChange={(e) => {
                const value
                  = props.type === "number"
                    ? e.target.value === ""
                      ? undefined
                      : +e.target.value
                    : e.target.value;

                field.onChange(value);
              }}
            />
          </FormControl>

          {description && !form.getFieldState(nameInSchema).error && (
            <FormDescription>{description}</FormDescription>
          )}

          <FormMessage />
        </FormItem>
      )}
    />
  );
}
