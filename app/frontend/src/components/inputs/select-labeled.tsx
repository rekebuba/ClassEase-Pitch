import { useFormContext } from "react-hook-form"

import {
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from '@/components/ui/form'

import {
    Select,
    SelectContent,
    SelectTrigger,
    SelectValue,
} from '@/components/ui/select'

type Props = {
    fieldTitle: string,
    nameInSchema: string,
    className?: string,
    children?: React.ReactNode,
}

export function SelectWithLabel({
    fieldTitle, nameInSchema, className, children
}: Props) {
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

                    <Select
                        {...field}
                        onValueChange={field.onChange}
                    >
                        <FormControl>
                            <SelectTrigger
                                id={nameInSchema}
                                className={`${className}`}
                            >
                                <SelectValue placeholder="Choose from suggestions..." />
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
    )
}
