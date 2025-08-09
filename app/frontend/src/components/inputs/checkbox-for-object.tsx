import { useFormContext, useWatch } from "react-hook-form"
import {
    FormControl,
    FormField,
    FormItem,
    FormMessage,
} from '@/components/ui/form'

import { Checkbox } from '@/components/ui/checkbox'
import isEqual from "lodash/isEqual"

type Props<T> = {
    fieldTitle: string
    nameInSchema: string
    value: T             // the object this checkbox represents
    disabled?: boolean
    className?: string
}

export function CheckboxForObject<T>({
    fieldTitle,
    nameInSchema,
    value,
    disabled = false,
    className,
}: Props<T>) {
    const { setValue, getValues, control } = useFormContext()
    const values = useWatch({ control: control, name: nameInSchema }) || []

    const checked = values.some((v: T) => isEqual(v, value))

    const toggle = (checked: boolean) => {
        const current = getValues(nameInSchema) || []
        if (checked) {
            setValue(nameInSchema, [...current, value], { shouldValidate: true })
        } else {
            setValue(
                nameInSchema,
                current.filter((item: T) => !isEqual(item, value)),
                { shouldValidate: true }
            )
        }
    }


    return (
        <FormField
            control={control}
            name={nameInSchema}
            render={() => (
                <FormItem className="w-full flex items-center gap-2">
                    <div className="flex items-center gap-2">
                        <FormControl>
                            <Checkbox
                                checked={checked}
                                onCheckedChange={toggle}
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
