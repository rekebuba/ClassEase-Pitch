import { FieldValues, Path, useFormContext } from "react-hook-form";

import {
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";

type RadioGroupWithLabelProps<T extends FieldValues, K extends string> = {
  fieldTitle: string;
  nameInSchema: Path<T>;
  className?: string;
  options: { label: string; value: K }[];
};

export function RadioGroupLabel<T extends FieldValues, K extends string>({
  fieldTitle,
  nameInSchema,
  className,
  options,
}: RadioGroupWithLabelProps<T, K>) {
  const form = useFormContext();

  return (
    <FormField
      control={form.control}
      name={nameInSchema}
      render={({ field }) => (
        <FormItem>
          <FormLabel>{fieldTitle}</FormLabel>

          <FormControl>
            <RadioGroup
              onValueChange={field.onChange}
              value={field.value}
              className={`flex gap-4 ${className}`}
            >
              {options.map((option) => (
                <FormItem key={option.value}>
                  <FormControl>
                    <div className="flex items-center space-x-2">
                      <RadioGroupItem value={option.value} id={option.value} />
                      <FormLabel
                        htmlFor={option.value}
                        className="font-normal items-center justify-between"
                      >
                        {option.label}
                      </FormLabel>
                    </div>
                  </FormControl>
                </FormItem>
              ))}
            </RadioGroup>
          </FormControl>

          <FormMessage />
        </FormItem>
      )}
    />
  );
}
