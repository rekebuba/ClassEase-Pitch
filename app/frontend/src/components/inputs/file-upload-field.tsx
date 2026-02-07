import { useFormContext } from "react-hook-form";
import { toast } from "sonner";

import {
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import {
  Dropzone,
  DropzoneContent,
  DropzoneEmptyState,
} from "@/components/ui/shadcn-io/dropzone";

import type { FieldValues, Path } from "react-hook-form";

type FileUploadFieldProps<T extends FieldValues> = {
  fieldTitle: string;
  nameInSchema: Path<T>;
  description?: string;
} & Omit<React.ComponentProps<typeof Dropzone>, "onDrop" | "src">;

export function FileUploadField<T extends FieldValues>({
  fieldTitle,
  nameInSchema,
  description,
  ...dropzoneProps
}: FileUploadFieldProps<T>) {
  const form = useFormContext<T>();

  return (
    <FormField
      control={form.control}
      name={nameInSchema}
      render={({ field }) => (
        <FormItem>
          <FormLabel htmlFor={nameInSchema}>{fieldTitle}</FormLabel>

          <FormControl>
            <Dropzone
              {...dropzoneProps}
              src={field.value as File[] | undefined}
              onDrop={files => field.onChange(files)}
              onError={message => toast.error(message.message)}
            >
              <DropzoneEmptyState />
              <DropzoneContent />
            </Dropzone>
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
