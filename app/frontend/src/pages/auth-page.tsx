import React, { useState } from "react";
import { authApi, zodApiHandler } from '@/api'

import { AuthLayout } from "@/components"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Checkbox } from "@/components/ui/checkbox"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { GraduationCap, EyeIcon, EyeOffIcon, AlertCircle, CheckCircle } from "lucide-react"
import { Progress } from "@/components/ui/progress"
import { LoginSchema, loginSchema } from "@/lib/validations"
import { login } from "@/api/authApi";

const AuthPage = () => {
  const [activeTab, setActiveTab] = useState("login")
  const [showPassword, setShowPassword] = useState(false)
  const [password, setPassword] = useState("")
  const [email, setEmail] = useState("")
  const [identification, setIdentification] = useState("")
  const [name, setName] = useState("")
  const [school, setSchool] = useState("")
  const [role, setRole] = useState("administrator")
  const [rememberMe, setRememberMe] = useState(false)
  const [loginStatus, setLoginStatus] = useState<null | "error" | "success" | "timeout">(null)
  const [signupStatus, setSignupStatus] = useState<null | "error" | "success">(null)
  const [isLoading, setIsLoading] = useState(false)

  // Password strength calculation
  const calculatePasswordStrength = (password: string) => {
    if (!password) return 0

    let strength = 0
    // Length check
    if (password.length >= 8) strength += 25
    // Contains lowercase
    if (/[a-z]/.test(password)) strength += 25
    // Contains uppercase
    if (/[A-Z]/.test(password)) strength += 25
    // Contains number or special char
    if (/[0-9!@#$%^&*(),.?":{}|<>]/.test(password)) strength += 25

    return strength
  }

  const passwordStrength = calculatePasswordStrength(password)

  const getPasswordStrengthText = () => {
    if (passwordStrength <= 25) return "Weak"
    if (passwordStrength <= 50) return "Fair"
    if (passwordStrength <= 75) return "Good"
    return "Strong"
  }

  const getPasswordStrengthColor = () => {
    if (passwordStrength <= 25) return "bg-red-500"
    if (passwordStrength <= 50) return "bg-yellow-500"
    if (passwordStrength <= 75) return "bg-blue-500"
    return "bg-green-500"
  }

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setLoginStatus(null)

    // Simulate API call
    const timeout = 7000; // 7 seconds
    try {
      const response = await Promise.race([
        login({ identification, password }),
        new Promise((_, reject) => setTimeout(() => reject(new Error("Request timed out")), timeout))
      ]) as LoginSchema;

      localStorage.setItem("apiKey", response.apiKey);
      setLoginStatus("success")
      window.location.href = `/${response.role}/dashboard`

      setIsLoading(false)
    } catch (error) {
      setLoginStatus("timeout");
      setIsLoading(false);
      return;
    }

  }


  const handleSignup = (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setSignupStatus(null)

    // Simulate API call
    setTimeout(() => {
      if (email && password && name && school && passwordStrength >= 75) {
        setSignupStatus("success")
        // Redirect would happen here in a real app
        setTimeout(() => {
          setActiveTab("login")
          setSignupStatus(null)
        }, 2000)
      } else {
        setSignupStatus("error")
      }
      setIsLoading(false)
    }, 1500)
  }



  return (
    <AuthLayout>
      <div className="flex justify-center mb-8 lg:hidden">
        <div className="flex items-center gap-2">
          <GraduationCap className="h-8 w-8 text-sky-500" />
          <span className="text-2xl font-bold text-sky-500">ClassEase</span>
        </div>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-2 mb-8">
          <TabsTrigger value="login">
            <a href="#login">Log In</a>
          </TabsTrigger>
          <TabsTrigger value="signup">
            <a href="#signup">Sign Up</a>
          </TabsTrigger>
        </TabsList>

        <TabsContent value="login" id="login">
          <Card className="border-0 shadow-lg animate-fade-left">
            <CardHeader className="space-y-1">
              <CardTitle className="text-2xl font-bold text-center">Welcome back</CardTitle>
              <CardDescription className="text-center">Enter your credentials to access your account</CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleLogin}>
                <div className="grid gap-4">
                  <div className="grid gap-2">
                    <Label htmlFor="id">ID</Label>
                    <Input
                      id="id"
                      type="id"
                      placeholder="XXX/XXX/XXXX"
                      value={identification}
                      onChange={(e) => setIdentification(e.target.value)}
                      required
                    />
                  </div>
                  <div className="grid gap-2">
                    <div className="flex items-center justify-between">
                      <Label htmlFor="password">Password</Label>
                      <a href="#" className="text-sm text-sky-500 hover:text-sky-600">
                        Forgot password?
                      </a>
                    </div>
                    <div className="relative">
                      <Input
                        id="password"
                        type={showPassword ? "text" : "password"}
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                      />
                      <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700"
                        aria-label={showPassword ? "Hide password" : "Show password"}
                      >
                        {showPassword ? <EyeOffIcon className="h-4 w-4" /> : <EyeIcon className="h-4 w-4" />}
                      </button>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Checkbox
                      id="remember"
                      checked={rememberMe}
                      onCheckedChange={(checked) => setRememberMe(checked as boolean)}
                    />
                    <label
                      htmlFor="remember"
                      className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                    >
                      Remember me
                    </label>
                  </div>

                  {loginStatus === "timeout" && (
                    <Alert variant="destructive">
                      <AlertCircle className="h-4 w-4" />
                      <AlertDescription>Request Timed Out. Please try again.</AlertDescription>
                    </Alert>
                  )}

                  {loginStatus === "error" && (
                    <Alert variant="destructive">
                      <AlertCircle className="h-4 w-4" />
                      <AlertDescription>Invalid ID or Password. Please try again.</AlertDescription>
                    </Alert>
                  )}

                  {loginStatus === "success" && (
                    <Alert className="bg-green-50 text-green-800 border-green-200">
                      <CheckCircle className="h-4 w-4 text-green-500" />
                      <AlertDescription>Login successful! Redirecting...</AlertDescription>
                    </Alert>
                  )}

                  <Button type="submit" className="w-full" disabled={isLoading}>
                    {isLoading ? "Logging in..." : "Log in"}
                  </Button>
                </div>
              </form>
            </CardContent>

            <CardFooter className="flex flex-col">
              <p className="mt-2 text-xs text-center text-muted-foreground">
                By logging in, you agree to our{" "}
                <a href="#" className="underline underline-offset-4 hover:text-primary">
                  Terms of Service
                </a>{" "}
                and{" "}
                <a href="#" className="underline underline-offset-4 hover:text-primary">
                  Privacy Policy
                </a>
                .
              </p>
            </CardFooter>
          </Card>
        </TabsContent>

        <TabsContent value="signup" id="signup">
          <Card className="border-0 shadow-lg">
            <CardHeader className="space-y-1">
              <CardTitle className="text-2xl font-bold text-center">Create an account</CardTitle>
              <CardDescription className="text-center">
                Enter your information to create your ClassEase account
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSignup}>
                <div className="grid gap-4">
                  <div className="grid gap-2">
                    <Label htmlFor="name">Full Name</Label>
                    <Input
                      id="name"
                      type="text"
                      placeholder="John Doe"
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      required
                    />
                  </div>
                  <div className="grid gap-2">
                    <Label htmlFor="signup-email">Email</Label>
                    <Input
                      id="signup-email"
                      type="email"
                      placeholder="name@school.com"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      required
                    />
                  </div>
                  <div className="grid gap-2">
                    <Label htmlFor="school-name">School Name</Label>
                    <Input
                      id="school-name"
                      type="text"
                      placeholder="Westfield Academy"
                      value={school}
                      onChange={(e) => setSchool(e.target.value)}
                      required
                    />
                  </div>
                  <div className="grid gap-2">
                    <Label htmlFor="role">Your Role</Label>
                    <select
                      id="role"
                      className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                      value={role}
                      onChange={(e) => setRole(e.target.value)}
                      required
                    >
                      <option value="administrator">Administrator</option>
                      <option value="teacher">Teacher</option>
                      <option value="staff">Staff</option>
                      <option value="other">Other</option>
                    </select>
                  </div>
                  <div className="grid gap-2">
                    <Label htmlFor="signup-password">Password</Label>
                    <div className="relative">
                      <Input
                        id="signup-password"
                        type={showPassword ? "text" : "password"}
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                      />
                      <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700"
                        aria-label={showPassword ? "Hide password" : "Show password"}
                      >
                        {showPassword ? <EyeOffIcon className="h-4 w-4" /> : <EyeIcon className="h-4 w-4" />}
                      </button>
                    </div>
                    <div className="space-y-1 mt-1">
                      <div className="flex justify-between text-xs">
                        <span>Password strength:</span>
                        <span
                          className={
                            passwordStrength <= 25
                              ? "text-red-500"
                              : passwordStrength <= 50
                                ? "text-yellow-500"
                                : passwordStrength <= 75
                                  ? "text-blue-500"
                                  : "text-green-500"
                          }
                        >
                          {getPasswordStrengthText()}
                        </span>
                      </div>
                      <Progress value={passwordStrength} className={getPasswordStrengthColor()} />
                      <ul className="text-xs text-muted-foreground space-y-1 mt-2">
                        <li className="flex items-center">
                          <div
                            className={`w-3 h-3 rounded-full mr-2 ${password.length >= 8 ? "bg-green-500" : "bg-gray-300"
                              }`}
                          ></div>
                          At least 8 characters
                        </li>
                        <li className="flex items-center">
                          <div
                            className={`w-3 h-3 rounded-full mr-2 ${/[a-z]/.test(password) ? "bg-green-500" : "bg-gray-300"
                              }`}
                          ></div>
                          Lowercase letters (a-z)
                        </li>
                        <li className="flex items-center">
                          <div
                            className={`w-3 h-3 rounded-full mr-2 ${/[A-Z]/.test(password) ? "bg-green-500" : "bg-gray-300"
                              }`}
                          ></div>
                          Uppercase letters (A-Z)
                        </li>
                        <li className="flex items-center">
                          <div
                            className={`w-3 h-3 rounded-full mr-2 ${/[0-9!@#$%^&*(),.?":{}|<>]/.test(password) ? "bg-green-500" : "bg-gray-300"
                              }`}
                          ></div>
                          Numbers or special characters
                        </li>
                      </ul>
                    </div>
                  </div>

                  {signupStatus === "error" && (
                    <Alert variant="destructive">
                      <AlertCircle className="h-4 w-4" />
                      <AlertDescription>
                        Please check your information and ensure your password is strong enough.
                      </AlertDescription>
                    </Alert>
                  )}

                  {signupStatus === "success" && (
                    <Alert className="bg-green-50 text-green-800 border-green-200">
                      <CheckCircle className="h-4 w-4 text-green-500" />
                      <AlertDescription>
                        Account created successfully! You can now log in with your credentials.
                      </AlertDescription>
                    </Alert>
                  )}

                  <div className="flex items-center space-x-2">
                    <Checkbox id="terms" required />
                    <label
                      htmlFor="terms"
                      className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                    >
                      I agree to the{" "}
                      <a href="#" className="text-sky-500 hover:text-sky-600">
                        terms of service
                      </a>{" "}
                      and{" "}
                      <a href="#" className="text-sky-500 hover:text-sky-600">
                        privacy policy
                      </a>
                    </label>
                  </div>

                  <Button type="submit" className="w-full" disabled={isLoading}>
                    {isLoading ? "Creating account..." : "Create account"}
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </AuthLayout>
  )
}

export default AuthPage;
