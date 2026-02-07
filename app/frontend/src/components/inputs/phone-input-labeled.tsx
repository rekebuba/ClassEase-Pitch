import { useFormContext } from "react-hook-form";

import {
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { PhoneInput } from "@/components/ui/phone-input";

import type { InputHTMLAttributes } from "react";
import type { FieldValues, Path } from "react-hook-form";

type InputWithLabelProps<T extends FieldValues> = {
  fieldTitle: string;
  nameInSchema: Path<T>;
  className?: string;
  description?: string;
} & InputHTMLAttributes<HTMLInputElement>;

export function PhoneInputWithLabel<T extends FieldValues>({
  fieldTitle,
  nameInSchema,
  className,
  description,
}: InputWithLabelProps<T>) {
  const form = useFormContext();

  return (
    <FormField
      control={form.control}
      name={nameInSchema}
      render={({ field }) => (
        <FormItem>
          <FormLabel htmlFor={nameInSchema}>{fieldTitle}</FormLabel>

          <FormControl>
            <PhoneInput
              placeholder="Placeholder"
              {...field}
              defaultCountry="ET"
              className={className}
            />
          </FormControl>
          {form.formState.errors[nameInSchema]
            ? (
                <FormMessage />
              )
            : (
                description && <FormDescription>{description}</FormDescription>
              )}
        </FormItem>
      )}
    />
  );
}
