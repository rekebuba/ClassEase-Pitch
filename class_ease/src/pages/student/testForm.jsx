import React, { useState } from 'react';
import '../../styles/StudRegistrationForm.css';
import Api from '../../services/api';
import Alert from "../../services/Alert";
import convertKeysToSnakeCase from '../library/lodash';
import HomeHeader from '../../components/HomeHeader';
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { useToast } from "@/components/ui/use-toast";

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
  const { toast } = useToast();

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
    toast({ title: "Success", description: "Student enrolled successfully!" });
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
    <Card className="max-w-3xl mx-auto mt-8 p-6">
      <CardHeader>
        <CardTitle>Student Enrollment Form</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          {step === 1 && (
            <>
              <Label>Name:</Label>
              <Input {...register("name")} placeholder="Enter full name" />
              {errors.name && <p className="text-red-500">{errors.name.message}</p>}

              <Label>Father's Name:</Label>
              <Input {...register("father_name")} placeholder="Enter father's name" />
              {errors.father_name && <p className="text-red-500">{errors.father_name.message}</p>}

              <Label>Date of Birth:</Label>
              <Input type="date" {...register("date_of_birth")} />
              {errors.date_of_birth && <p className="text-red-500">{errors.date_of_birth.message}</p>}
            </>
          )}

          {step === 2 && (
            <>
              <Label>Father's Phone:</Label>
              <Input {...register("father_phone")} placeholder="Enter father's phone" />
              <Label>Mother's Phone:</Label>
              <Input {...register("mother_phone")} placeholder="Enter mother's phone" />
              <Label>Guardian's Phone (if applicable):</Label>
              <Input {...register("guardian_phone")} placeholder="Enter guardian's phone" />
              {errors.father_phone && <p className="text-red-500">{errors.father_phone.message}</p>}
            </>
          )}

          {step === 3 && (
            <>
              <Label>Start Year:</Label>
              <Input {...register("start_year")} placeholder="YYYY" />
              <Label>Grade:</Label>
              <Input {...register("grade")} placeholder="Enter grade level" />
              {errors.start_year && <p className="text-red-500">{errors.start_year.message}</p>}
              {errors.grade && <p className="text-red-500">{errors.grade.message}</p>}
            </>
          )}

          {step === 4 && (
            <>
              <Label>Medical Condition:</Label>
              <Checkbox {...register("has_medical_condition")} />
              {watch("has_medical_condition") && (
                <>
                  <Label>Medical Details:</Label>
                  <Input {...register("medical_details")} placeholder="Describe medical condition" />
                </>
              )}

              <Label>Disability:</Label>
              <Checkbox {...register("has_disability")} />
              {watch("has_disability") && (
                <>
                  <Label>Disability Details:</Label>
                  <Input {...register("disability_details")} placeholder="Describe disability" />
                </>
              )}
            </>
          )}

          <div className="flex justify-between">
            {step > 1 && <Button onClick={() => setStep(step - 1)}>Back</Button>}
            {step < 4 ? (
              <Button onClick={() => setStep(step + 1)}>Next</Button>
            ) : (
              <Button type="submit">Submit</Button>
            )}
          </div>
        </form>
      </CardContent>
    </Card>
  );
};

export default StudentRegistrationForm;
