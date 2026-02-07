import { Calendar } from "lucide-react";
import { useEffect } from "react";
import { useFieldArray, useFormContext } from "react-hook-form";

import { zAcademicTermTypeEnum } from "@/client/zod.gen";
import { DateWithLabel } from "@/components/inputs/date-labeled";
import DateRangeLabeled from "@/components/inputs/date-range-labeled";
import { InputWithLabel } from "@/components/inputs/input-labeled";
import { SelectWithLabel } from "@/components/inputs/select-labeled";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { SelectItem } from "@/components/ui/select";

import type { AcademicTermEnum, YearSetupSchemaOutput } from "@/client/types.gen";

export default function BasicInfoTab({
  onDirty,
}: {
  onDirty: (dirty: boolean) => void;
}) {
  const {
    formState: { isDirty },
    control,
    watch,
    setValue,
  } = useFormContext<YearSetupSchemaOutput>();
  const { append: appendTerm } = useFieldArray({
    control,
    name: "academicTerms",
    keyName: "rhfId",
  });
  const form = watch();

  onDirty(isDirty);

  const getValue = (value: AcademicTermEnum) => {
    switch (value) {
      case "1":
        return "First";
      case "2":
        return "Second";
      case "3":
        return "Third";
      case "4":
        return "Fourth";
      default:
        return "Unknown";
    }
  };

  useEffect(() => {
    // This effect runs when the form state changes
    if (form.academicTerms.length === 4 && form.calendarType === "Semester") {
      setValue("academicTerms", form.academicTerms.slice(0, 2));
    }
    else if (
      form.academicTerms.length === 2
      && form.calendarType === "Quarter"
    ) {
      appendTerm({
        id: String(Date.now()),
        yearId: form.id,
        name: "3",
        startDate: "",
        endDate: "",
      });
      appendTerm({
        id: String(Date.now()),
        yearId: form.id,
        name: "4",
        startDate: "",
        endDate: "",
      });
    }
  }, [form.calendarType]);

  const disableFrom = (index: number) => {
    return form.academicTerms[index - 1]?.endDate
      ? new Date(form.academicTerms[index - 1]?.endDate)
      : form.startDate
        ? new Date(form.startDate)
        : new Date("2035-12-31");
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Academic Year Basic Information</CardTitle>
        <p className="text-sm text-gray-600">
          Set up the fundamental details of your academic year
        </p>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="flex items-center gap-3 flex-wrap">
          <div className="flex-1 min-w-0">
            <DateWithLabel<YearSetupSchemaOutput>
              fieldTitle="Academic Year Start Date"
              nameInSchema="startDate"
            />
          </div>
          <div className="flex-1 min-w-0">
            <DateWithLabel<YearSetupSchemaOutput>
              fieldTitle="Academic Year End Date"
              nameInSchema="endDate"
              className="flex-1 min-w-0"
              disableFrom={
                form.startDate
                  ? new Date(form.startDate)
                  : new Date("1900-01-01")
              }
            />
          </div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <InputWithLabel<YearSetupSchemaOutput>
            fieldTitle="Academic Year Name"
            nameInSchema="name"
            placeholder="e.g., 2024-2025 Academic Year"
          />
          <SelectWithLabel<YearSetupSchemaOutput, string>
            fieldTitle="Term System"
            nameInSchema="calendarType"
          >
            {zAcademicTermTypeEnum.options.map(option => (
              <SelectItem value={option}>{option}</SelectItem>
            ))}
          </SelectWithLabel>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {form.academicTerms
            .sort((a, b) => Number(a.name) - Number(b.name))
            .map((term, index) => (
              <Card key={term.id}>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 mb-2 text-md">
                    <Calendar className="shrink-0" />
                    <span className="truncate">{` ${getValue(term.name)} ${form.calendarType}`}</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center gap-3 flex-wrap">
                    <div className="flex-1 min-w-0">
                      <DateRangeLabeled<YearSetupSchemaOutput>
                        fieldTitle={`Select ${getValue(term.name)} ${form.calendarType} Start and End Date`}
                        fromInSchema={`academicTerms.${index}.startDate`}
                        toInSchema={`academicTerms.${index}.endDate`}
                        disableFrom={disableFrom(index)}
                        disableTo={
                          form.endDate
                            ? new Date(form.endDate)
                            : new Date("2035-12-31")
                        }
                      />
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
        </div>
      </CardContent>
    </Card>
  );
}
