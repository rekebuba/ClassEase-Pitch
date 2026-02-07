import { isEqual } from "lodash";
import {
  useFormContext,
  useWatch,
} from "react-hook-form";

import { Checkbox } from "@/components/ui/checkbox";
import {
  FormControl,
  FormField,
  FormItem,
  FormMessage,
} from "@/components/ui/form";

import type {
  FieldValues,
  Path,
  PathValue,
} from "react-hook-form";

type CheckboxWithLabelProps<T extends FieldValues, V> = {
  fieldTitle: string;
  nameInSchema: Path<T>;
  className?: string;
  disabled?: boolean;
  /** If provided, checkbox will act as "toggle in array of objects" mode */
  value?: V;
};

export function CheckboxWithLabel<T extends FieldValues, V>({
  fieldTitle,
  nameInSchema,
  className,
  disabled = false,
  value,
}: CheckboxWithLabelProps<T, V>) {
  const form = useFormContext<T>();
  const control = form.control;

  // Always watch the field to satisfy hook rules
  const watchedValue = useWatch({ control, name: nameInSchema });

  // --- Object toggle mode ---
  const values = value ? watchedValue || [] : undefined;
  const checked
    = value && values
      ? (values as T[]).some((v: T) => isEqual(v, value))
      : undefined;

  const toggle = (isChecked: boolean) => {
    const current = (form.getValues(nameInSchema) as unknown as T[]) || [];

    if (isChecked) {
      // Simply append to the end
      const next = [...current, value!];
      form.setValue(nameInSchema, next as PathValue<T, Path<T>>, {
        shouldValidate: true,
        shouldDirty: true,
      });
    }
    else {
      // Remove the item
      const next = current.filter((item: T) => !isEqual(item, value));
      form.setValue(nameInSchema, next as PathValue<T, Path<T>>, {
        shouldValidate: true,
        shouldDirty: true,
      });
    }
  };

  return (
    <FormField
      control={control}
      name={nameInSchema}
      render={({ field }) => (
        <FormItem className="w-full flex items-center gap-2">
          <div className="flex items-center gap-2">
            <FormControl>
              <Checkbox
                id={nameInSchema}
                {...(!value
                  ? {
                      // Normal boolean checkbox mode
                      ...field,
                      checked: field.value,
                      onCheckedChange: field.onChange,
                    }
                  : {
                      // Object array toggle mode
                      checked,
                      onCheckedChange: toggle,
                    })}
                disabled={disabled}
                className={`disabled:text-blue-500 dark:disabled:text-yellow-300 disabled:opacity-75 ${className}`}
              />
            </FormControl>
            {fieldTitle}
          </div>
          <FormMessage />
        </FormItem>
      )}
    />
  );
}
