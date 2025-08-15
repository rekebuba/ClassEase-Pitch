import { FieldValues, Path, useFormContext } from "react-hook-form"

import {
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from '@/components/ui/form'
import { Switch } from '@/components/ui/switch'


type SwitchWithLabelProps<T extends FieldValues> = {
    fieldTitle: string,
    nameInSchema: Path<T>,
    className?: string,
}

export function SwitchWithLabel<T extends FieldValues>({
    fieldTitle, nameInSchema, className, ...props
}: SwitchWithLabelProps<T>) {
    const form = useFormContext()

    return (
        <FormField
            control={form.control}
            name={nameInSchema}
            render={({ field }) => (
                <FormItem>
                    <FormLabel
                        htmlFor={nameInSchema}
                    >
                        {fieldTitle}
                    </FormLabel>

                    <FormControl>
                        <Switch
                            id={nameInSchema}
                            className={`disabled:text-blue-500 dark:disabled:text-yellow-300 disabled:opacity-75 ${className}`}
                            {...props}
                            {...field}
                            checked={field.value}
                            onCheckedChange={field.onChange}
                        />
                    </FormControl>

                    <FormMessage />
                </FormItem>
            )}
        />
    )
}
