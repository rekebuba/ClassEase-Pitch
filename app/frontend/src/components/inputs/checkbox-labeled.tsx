import { FieldValues, Path, PathValue, useFormContext, useWatch } from "react-hook-form"

import {
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from '@/components/ui/form'

import { Checkbox } from '@/components/ui/checkbox'
import { isEqual } from "lodash"


type Primitive = string | number | boolean

type CheckboxWithLabelProps<T extends FieldValues, V> = {
    fieldTitle: string
    nameInSchema: Path<T>
    className?: string
    disabled?: boolean
    /** If provided, checkbox will act as "toggle in array of objects" mode */
    value?: V
}

export function CheckboxWithLabel<T extends FieldValues, V>({
    fieldTitle,
    nameInSchema,
    className,
    disabled = false,
    value,
}: CheckboxWithLabelProps<T, V>) {
    const form = useFormContext<T>()
    const control = form.control

    // --- Object toggle mode ---
    const values = value ? useWatch({ control, name: nameInSchema }) || [] : undefined
    const checked = (value && values) ? values.some((v: T) => isEqual(v, value)) : undefined

    const getKey = (x: unknown): Primitive => (x as any).id

    const sortValues = <E,>(arr: E[], key?: (x: E) => Primitive) => {
        const cmp = (a: E, b: E) => {
            const ak = key ? key(a) : (a as unknown as Primitive)
            const bk = key ? key(b) : (b as unknown as Primitive)
            return ak < bk ? -1 : ak > bk ? 1 : 0
        }
        return [...arr].sort(cmp)
    }

    const toggle = (isChecked: boolean) => {
        const current = (form.getValues(nameInSchema) as unknown as T[]) || []
        if (isChecked) {
            const next = sortValues([...current, value!], getKey)
            form.setValue(nameInSchema, next as PathValue<T, Path<T>>, { shouldValidate: true, shouldDirty: true })
        } else {
            const next = sortValues(
                current.filter((item: T) => !isEqual(item, value)),
                getKey
            )
            form.setValue(nameInSchema, next as PathValue<T, Path<T>>, { shouldValidate: true, shouldDirty: true })
        }
    }

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
    )
}
