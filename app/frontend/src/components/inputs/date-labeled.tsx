import { zodResolver } from "@hookform/resolvers/zod"
import { format } from "date-fns"
import { CalendarIcon } from "lucide-react"
import { useForm, useFormContext } from "react-hook-form"
import { toast } from "sonner"
import { z } from "zod"

import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Calendar } from "@/components/ui/calendar"
import {
    Form,
    FormControl,
    FormDescription,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form"
import {
    Popover,
    PopoverContent,
    PopoverTrigger,
} from "@/components/ui/popover"
import { InputHTMLAttributes } from "react"
import React from "react"

type Props = {
    fieldTitle: string,
    nameInSchema: string,
    className?: string,
    disableFrom?: Date,
    disableTo?: Date,
} & InputHTMLAttributes<HTMLInputElement>


export function DateWithLabel({
    fieldTitle,
    nameInSchema,
    className,
    disableFrom = new Date("1900-01-01"),
    disableTo = new Date("2035-12-31"),
    ...props
}: Props) {
    const form = useFormContext()
    const [date] = React.useState<Date | undefined>(undefined)
    const [month, setMonth] = React.useState<Date | undefined>(date)

    return (
        <FormField
            control={form.control}
            name={nameInSchema}
            render={({ field }) => (
                <FormItem className="flex flex-col">
                    <FormLabel>{fieldTitle}</FormLabel>
                    <Popover>
                        <PopoverTrigger asChild>
                            <FormControl>
                                <Button
                                    variant={"outline"}
                                    className={cn(
                                        "pl-3 text-left font-normal",
                                        !field.value && "text-muted-foreground"
                                    )}
                                >
                                    {field.value ? (
                                        format(field.value, "PPP")
                                    ) : (
                                        <span>Pick a date</span>
                                    )}
                                    <CalendarIcon className="ml-auto h-4 w-4 opacity-50" />
                                </Button>
                            </FormControl>
                        </PopoverTrigger>
                        <PopoverContent className="w-auto p-0" align="start">
                            <Calendar
                                mode="single"
                                selected={field.value}
                                onSelect={(date) => {
                                    field.onChange(date ? format(date, "yyyy-MM-dd") : "")
                                }}
                                month={month}
                                onMonthChange={setMonth}
                                captionLayout="dropdown"
                                disabled={(date) =>
                                    date > disableTo || date < disableFrom
                                }
                                startMonth={disableFrom}
                                endMonth={disableTo}
                            />
                        </PopoverContent>
                    </Popover>
                    <FormMessage />
                </FormItem>
            )}
        />
    )
}
