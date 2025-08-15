import { FieldValues, Path, useFormContext } from "react-hook-form"

import {
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { InputHTMLAttributes } from "react"

type InputWithLabelProps<T extends FieldValues> = {
    fieldTitle: string,
    nameInSchema: Path<T>,
    className?: string,
} & InputHTMLAttributes<HTMLInputElement>

export function InputWithLabel<T extends FieldValues>({
    fieldTitle, nameInSchema, className, ...props
}: InputWithLabelProps<T>) {
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
                        <Input
                            id={nameInSchema}
                            className={`disabled:text-blue-500 dark:disabled:text-yellow-300 disabled:opacity-75 ${className}`}
                            {...props}
                            {...field}
                        />
                    </FormControl>

                    <FormMessage />
                </FormItem>
            )}
        />
    )
}
