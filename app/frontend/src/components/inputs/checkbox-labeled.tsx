import { useFormContext } from "react-hook-form"

import {
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from '@/components/ui/form'

import { Checkbox } from '@/components/ui/checkbox'

type Props = {
    fieldTitle: string,
    nameInSchema: string,
    disabled?: boolean,
    className?: string,
}

export function CheckboxWithLabel({
    fieldTitle, nameInSchema, disabled = false, className
}: Props) {
    const form = useFormContext()

    return (
        <FormField
            control={form.control}
            name={nameInSchema}
            render={({ field }) => (
                <FormItem className="w-full flex items-center gap-2">
                    <div className="flex items-center gap-2">
                        <FormControl>
                            <Checkbox
                                id={nameInSchema}
                                {...field}
                                checked={field.value}
                                onCheckedChange={field.onChange}
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
    )
}
