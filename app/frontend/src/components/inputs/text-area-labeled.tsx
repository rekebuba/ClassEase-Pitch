import { FieldValues, Path, useFormContext } from "react-hook-form"

import {
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from '@/components/ui/form'

import { Textarea } from "@/components/ui/textarea"
import { TextareaHTMLAttributes } from "react"

type TextAreaWithLabelProps<T extends FieldValues> = {
    fieldTitle: string,
    nameInSchema: Path<T>,
    className?: string,
} & TextareaHTMLAttributes<HTMLTextAreaElement>

export function TextAreaWithLabel<T extends FieldValues>({
    fieldTitle, nameInSchema, className, ...props
}: TextAreaWithLabelProps<T>) {
    const form = useFormContext()

    return (
        <FormField
            control={form.control}
            name={nameInSchema}
            render={({ field }) => (
                <FormItem>
                    <FormLabel
                        className="text-base mb-2"
                        htmlFor={nameInSchema}
                    >
                        {fieldTitle}
                    </FormLabel>

                    <FormControl>
                        <Textarea
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
