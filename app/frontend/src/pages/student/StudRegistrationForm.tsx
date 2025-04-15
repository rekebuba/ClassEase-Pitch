import { useState } from 'react';
import '../../styles/StudRegistrationForm.css';
import { api } from '@/api';
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";

const studentSchema = z.object({
  name: z.string().min(3, "Name must be at least 3 characters"),
  father_name: z.string().min(3, "Father's name is required"),
  grand_father_name: z.string().optional(),
  date_of_birth: z.string().refine((date) => !isNaN(Date.parse(date)), "Invalid date"),
  father_phone: z.string().optional(),
  mother_phone: z.string().optional(),
  guardian_phone: z.string().optional(),
  start_year: z.string().min(4, "Start year is required"),
  end_year: z.string().optional(),
  previous_school: z.string().optional(),
  grade: z.string().min(1, "Grade is required"),
  section: z.string().optional(),
  birth_certificate: z.any().optional(),
  national_id: z.string().optional(),
  has_medical_condition: z.boolean(),
  medical_details: z.string().optional(),
  has_disability: z.boolean(),
  disability_details: z.string().optional(),
  requires_special_accommodation: z.boolean(),
  special_accommodation_details: z.string().optional(),
}).refine((data) => data.father_phone || data.mother_phone || data.guardian_phone, {
  message: "At least one contact (Father, Mother, or Guardian) is required",
  path: ["father_phone"],
});

/**
 * StudentRegistrationForm component handles the registration form for students.
 * It manages form state, handles form submission, and displays alerts based on the response.
 *
 * @component
 * @example
 * return (
 *   <StudentRegistrationForm />
 * )
 *
 * @returns {JSX.Element} The rendered component.
 *
 * @typedef {Object} FormData
 * @property {string} name - The student's name.
 * @property {string} fatherName - The student's father's name.
 * @property {string} grandFatherName - The student's grandfather's name.
 * @property {string} grade - The student's grade.
 * @property {string} dateOfBirth - The student's date of birth.
 * @property {string} fatherPhone - The student's father's phone number.
 * @property {string} motherPhone - The student's mother's phone number.
 * @property {string} startYear - The year the student is registering for.
 */
