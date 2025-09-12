import { FieldValues, Path, PathValue, useFormContext } from "react-hook-form";

import {
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";

import {
  Select,
  SelectContent,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { ReactNode, useState } from "react";

type SelectWithLabelProps<T extends FieldValues, V> = {
  fieldTitle: string;
  nameInSchema: Path<T>;
  className?: string;
  children?: ReactNode;
  disabled?: boolean;
  description?: string;
  getObjects?: (index: string) => V | V[];
};

export function SelectWithLabel<T extends FieldValues, V>({
  fieldTitle,
  nameInSchema,
  className,
  children,
  description,
  disabled = false,
  getObjects,
}: SelectWithLabelProps<T, V>) {
  const form = useFormContext<T>();

  // Only needed if getObjects is provided
  const defaultValues = form.getValues(nameInSchema) as
    | PathValue<T, Path<T>>
    | undefined;
  const [value, setValue] = useState<string>(
    Array.isArray(defaultValues) && defaultValues.length > 0
      ? defaultValues.length.toString()
      : "",
  );

  return (
    <FormField
      control={form.control}
      name={nameInSchema}
      render={({ field }) => (
        <FormItem>
          <FormLabel htmlFor={nameInSchema}>{fieldTitle}</FormLabel>

          <Select
            value={getObjects ? value : field.value}
            onValueChange={(val) => {
              if (getObjects) {
                const obj = getObjects(val) as PathValue<T, Path<T>>;
                form.setValue(nameInSchema, obj, {
                  shouldValidate: true,
                  shouldDirty: true,
                });
                setValue(val);
              } else {
                field.onChange(val);
              }
            }}
            disabled={disabled}
          >
            <FormControl>
              <SelectTrigger id={nameInSchema} className={className}>
                <SelectValue placeholder="Choose from suggestions..." />
              </SelectTrigger>
            </FormControl>
            <SelectContent>{children}</SelectContent>
          </Select>
          {form.formState.errors[nameInSchema] ? (
            <FormMessage />
          ) : (
            description && <FormDescription>{description}</FormDescription>
          )}
        </FormItem>
      )}
    />
  );
}
