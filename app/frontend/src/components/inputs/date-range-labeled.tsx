import { zodResolver } from "@hookform/resolvers/zod";
import {
  FieldValues,
  Path,
  PathValue,
  useForm,
  useFormContext,
} from "react-hook-form";
import { z } from "zod";

import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { cn } from "@/lib/utils";
import { format } from "date-fns";
import { CalendarIcon } from "lucide-react";
import { InputHTMLAttributes, useEffect } from "react";

const schema = z.object({
  dateRange: z.object({
    from: z.date(),
    to: z.date(),
  }),
});

type DateRangeLabeledProps<T extends FieldValues> = {
  fieldTitle: string;
  fromInSchema: Path<T>;
  toInSchema: Path<T>;
  className?: string;
  disableFrom?: Date;
  disableTo?: Date;
} & InputHTMLAttributes<HTMLInputElement>;

export default function DateRangeLabeled<T extends FieldValues>({
  fieldTitle,
  fromInSchema,
  toInSchema,
  className,
  disableFrom = new Date("1900-01-01"),
  disableTo = new Date("2035-12-31"),
}: DateRangeLabeledProps<T>) {
  const parentForm = useFormContext<T>();

  const form = useForm<z.infer<typeof schema>>({
    resolver: zodResolver(schema),
    defaultValues: {
      dateRange: {
        from: parentForm.getValues(fromInSchema) as unknown as Date | undefined,
        to: parentForm.getValues(toInSchema) as unknown as Date | undefined,
      },
    },
  });
  const from = form.watch("dateRange").from;
  const to = form.watch("dateRange").to;

  useEffect(() => {
    parentForm.setValue(fromInSchema, from as PathValue<T, Path<T>>);
    parentForm.setValue(toInSchema, to as PathValue<T, Path<T>>);
  }, [from, to]);

  function onSubmit(values: z.infer<typeof schema>) {
    console.log("Form values:", values);
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <FormField
          control={form.control}
          name="dateRange"
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
                        !field.value && "text-muted-foreground",
                      )}
                    >
                      {field.value && field.value.from && field.value.to ? (
                        `${format(field.value.from, "PPP")} - ${format(field.value.to, "PPP")}`
                      ) : (
                        <span>Pick Range of Dates</span>
                      )}
                      <CalendarIcon className="ml-auto h-4 w-4 opacity-50" />
                    </Button>
                  </FormControl>
                </PopoverTrigger>
                <PopoverContent
                  className={`w-auto p-0 ${className}`}
                  align="start"
                >
                  <Calendar
                    mode="range"
                    className={className}
                    numberOfMonths={2}
                    selected={{ from: field.value?.from, to: field.value?.to }}
                    onSelect={field.onChange}
                    disabled={(date) => date > disableTo || date < disableFrom}
                    startMonth={disableFrom}
                    endMonth={disableTo}
                  />
                </PopoverContent>
              </Popover>
              <FormMessage />
            </FormItem>
          )}
        />
      </form>
    </Form>
  );
}