const StudentRegistrationForm = ({ role }) => {
  const { register, handleSubmit, watch, formState: { errors } } = useForm({
    resolver: zodResolver(studentSchema),
  });
  const [step, setStep] = useState(1);

  const [alert, setAlert] = useState({ type: "", message: "", show: false });
  const [currentYear] = useState(new Date().getFullYear());
  const [formData, setFormData] = useState({
    name: "",
    fatherName: "",
    grandFatherName: "",
    grade: "",
    dateOfBirth: "",
    fatherPhone: "",
    motherPhone: "",
    startYear: ""
  });

  /**
   * @function handleSubmit
   * @description Handles form submission, sends data to the server, and displays alerts based on the response.
   * @param {Event} e - The form submission event.
   * @async
   * @returns {Promise<void>} A promise that resolves when the form submission is complete.
   * @throws {Error} An error if the form submission fails.
   */
  // const handleSubmit = async (e) => {
  //   e.preventDefault();
  //   const snakeCaseFormData = convertKeysToSnakeCase(formData);
  //   try {
  //     const response = await Api.post('/student/registration', snakeCaseFormData);
  //     showAlert("success", response.data['message']);
  //     // clear the form inputs (keeps user on same page)
  //     setFormData({
  //       name: "",
  //       fatherName: "",
  //       grandFatherName: "",
  //       grade: "",
  //       dateOfBirth: "",
  //       fatherPhone: "",
  //       motherPhone: "",
  //       startYear: ""
  //     });
  //   } catch (error) {
  //     if (error.response && error.response.data && error.response.data['error']) {
  //       showAlert("warning", error.response.data['error']);
  //     } else {
  //       showAlert("warning", "An unexpected error occurred.");
  //     }
  //   }
  // };

  const onSubmit = (data) => {
    console.log("Form Submitted", data);
  };

  /**
   * @function handleInputChange
   * @description Handles input changes and updates the form state.
   * @param {Event} e - The input change
   * @returns {void}
   */
  const handleInputChange = e => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  /**
   * @function showAlert
   * @description Displays an alert with the specified type and message.
   * @param {string} type - The type of alert (e.g., "success", "warning").
   * @param {string} message - The alert message.
   * @returns {void}
   */
  const showAlert = (type, message) => {
    setAlert({ type, message, show: true });
  };

  /**
   * @function closeAlert
   * @description Closes the currently displayed alert.
   * @returns {void}
   */
  const closeAlert = () => {
    setAlert({ ...alert, show: false });
  };

  return (
    <Card className="max-w-3xl mx-auto mt-8 p-6 shadow-lg border border-gray-200 rounded-lg bg-white">
      <CardHeader className="mb-4">
        <CardTitle className="text-2xl font-bold text-gray-800">
          Student Enrollment Form
        </CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
          {step === 1 && (
            <div className="space-y-4">
              <div>
                <Label htmlFor="name" className="block text-sm font-medium text-gray-700">
                  Name:
                </Label>
                <Input
                  id="name"
                  {...register("name")}
                  placeholder="Enter full name"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200"
                />
                {errors.name && <p className="mt-1 text-sm text-red-600">{errors.name.message}</p>}
              </div>

              <div>
                <Label htmlFor="father_name" className="block text-sm font-medium text-gray-700">
                  Father's Name:
                </Label>
                <Input
                  id="father_name"
                  {...register("father_name")}
                  placeholder="Enter father's name"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200"
                />
                {errors.father_name && <p className="mt-1 text-sm text-red-600">{errors.father_name.message}</p>}
              </div>

              <div>
                <Label htmlFor="date_of_birth" className="block text-sm font-medium text-gray-700">
                  Date of Birth:
                </Label>
                <Input
                  id="date_of_birth"
                  type="date"
                  {...register("date_of_birth")}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200"
                />
                {errors.date_of_birth && <p className="mt-1 text-sm text-red-600">{errors.date_of_birth.message}</p>}
              </div>
            </div>
          )}

          {step === 2 && (
            <div className="space-y-4">
              <div>
                <Label htmlFor="father_phone" className="block text-sm font-medium text-gray-700">
                  Father's Phone:
                </Label>
                <Input
                  id="father_phone"
                  {...register("father_phone")}
                  placeholder="Enter father's phone"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200"
                />
              </div>

              <div>
                <Label htmlFor="mother_phone" className="block text-sm font-medium text-gray-700">
                  Mother's Phone:
                </Label>
                <Input
                  id="mother_phone"
                  {...register("mother_phone")}
                  placeholder="Enter mother's phone"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200"
                />
              </div>

              <div>
                <Label htmlFor="guardian_phone" className="block text-sm font-medium text-gray-700">
                  Guardian's Phone (if applicable):
                </Label>
                <Input
                  id="guardian_phone"
                  {...register("guardian_phone")}
                  placeholder="Enter guardian's phone"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200"
                />
              </div>
              {errors.father_phone && <p className="mt-1 text-sm text-red-600">{errors.father_phone.message}</p>}
            </div>
          )}

          {step === 3 && (
            <div className="space-y-4">
              <div>
                <Label htmlFor="start_year" className="block text-sm font-medium text-gray-700">
                  Start Year:
                </Label>
                <Input
                  id="start_year"
                  {...register("start_year")}
                  placeholder="YYYY"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200"
                />
                {errors.start_year && <p className="mt-1 text-sm text-red-600">{errors.start_year.message}</p>}
              </div>

              <div>
                <Label htmlFor="grade" className="block text-sm font-medium text-gray-700">
                  Grade:
                </Label>
                <Input
                  id="grade"
                  {...register("grade")}
                  placeholder="Enter grade level"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200"
                />
                {errors.grade && <p className="mt-1 text-sm text-red-600">{errors.grade.message}</p>}
              </div>
            </div>
          )}

          {step === 4 && (
            <div className="space-y-4">
              <div className="flex items-center space-x-2">
                <Checkbox id="has_medical_condition" {...register("has_medical_condition")} />
                <Label htmlFor="has_medical_condition" className="text-sm font-medium text-gray-700">
                  Medical Condition
                </Label>
              </div>
              {watch("has_medical_condition") && (
                <div>
                  <Label htmlFor="medical_details" className="block text-sm font-medium text-gray-700">
                    Medical Details:
                  </Label>
                  <Input
                    id="medical_details"
                    {...register("medical_details")}
                    placeholder="Describe medical condition"
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200"
                  />
                </div>
              )}

              <div className="flex items-center space-x-2">
                <Checkbox id="has_disability" {...register("has_disability")} />
                <Label htmlFor="has_disability" className="text-sm font-medium text-gray-700">
                  Disability
                </Label>
              </div>
              {watch("has_disability") && (
                <div>
                  <Label htmlFor="disability_details" className="block text-sm font-medium text-gray-700">
                    Disability Details:
                  </Label>
                  <Input
                    id="disability_details"
                    {...register("disability_details")}
                    placeholder="Describe disability"
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200"
                  />
                </div>
              )}
            </div>
          )}

          <div className="flex justify-between pt-4">
            {step > 1 && (
              <Button
                type="button"
                onClick={() => setStep(step - 1)}
                className="px-4 py-2 bg-gray-300 text-gray-800 rounded-md hover:bg-gray-400"
              >
                Back
              </Button>
            )}
            {step < 4 ? (
              <Button
                type="button"
                onClick={() => setStep(step + 1)}
                className="ml-auto px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
              >
                Next
              </Button>
            ) : (
              <Button
                type="submit"
                className="ml-auto px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
              >
                Submit
              </Button>
            )}
          </div>
        </form>
      </CardContent>
    </Card>
  );
};

export default StudentRegistrationForm;
