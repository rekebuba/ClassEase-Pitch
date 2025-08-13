import { useFormContext } from "react-hook-form";
import {
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from '@/components/ui/form';
import {
    Select,
    SelectContent,
    SelectTrigger,
    SelectValue,
} from '@/components/ui/select';
import { useState } from "react";

type Props<T> = {
    fieldTitle: string;
    nameInSchema: string;
    getObjects: (index: string) => T | T[];
    disabled?: boolean;
    className?: string;
    children?: React.ReactNode;
};

export function SelectForObject<T>({
    fieldTitle,
    nameInSchema,
    getObjects,
    disabled = false,
    className,
    children,
}: Props<T>) {
    const form = useFormContext();
    const defaultValues = form.getValues(nameInSchema) || [];
    const [value, setValue] = useState<string>(defaultValues.length > 0 ? defaultValues.length.toString() : "");

    return (
        <FormField
            control={form.control}
            name={nameInSchema}
            render={() => (
                <FormItem>
                    <FormLabel htmlFor={nameInSchema}>
                        {fieldTitle}
                    </FormLabel>

                    <Select
                        value={value}
                        onValueChange={(val) => {
                            const obj = getObjects(val);
                            form.setValue(nameInSchema, obj, { shouldValidate: true, shouldDirty: true });
                            setValue(val);
                        }}
                        disabled={disabled}
                    >
                        <FormControl>
                            <SelectTrigger id={nameInSchema} className={className}>
                                <SelectValue
                                    placeholder="Choose from suggestions..."
                                />
                            </SelectTrigger>
                        </FormControl>

                        <SelectContent>
                            {children}
                        </SelectContent>
                    </Select>

                    <FormMessage />
                </FormItem>
            )}
        />
    );
}
