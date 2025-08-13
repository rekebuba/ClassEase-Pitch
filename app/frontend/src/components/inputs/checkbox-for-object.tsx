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
    value: T
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

    // If items are objects, provide a stable key (e.g., id, value, name).
    type Primitive = string | number | boolean;

    // sort by a stable object key
    const getKey = (x: T): Primitive => (x as any).id;

    const sortValues = (arr: T[], key?: (x: T) => Primitive) => {
        const cmp = (a: T, b: T) => {
            const ak = key ? key(a) : (a as unknown as Primitive);
            const bk = key ? key(b) : (b as unknown as Primitive);
            return ak < bk ? -1 : ak > bk ? 1 : 0;
        };
        return [...arr].sort(cmp); // don't mutate original
    };

    const toggle = (checked: boolean) => {
        const current: T[] = getValues(nameInSchema) || [];

        if (checked) {
            const next = sortValues([...current, value], getKey);
            setValue(nameInSchema, next, { shouldValidate: true, shouldDirty: true });
        } else {
            const next = sortValues(
                current.filter((item: T) => !isEqual(item, value)),
                getKey
            );
            setValue(nameInSchema, next, { shouldValidate: true, shouldDirty: true });
        }
    };


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
