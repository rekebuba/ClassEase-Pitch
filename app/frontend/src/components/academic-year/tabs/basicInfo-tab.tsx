import { useFormContext } from "react-hook-form"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { InputWithLabel } from "@/components/inputs/input-labeled"
import { DateWithLabel } from "@/components/inputs/date-labeled"
import { SelectWithLabel } from "@/components/inputs/select-labeled"
import { SelectItem } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { useEffect, useState } from "react"
import { YearSetupType } from "@/lib/api-response-type"


export default function BasicInfoTab({
    onDirty,
}: {
    onDirty: (dirty: boolean) => void
}) {
    const [dayDifference, setDayDifference] = useState<number | null>(null);
    const { register, formState, watch, setValue } = useFormContext<YearSetupType>()
    const startDate = watch("startDate")
    const endDate = watch("endDate")

    useEffect(() => {
        if (startDate && endDate) {
            const start = new Date(startDate);
            const end = new Date(endDate);
            const diffInDays = Math.ceil((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24));
            setDayDifference(diffInDays);
            if (startDate > endDate) {
                setValue("endDate", "");
            }
        } else {
            setDayDifference(null);
        }
    }, [startDate, endDate]);

    // Mark dirty state
    onDirty(formState.isDirty)

    return (
        <Card>
            <CardHeader>
                <CardTitle>Academic Year Basic Information</CardTitle>
                <p className="text-sm text-gray-600">Set up the fundamental details of your academic year</p>
            </CardHeader>
            <CardContent className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <InputWithLabel<YearSetupType>
                        fieldTitle="Academic Year Name"
                        nameInSchema="name"
                        placeholder="e.g., 2024-2025 Academic Year"
                    />
                    <SelectWithLabel<YearSetupType>
                        fieldTitle="Term System"
                        nameInSchema="calendarType"
                    >
                        <SelectItem value="Semester">Semester (2 Terms)</SelectItem>
                        <SelectItem value="Quarter">Quarterly (4 Terms)</SelectItem>
                    </SelectWithLabel>
                </div>
                <div className="flex items-center gap-3 flex-wrap">
                    <div className="flex-1 min-w-0">
                        <DateWithLabel<YearSetupType>
                            fieldTitle="Academic Year Start Date"
                            nameInSchema="startDate"
                        />
                    </div>
                    {/* Calculate Date Range */}
                    <Badge
                        variant={dayDifference && dayDifference < 0 ? "destructive" : "outline"}
                        className="whitespace-nowrap mt-7"
                    >
                        {dayDifference !== null ? `${dayDifference} d` : '--'}
                    </Badge>
                    <div className="flex-1 min-w-0">
                        <DateWithLabel<YearSetupType>
                            fieldTitle="Academic Year End Date"
                            nameInSchema="endDate"
                            className="flex-1 min-w-0"
                            disableFrom={startDate ? new Date(startDate) : new Date("1900-01-01")}
                        />
                    </div>
                </div>
            </CardContent>
        </Card>
    )
}
