import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { ProfileProgress } from "@/components/guest/profile-progress";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";

import type { GuestProfile } from "@/lib/guest-data";

const profileSchema = z.object({
  firstName: z.string().min(1, "First name is required"),
  lastName: z.string().min(1, "Last name is required"),
  email: z.string().email("Enter a valid email"),
  phone: z.string().min(1, "Phone number is required"),
  dateOfBirth: z.string().optional(),
  gender: z.string().optional(),
  photoUrl: z.string().optional(),
  city: z.string().min(1, "City is required"),
  address: z.string().optional(),
  highestEducation: z.string().min(1, "Highest education is required"),
  fieldOfStudy: z.string().min(1, "Field of study is required"),
  institution: z.string().optional(),
  yearsOfExperience: z.string().min(1, "Years of experience is required"),
  skills: z.string().optional(),
  certifications: z.string().optional(),
  summary: z.string().optional(),
});

type ProfileFormValues = z.infer<typeof profileSchema>;

export function ProfileForm({
  profile,
  onSave,
  onUseSample,
}: {
  profile: GuestProfile;
  onSave: (profile: GuestProfile) => void;
  onUseSample?: () => void;
}) {
  const form = useForm<ProfileFormValues>({
    resolver: zodResolver(profileSchema),
    defaultValues: profile,
  });

  function onSubmit(values: ProfileFormValues) {
    onSave({
      ...profile,
      ...values,
      dateOfBirth: values.dateOfBirth ?? "",
      gender: values.gender ?? "",
      photoUrl: values.photoUrl ?? "",
      address: values.address ?? "",
      institution: values.institution ?? "",
      yearsOfExperience: values.yearsOfExperience ?? "",
      skills: values.skills ?? "",
      certifications: values.certifications ?? "",
      summary: values.summary ?? "",
    });
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <Card className="rounded-lg">
          <CardHeader>
            <CardTitle>Employment profile</CardTitle>
            <CardDescription>
              Complete this once and reuse it when applying for school positions.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ProfileProgress profile={form.watch() as GuestProfile} />
          </CardContent>
        </Card>

        <Card className="rounded-lg">
          <CardHeader>
            <CardTitle>Personal information</CardTitle>
            <CardDescription>Required fields help schools identify and contact you.</CardDescription>
          </CardHeader>
          <CardContent className="grid gap-4 md:grid-cols-2">
            <TextField name="firstName" label="First name" required />
            <TextField name="lastName" label="Last name" required />
            <TextField name="dateOfBirth" label="Date of birth" type="date" />
            <SelectField
              name="gender"
              label="Gender"
              placeholder="Select gender"
              options={["Female", "Male", "Prefer not to say"]}
            />
            <TextField name="photoUrl" label="Profile photo URL" placeholder="https://..." />
          </CardContent>
        </Card>

        <Card className="rounded-lg">
          <CardHeader>
            <CardTitle>Contact information</CardTitle>
            <CardDescription>Email, phone, and city are required. Address is optional.</CardDescription>
          </CardHeader>
          <CardContent className="grid gap-4 md:grid-cols-2">
            <TextField name="email" label="Email" type="email" required />
            <TextField name="phone" label="Phone number" required />
            <TextField name="city" label="City" required />
            <TextField name="address" label="Address" />
          </CardContent>
        </Card>

        <Card className="rounded-lg">
          <CardHeader>
            <CardTitle>Employment information</CardTitle>
            <CardDescription>
              Education, field of study, and experience are required for employment applications.
            </CardDescription>
          </CardHeader>
          <CardContent className="grid gap-4 md:grid-cols-2">
            <SelectField
              name="highestEducation"
              label="Highest education"
              placeholder="Select education level"
              required
              options={["Diploma", "Bachelor's degree", "Master's degree", "Doctorate", "Professional certificate"]}
            />
            <TextField name="fieldOfStudy" label="Field of study" required />
            <TextField name="institution" label="Institution" />
            <TextField name="yearsOfExperience" label="Years of experience" type="number" min="0" required />
            <TextareaField name="skills" label="Skills" placeholder="Mathematics instruction, classroom technology, lesson planning" />
            <TextareaField name="certifications" label="Certifications" placeholder="Teaching license, short courses, awards" />
            <div className="md:col-span-2">
              <TextareaField name="summary" label="Professional summary" placeholder="Briefly describe your strengths and the roles you are looking for." />
            </div>
          </CardContent>
        </Card>

        <div className="flex flex-col-reverse gap-3 sm:flex-row sm:justify-end">
          {onUseSample && (
            <Button type="button" variant="outline" onClick={onUseSample}>
              Fill Sample Profile
            </Button>
          )}
          <Button type="submit">Save Profile</Button>
        </div>
      </form>
    </Form>
  );
}

function requiredLabel(label: string, required?: boolean) {
  return (
    <span>
      {label}
      {" "}
      <span className={required ? "text-destructive" : "text-muted-foreground"}>
        {required ? "Required" : "Optional"}
      </span>
    </span>
  );
}

function TextField({
  name,
  label,
  required,
  ...props
}: {
  name: keyof ProfileFormValues;
  label: string;
  required?: boolean;
} & React.ComponentProps<typeof Input>) {
  return (
    <FormField
      name={name}
      render={({ field }) => (
        <FormItem>
          <FormLabel>{requiredLabel(label, required)}</FormLabel>
          <FormControl>
            <Input {...props} {...field} value={field.value ?? ""} />
          </FormControl>
          <FormMessage />
        </FormItem>
      )}
    />
  );
}

function TextareaField({
  name,
  label,
  placeholder,
}: {
  name: keyof ProfileFormValues;
  label: string;
  placeholder?: string;
}) {
  return (
    <FormField
      name={name}
      render={({ field }) => (
        <FormItem>
          <FormLabel>{requiredLabel(label)}</FormLabel>
          <FormControl>
            <Textarea {...field} value={field.value ?? ""} placeholder={placeholder} />
          </FormControl>
          <FormDescription>Optional information that schools can review when relevant.</FormDescription>
          <FormMessage />
        </FormItem>
      )}
    />
  );
}

function SelectField({
  name,
  label,
  placeholder,
  options,
  required,
}: {
  name: keyof ProfileFormValues;
  label: string;
  placeholder: string;
  options: string[];
  required?: boolean;
}) {
  return (
    <FormField
      name={name}
      render={({ field }) => (
        <FormItem>
          <FormLabel>{requiredLabel(label, required)}</FormLabel>
          <Select onValueChange={field.onChange} value={String(field.value ?? "")}>
            <FormControl>
              <SelectTrigger className="w-full">
                <SelectValue placeholder={placeholder} />
              </SelectTrigger>
            </FormControl>
            <SelectContent>
              {options.map(option => (
                <SelectItem key={option} value={option}>{option}</SelectItem>
              ))}
            </SelectContent>
          </Select>
          <FormMessage />
        </FormItem>
      )}
    />
  );
}
