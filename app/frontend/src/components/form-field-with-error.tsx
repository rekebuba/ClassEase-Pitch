import { AlertCircle, CheckCircle } from "lucide-react";

import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { cn } from "@/lib/utils";

import type React from "react";

type FormFieldProps = {
  label: string;
  id: string;
  error?: string;
  success?: boolean;
  required?: boolean;
  children: React.ReactNode;
  description?: string;
};

export function FormField({
  label,
  id,
  error,
  success,
  required,
  children,
  description,
}: FormFieldProps) {
  return (
    <div className="space-y-2">
      <Label htmlFor={id} className={cn("flex items-center gap-1")}>
        {label}
        {required && <span className="text-red-500">*</span>}
      </Label>
      {description && <p className="text-sm text-gray-600">{description}</p>}
      <div className="relative">
        {children}
        {success && !error && (
          <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
            <CheckCircle className="h-4 w-4 text-green-500" />
          </div>
        )}
      </div>
      {error && (
        <p className="text-sm text-red-600 flex items-center gap-1">
          <AlertCircle className="h-3 w-3" />
          {error}
        </p>
      )}
    </div>
  );
}

type InputWithErrorProps = {
  error?: string;
} & React.InputHTMLAttributes<HTMLInputElement>;

export function InputWithError({
  error,
  className,
  ...props
}: InputWithErrorProps) {
  return (
    <Input
      className={cn(
        error && "border-red-500 focus:border-red-500 focus:ring-red-500",
        !error && props.value && "border-green-500",
        className,
      )}
      {...props}
    />
  );
}

type TextareaWithErrorProps = {
  error?: string;
} & React.TextareaHTMLAttributes<HTMLTextAreaElement>;

export function TextareaWithError({
  error,
  className,
  ...props
}: TextareaWithErrorProps) {
  return (
    <Textarea
      className={cn(
        error && "border-red-500 focus:border-red-500 focus:ring-red-500",
        !error && props.value && "border-green-500",
        className,
      )}
      {...props}
    />
  );
}

type SelectWithErrorProps = {
  error?: string;
  children: React.ReactNode;
  value?: string;
  onValueChange?: (value: string) => void;
  placeholder?: string;
};

export function SelectWithError({
  error,
  children,
  ...props
}: SelectWithErrorProps) {
  return (
    <>
      <Select {...props}>
        <SelectTrigger
          className={cn(
            error && "border-red-500 focus:border-red-500 focus:ring-red-500",
            !error && props.value && "border-green-500",
          )}
        >
          <SelectValue placeholder={props.placeholder} />
        </SelectTrigger>
        <SelectContent>{children}</SelectContent>
      </Select>
    </>
  );
}
