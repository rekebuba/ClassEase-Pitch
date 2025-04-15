import classEaseImage from '../assets/images/ClassEase-no-slogan.png';
import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"
import {
  CheckCircle,
  GraduationCap,
  Users,
  Calendar,
  BookOpen,
  BarChart3,
  Settings,
  ArrowRight,
  ChevronRight,
  Star,
  Shield,
  Clock,
  FileText,
  MessageSquare,
  Globe,
  Award,
  Zap,
  Phone,
  Mail,
  MapPin,
  Facebook,
  Twitter,
  Instagram,
  Linkedin,
} from "lucide-react"

export default function LandingPage() {
  const [activeTestimonial, setActiveTestimonial] = useState(0)
  const [isVisible, setIsVisible] = useState(false)

  // For the counter animation
  const [counts, setCounts] = useState({
    schools: 0,
    students: 0,
    teachers: 0,
    countries: 0,
  })

  const targetCounts = {
    schools: 500,
    students: 250000,
    teachers: 15000,
    countries: 25,
  }

  // For testimonial auto-rotation
  useEffect(() => {
    const interval = setInterval(() => {
      setActiveTestimonial((prev) => (prev + 1) % 3)
    }, 5000)
    return () => clearInterval(interval)
  }, [])

  // For counter animation when section is visible
  useEffect(() => {
    const handleScroll = () => {
      const statsSection = document.getElementById("stats-section")
      if (statsSection) {
        const rect = statsSection.getBoundingClientRect()
        const isVisible = rect.top < window.innerHeight && rect.bottom >= 0
        setIsVisible(isVisible)
      }
    }

    window.addEventListener("scroll", handleScroll)
    handleScroll() // Check on initial load

    return () => window.removeEventListener("scroll", handleScroll)
  }, [])

  // Animate the counters when section becomes visible
  useEffect(() => {
    if (isVisible) {
      const duration = 2000 // 2 seconds
      const interval = 20 // Update every 20ms
      const steps = duration / interval

      let step = 0
      const timer = setInterval(() => {
        step++
        const progress = step / steps

        setCounts({
          schools: Math.floor(targetCounts.schools * progress),
          students: Math.floor(targetCounts.students * progress),
          teachers: Math.floor(targetCounts.teachers * progress),
          countries: Math.floor(targetCounts.countries * progress),
        })

        if (step >= steps) {
          clearInterval(timer)
        }
      }, interval)

      return () => clearInterval(timer)
    }
  }, [isVisible])

  return (
    <div className="flex min-h-screen flex-col">
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center gap-2">
            <GraduationCap className="h-6 w-6 text-sky-500" />
            <span className="text-xl font-bold text-sky-500">ClassEase</span>
          </div>
          <nav className="hidden md:flex gap-6">
            <a href="#features" className="text-sm font-medium transition-colors hover:text-primary">
              Features
            </a>
            <a href="#solutions" className="text-sm font-medium transition-colors hover:text-primary">
              Solutions
            </a>
            <a href="#testimonials" className="text-sm font-medium transition-colors hover:text-primary">
              Testimonials
            </a>
            <a href="#pricing" className="text-sm font-medium transition-colors hover:text-primary">
              Pricing
            </a>
            <a href="#faq" className="text-sm font-medium transition-colors hover:text-primary">
              FAQ
            </a>
            <a href="#contact" className="text-sm font-medium transition-colors hover:text-primary">
              Contact
            </a>
          </nav>
          <div className="flex items-center gap-4">
            <a href="/auth">
              <Button variant="outline">Log in</Button>
            </a>
            <a href="/signup">
              <Button>Sign up</Button>
            </a>
          </div>
        </div>
      </header>
      <main className="flex-1">
        <section className="w-full py-12 md:py-24 lg:py-32 bg-gradient-to-b from-sky-50 to-white">
          <div className="container px-4 md:px-6">
            <div className="grid gap-6 lg:grid-cols-2 lg:gap-12 xl:grid-cols-2">
              <div className="flex flex-col justify-center space-y-4">
                <div className="space-y-2">
                  <h1 className="text-3xl font-bold tracking-tighter sm:text-5xl xl:text-6xl/none">
                    Simplify School Management with ClassEase
                  </h1>
                  <p className="max-w-[600px] text-muted-foreground md:text-xl">
                    The all-in-one platform for administrators, teachers, and students to streamline education workflows
                    and enhance learning outcomes.
                  </p>
                </div>
                <div className="flex flex-col gap-2 min-[400px]:flex-row">
                  <a href="/signup">
                    <Button size="lg" className="gap-1">
                      Get Started <ArrowRight className="h-4 w-4" />
                    </Button>
                  </a>
                  <a href="/demo">
                    <Button size="lg" variant="outline">
                      Request Demo
                    </Button>
                  </a>
                </div>
                <div className="flex items-center space-x-4 pt-4">
                  <div className="flex -space-x-2">
                    {[1, 2, 3, 4].map((i) => (
                      <div
                        key={i}
                        className="inline-block h-8 w-8 rounded-full bg-gray-200 ring-2 ring-white overflow-hidden"
                      >
                        <img
                          src={`https://randomuser.me/api/portraits/men/${i + 10}.jpg`}
                          alt="User"
                          className="h-full w-full object-cover"
                        />
                      </div>
                    ))}
                  </div>
                  <div className="text-sm text-muted-foreground">
                    Trusted by <span className="font-medium text-foreground">2,000+</span> schools worldwide
                  </div>
                </div>
              </div>
              <div className="flex items-center justify-center">
                <div className="relative">
                  <div className="absolute -top-4 -left-4 h-72 w-72 bg-sky-100 rounded-full blur-3xl opacity-30"></div>
                  <div className="absolute -bottom-4 -right-4 h-72 w-72 bg-sky-200 rounded-full blur-3xl opacity-30"></div>
                  <img
                    src={classEaseImage}
                    alt="ClassEase Dashboard Preview"
                    className="relative z-10 rounded-lg object-cover"
                    width={650}
                    height={650}
                  />
                </div>
              </div>
            </div>
          </div>
        </section>

        <section id="stats-section" className="w-full py-20 bg-gray-50 text-gray-800">
          <div className="container mx-auto px-4 md:px-6 flex flex-col items-center justify-center">
            <div className="text-center mb-12">
              <h2 className="text-3xl md:text-4xl font-bold mb-2">Empowering Education Everywhere</h2>
              <p className="text-gray-500 text-lg">Trusted globally by schools, students, and educators</p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-8 w-full max-w-5xl text-center">
              {[
                { label: "Schools", value: counts.schools },
                { label: "Students", value: counts.students },
                { label: "Teachers", value: counts.teachers },
                { label: "Countries", value: counts.countries },
              ].map((stat, i) => (
                <div
                  key={i}
                  className="bg-white rounded-xl shadow-md p-6 hover:shadow-xl transition-shadow duration-300"
                >
                  <h3 className="text-4xl font-bold text-blue-600">{stat.value.toLocaleString()}+</h3>
                  <p className="mt-2 text-gray-600">{stat.label}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section id="features" className="w-full py-12 md:py-24 lg:py-32">
          <div className="container px-4 md:px-6">
            <div className="flex flex-col items-center justify-center space-y-4 text-center">
              <div className="space-y-2">
                <div className="inline-block rounded-lg bg-sky-100 px-3 py-1 text-sm text-sky-700">Features</div>
                <h2 className="text-3xl font-bold tracking-tighter md:text-4xl/tight">
                  Everything you need to manage your school
                </h2>
                <p className="max-w-[900px] text-muted-foreground md:text-xl">
                  ClassEase provides powerful tools for administrators, teachers, and students to streamline education
                  workflows and enhance learning outcomes.
                </p>
              </div>
            </div>
            <div className="mx-auto grid max-w-5xl items-center gap-6 py-12 lg:grid-cols-3">
              {[
                {
                  icon: Users,
                  title: "User Management",
                  description: "Easily manage students, teachers, and staff accounts with role-based access control.",
                },
                {
                  icon: BookOpen,
                  title: "Curriculum Planning",
                  description: "Create, organize, and distribute curriculum materials across departments.",
                },
                {
                  icon: BarChart3,
                  title: "Performance Analytics",
                  description: "Track student performance with detailed analytics and customizable reports.",
                },
                {
                  icon: Calendar,
                  title: "Scheduling",
                  description: "Manage class schedules, events, and appointments with an intuitive calendar.",
                },
                {
                  icon: Clock,
                  title: "Attendance Tracking",
                  description: "Monitor student and teacher attendance with automated reporting.",
                },
                {
                  icon: FileText,
                  title: "Assessment Tools",
                  description: "Create, distribute, and grade assessments with powerful analytics.",
                },
                {
                  icon: MessageSquare,
                  title: "Communication",
                  description: "Connect teachers, students, and parents with integrated messaging.",
                },
                {
                  icon: Shield,
                  title: "Security & Privacy",
                  description: "Protect sensitive data with enterprise-grade security and compliance.",
                },
                {
                  icon: Settings,
                  title: "Customizable",
                  description: "Tailor the platform to your school's specific needs with flexible settings.",
                },
              ].map((feature, index) => (
                <Card key={index} className="border-0 shadow-md hover:shadow-lg transition-shadow duration-300">
                  <CardContent className="p-6 flex flex-col items-center text-center space-y-2">
                    <div className="rounded-full bg-sky-100 p-3 mb-2">
                      <feature.icon className="h-6 w-6 text-sky-500" />
                    </div>
                    <h3 className="text-xl font-bold">{feature.title}</h3>
                    <p className="text-muted-foreground">{feature.description}</p>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </section>

        <section id="solutions" className="w-full py-12 md:py-24 lg:py-32 bg-sky-50">
          <div className="container px-4 md:px-6">
            <div className="flex flex-col items-center justify-center space-y-4 text-center">
              <div className="space-y-2">
                <div className="inline-block rounded-lg bg-sky-100 px-3 py-1 text-sm text-sky-700">Solutions</div>
                <h2 className="text-3xl font-bold tracking-tighter md:text-4xl/tight">
                  Tailored for every role in education
                </h2>
                <p className="max-w-[900px] text-muted-foreground md:text-xl">
                  ClassEase offers specialized solutions for administrators, teachers, students, and parents.
                </p>
              </div>
            </div>

            <Tabs defaultValue="administrators" className="w-full max-w-4xl mx-auto mt-12">
              <TabsList className="grid w-full grid-cols-4">
                <TabsTrigger value="administrators">Administrators</TabsTrigger>
                <TabsTrigger value="teachers">Teachers</TabsTrigger>
                <TabsTrigger value="students">Students</TabsTrigger>
                <TabsTrigger value="parents">Parents</TabsTrigger>
              </TabsList>

              <TabsContent value="administrators" className="mt-6">
                <div className="grid md:grid-cols-2 gap-8 items-center">
                  <div>
                    <h3 className="text-2xl font-bold mb-4">Streamline School Administration</h3>
                    <ul className="space-y-3">
                      {[
                        "Comprehensive dashboard with real-time analytics",
                        "Automated attendance and performance tracking",
                        "Efficient staff and student management",
                        "Budget planning and financial oversight",
                        "Customizable reporting and compliance tools",
                        "Campus-wide scheduling and resource allocation",
                      ].map((item, i) => (
                        <li key={i} className="flex items-start">
                          <CheckCircle className="h-5 w-5 text-sky-500 mr-2 mt-0.5 flex-shrink-0" />
                          <span>{item}</span>
                        </li>
                      ))}
                    </ul>
                    <Button className="mt-6">
                      Learn More <ChevronRight className="h-4 w-4 ml-1" />
                    </Button>
                  </div>
                  <div className="rounded-lg overflow-hidden shadow-xl">
                    <img
                      src="/placeholder.svg?height=300&width=400"
                      alt="Administrator Dashboard"
                      className="w-full h-auto"
                    />
                  </div>
                </div>
              </TabsContent>

              <TabsContent value="teachers" className="mt-6">
                <div className="grid md:grid-cols-2 gap-8 items-center">
                  <div>
                    <h3 className="text-2xl font-bold mb-4">Empower Your Teaching</h3>
                    <ul className="space-y-3">
                      {[
                        "Intuitive lesson planning and curriculum management",
                        "Digital gradeBook with automated calculations",
                        "Attendance tracking with absence notifications",
                        "Student performance analytics and insights",
                        "Parent-teacher communication tools",
                        "Resource sharing and collaboration features",
                      ].map((item, i) => (
                        <li key={i} className="flex items-start">
                          <CheckCircle className="h-5 w-5 text-sky-500 mr-2 mt-0.5 flex-shrink-0" />
                          <span>{item}</span>
                        </li>
                      ))}
                    </ul>
                    <Button className="mt-6">
                      Learn More <ChevronRight className="h-4 w-4 ml-1" />
                    </Button>
                  </div>
                  <div className="rounded-lg overflow-hidden shadow-xl">
                    <img
                      src="/placeholder.svg?height=300&width=400"
                      alt="Teacher Dashboard"
                      className="w-full h-auto"
                    />
                  </div>
                </div>
              </TabsContent>

              <TabsContent value="students" className="mt-6">
                <div className="grid md:grid-cols-2 gap-8 items-center">
                  <div>
                    <h3 className="text-2xl font-bold mb-4">Enhance Your Learning Journey</h3>
                    <ul className="space-y-3">
                      {[
                        "Personalized student dashboard with upcoming assignments",
                        "Access to course materials and resources",
                        "Assignment submission and feedback tracking",
                        "Grade monitoring and performance insights",
                        "Calendar integration for classes and events",
                        "Collaboration tools for group projects",
                      ].map((item, i) => (
                        <li key={i} className="flex items-start">
                          <CheckCircle className="h-5 w-5 text-sky-500 mr-2 mt-0.5 flex-shrink-0" />
                          <span>{item}</span>
                        </li>
                      ))}
                    </ul>
                    <Button className="mt-6">
                      Learn More <ChevronRight className="h-4 w-4 ml-1" />
                    </Button>
                  </div>
                  <div className="rounded-lg overflow-hidden shadow-xl">
                    <img
                      src="/placeholder.svg?height=300&width=400"
                      alt="Student Dashboard"
                      className="w-full h-auto"
                    />
                  </div>
                </div>
              </TabsContent>

              <TabsContent value="parents" className="mt-6">
                <div className="grid md:grid-cols-2 gap-8 items-center">
                  <div>
                    <h3 className="text-2xl font-bold mb-4">Stay Connected with Your Child&apos;s Education</h3>
                    <ul className="space-y-3">
                      {[
                        "Real-time access to grades and attendance",
                        "Direct messaging with teachers and staff",
                        "Homework and assignment tracking",
                        "School announcements and calendar events",
                        "Permission slips and form submissions",
                        "Fee payment and financial management",
                      ].map((item, i) => (
                        <li key={i} className="flex items-start">
                          <CheckCircle className="h-5 w-5 text-sky-500 mr-2 mt-0.5 flex-shrink-0" />
                          <span>{item}</span>
                        </li>
                      ))}
                    </ul>
                    <Button className="mt-6">
                      Learn More <ChevronRight className="h-4 w-4 ml-1" />
                    </Button>
                  </div>
                  <div className="rounded-lg overflow-hidden shadow-xl">
                    <img src="/placeholder.svg?height=300&width=400" alt="Parent Dashboard" className="w-full h-auto" />
                  </div>
                </div>
              </TabsContent>
            </Tabs>
          </div>
        </section>

        <section className="w-full py-12 md:py-24 lg:py-32">
          <div className="container px-4 md:px-6">
            <div className="grid gap-6 lg:grid-cols-2 lg:gap-12 items-center">
              <div>
                <div className="inline-block rounded-lg bg-sky-100 px-3 py-1 text-sm text-sky-700 mb-4">
                  Why ClassEase
                </div>
                <h2 className="text-3xl font-bold tracking-tighter md:text-4xl/tight mb-4">
                  Transform your school with modern technology
                </h2>
                <p className="text-muted-foreground md:text-lg mb-6">
                  ClassEase brings together the best of educational technology to create a seamless, integrated platform
                  that addresses the unique challenges of school management.
                </p>

                <div className="grid gap-4">
                  {[
                    {
                      icon: Zap,
                      title: "Increased Efficiency",
                      description:
                        "Automate routine tasks and streamline workflows to save time and reduce administrative burden.",
                    },
                    {
                      icon: Globe,
                      title: "Improved Communication",
                      description: "Connect all stakeholders with integrated messaging and notification systems.",
                    },
                    {
                      icon: Award,
                      title: "Enhanced Learning Outcomes",
                      description: "Use data-driven insights to identify areas for improvement and track progress.",
                    },
                  ].map((item, i) => (
                    <div key={i} className="flex gap-4">
                      <div className="rounded-full bg-sky-100 p-2 h-10 w-10 flex items-center justify-center flex-shrink-0">
                        <item.icon className="h-5 w-5 text-sky-500" />
                      </div>
                      <div>
                        <h3 className="font-bold">{item.title}</h3>
                        <p className="text-muted-foreground">{item.description}</p>
                      </div>
                    </div>
                  ))}
                </div>

                <div className="mt-8">
                  <Button size="lg">
                    Schedule a Demo <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                </div>
              </div>

              <div className="relative">
                <div className="absolute -z-10 top-0 left-0 h-full w-full bg-gradient-to-br from-sky-100 to-sky-50 rounded-2xl transform -rotate-3"></div>
                <img
                  src="/placeholder.svg?height=500&width=600"
                  alt="ClassEase in action"
                  className="rounded-xl shadow-lg transform rotate-1"
                />
              </div>
            </div>
          </div>
        </section>


        <section id="testimonials" className="w-full py-12 md:py-24 lg:py-32 bg-sky-50 overflow-hidden">
          <div className="max-w-5xl mx-auto px-4 md:px-6 text-center">
            <div className="inline-block rounded-lg bg-sky-100 px-3 py-1 text-sm text-sky-700 mb-4">
              Testimonials
            </div>
            <h2 className="text-3xl font-bold tracking-tight md:text-4xl">
              Trusted by educators worldwide
            </h2>
            <p className="max-w-2xl mx-auto mt-4 text-muted-foreground md:text-xl">
              See what school administrators and teachers are saying about ClassEase.
            </p>

            {/* Testimonial Card */}
            <div className="relative mt-12 max-w-4xl mx-auto">
              <div className="absolute top-8 left-0 w-full h-full bg-sky-100 rounded-xl transform -rotate-1"></div>
              <div className="relative bg-white rounded-xl shadow-lg p-6 md:p-12">
                <div className="flex justify-center mb-6">
                  <div className="flex space-x-2">
                    {[0, 1, 2].map((i) => (
                      <button
                        key={i}
                        className={`h-2 rounded-full transition-all ${activeTestimonial === i ? "w-8 bg-sky-500" : "w-2 bg-sky-200"
                          }`}
                        onClick={() => setActiveTestimonial(i)}
                        aria-label={`View testimonial ${i + 1}`}
                      />
                    ))}
                  </div>
                </div>

                <div className="relative h-[250px]">
                  {[
                    {
                      quote:
                        "ClassEase has transformed how we manage our school. The administrative burden has been reduced significantly, and our teachers can focus more on teaching rather than paperwork. The analytics features have helped us identify areas for improvement and track our progress over time.",
                      name: "Sarah Johnson",
                      title: "Principal, Lincoln High School",
                      avatar: "/placeholder.svg?height=80&width=80",
                    },
                    {
                      quote:
                        "The analytics features help us identify struggling students early and provide targeted support. We've seen a 15% improvement in overall student performance since implementing ClassEase. The parent communication tools have also strengthened our school community.",
                      name: "Michael Chen",
                      title: "Department Head, Westfield Academy",
                      avatar: "/placeholder.svg?height=80&width=80",
                    },
                    {
                      quote:
                        "As a teacher, I love how easy it is to track attendance, manage grades, and communicate with parents. The lesson planning tools save me hours each week, and the student performance insights help me tailor my teaching to meet individual needs.",
                      name: "Emily Rodriguez",
                      title: "Teacher, Oakridge Elementary",
                      avatar: "/placeholder.svg?height=80&width=80",
                    },
                  ].map((testimonial, index) => (
                    <div
                      key={index}
                      className={`absolute top-0 left-0 w-full transition-opacity duration-500 ${activeTestimonial === index ? "opacity-100 z-10" : "opacity-0 z-0"
                        }`}
                    >
                      <div className="flex flex-col items-center text-center">
                        <div className="mb-6">
                          <div className="flex justify-center mb-4">
                            {[1, 2, 3, 4, 5].map((star) => (
                              <Star key={star} className="h-6 w-6 text-yellow-400 fill-yellow-400" />
                            ))}
                          </div>
                          <p className="text-lg italic text-muted-foreground mb-6">&quot;{testimonial.quote}&quot;</p>
                        </div>
                        <div className="flex flex-col items-center">
                          <div className="w-16 h-16 rounded-full overflow-hidden mb-3">
                            <img
                              src={testimonial.avatar}
                              alt={testimonial.name}
                              className="w-full h-full object-cover"
                            />
                          </div>
                          <p className="font-semibold">{testimonial.name}</p>
                          <p className="text-sm text-muted-foreground">{testimonial.title}</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Stats */}
            <div className="mt-16 grid gap-8 md:grid-cols-3">
              {[
                {
                  stat: "94%",
                  description: "of schools report improved administrative efficiency",
                },
                {
                  stat: "87%",
                  description: "of teachers save 5+ hours per week on administrative tasks",
                },
                {
                  stat: "92%",
                  description: "of parents feel more connected to their child's education",
                },
              ].map((item, i) => (
                <div key={i} className="bg-white rounded-lg p-6 text-center shadow-md">
                  <div className="text-4xl font-bold text-sky-500 mb-2">{item.stat}</div>
                  <p className="text-muted-foreground">{item.description}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section id="pricing" className="w-full py-12 md:py-24 lg:py-32">
          <div className="container px-4 md:px-6">
            <div className="flex flex-col items-center justify-center space-y-4 text-center">
              <div className="space-y-2">
                <div className="inline-block rounded-lg bg-sky-100 px-3 py-1 text-sm text-sky-700">Pricing</div>
                <h2 className="text-3xl font-bold tracking-tighter md:text-4xl/tight">Simple, transparent pricing</h2>
                <p className="max-w-[900px] text-muted-foreground md:text-xl">
                  Choose the plan that is right for your school.
                </p>
              </div>
            </div>
            <div className="mx-auto max-w-5xl py-12">
              <Tabs defaultValue="monthly" className="w-full">
                <TabsList className="grid w-full max-w-md mx-auto grid-cols-2 mb-8">
                  <TabsTrigger value="monthly">Monthly</TabsTrigger>
                  <TabsTrigger value="annually">Annually (Save 20%)</TabsTrigger>
                </TabsList>
                <TabsContent value="monthly" className="grid gap-6 md:grid-cols-3">
                  {[
                    {
                      name: "Starter",
                      price: "$99",
                      description: "Perfect for small schools",
                      features: ["Up to 500 students", "Basic analytics", "Email support", "Core features"],
                    },
                    {
                      name: "Professional",
                      price: "$199",
                      description: "Ideal for medium-sized schools",
                      features: [
                        "Up to 2,000 students",
                        "Advanced analytics",
                        "Priority support",
                        "All core features",
                        "API access",
                      ],
                      popular: true,
                    },
                    {
                      name: "Enterprise",
                      price: "Custom",
                      description: "For large school districts",
                      features: [
                        "Unlimited students",
                        "Custom integrations",
                        "Dedicated support",
                        "All features",
                        "On-premise option",
                        "Custom reporting",
                        "White labeling",
                      ],
                    },
                  ].map((plan, index) => (
                    <Card
                      key={index}
                      className={`border-0 shadow-md relative ${plan.popular ? "border-sky-500 border-2" : ""}`}
                    >
                      {plan.popular && (
                        <div className="absolute top-0 right-0 bg-sky-500 text-white text-xs font-bold px-3 py-1 rounded-bl-lg rounded-tr-lg">
                          MOST POPULAR
                        </div>
                      )}
                      <CardContent className="p-6 flex flex-col space-y-4">
                        <div>
                          <h3 className="text-xl font-bold">{plan.name}</h3>
                          <p className="text-muted-foreground text-sm">{plan.description}</p>
                        </div>
                        <div className="flex items-baseline">
                          <span className="text-3xl font-bold">{plan.price}</span>
                          <span className="text-muted-foreground ml-1">/month</span>
                        </div>
                        <ul className="space-y-2">
                          {plan.features.map((feature, i) => (
                            <li key={i} className="flex items-center">
                              <CheckCircle className="h-4 w-4 text-sky-500 mr-2" />
                              <span className="text-sm">{feature}</span>
                            </li>
                          ))}
                        </ul>
                        <Button className="mt-4" variant={plan.popular ? "default" : "outline"}>
                          {index === 2 ? "Contact Sales" : "Get Started"}
                        </Button>
                      </CardContent>
                    </Card>
                  ))}
                </TabsContent>
                <TabsContent value="annually" className="grid gap-6 md:grid-cols-3">
                  {[
                    {
                      name: "Starter",
                      price: "$79",
                      description: "Perfect for small schools",
                      features: ["Up to 500 students", "Basic analytics", "Email support", "Core features"],
                    },
                    {
                      name: "Professional",
                      price: "$159",
                      description: "Ideal for medium-sized schools",
                      features: [
                        "Up to 2,000 students",
                        "Advanced analytics",
                        "Priority support",
                        "All core features",
                        "API access",
                      ],
                      popular: true,
                    },
                    {
                      name: "Enterprise",
                      price: "Custom",
                      description: "For large school districts",
                      features: [
                        "Unlimited students",
                        "Custom integrations",
                        "Dedicated support",
                        "All features",
                        "On-premise option",
                        "Custom reporting",
                        "White labeling",
                      ],
                    },
                  ].map((plan, index) => (
                    <Card
                      key={index}
                      className={`border-0 shadow-md relative ${plan.popular ? "border-sky-500 border-2" : ""}`}
                    >
                      {plan.popular && (
                        <div className="absolute top-0 right-0 bg-sky-500 text-white text-xs font-bold px-3 py-1 rounded-bl-lg rounded-tr-lg">
                          MOST POPULAR
                        </div>
                      )}
                      <CardContent className="p-6 flex flex-col space-y-4">
                        <div>
                          <h3 className="text-xl font-bold">{plan.name}</h3>
                          <p className="text-muted-foreground text-sm">{plan.description}</p>
                        </div>
                        <div className="flex items-baseline">
                          <span className="text-3xl font-bold">{plan.price}</span>
                          <span className="text-muted-foreground ml-1">/month</span>
                        </div>
                        <ul className="space-y-2">
                          {plan.features.map((feature, i) => (
                            <li key={i} className="flex items-center">
                              <CheckCircle className="h-4 w-4 text-sky-500 mr-2" />
                              <span className="text-sm">{feature}</span>
                            </li>
                          ))}
                        </ul>
                        <Button className="mt-4" variant={plan.popular ? "default" : "outline"}>
                          {index === 2 ? "Contact Sales" : "Get Started"}
                        </Button>
                      </CardContent>
                    </Card>
                  ))}
                </TabsContent>
              </Tabs>

              <div className="mt-12 bg-sky-50 rounded-lg p-6 md:p-8">
                <div className="flex flex-col md:flex-row md:items-center gap-6">
                  <div className="md:flex-1">
                    <h3 className="text-xl font-bold mb-2">Need a custom solution?</h3>
                    <p className="text-muted-foreground">
                      We offer tailored solutions for school districts, universities, and educational organizations with
                      specific requirements.
                    </p>
                  </div>
                  <div>
                    <Button size="lg">Contact Our Sales Team</Button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section id="faq" className="w-full py-12 md:py-24 lg:py-32 bg-white">
          <div className="container px-4 md:px-6">
            <div className="flex flex-col items-center justify-center space-y-4 text-center">
              <div className="space-y-2">
                <div className="inline-block rounded-lg bg-sky-100 px-3 py-1 text-sm text-sky-700">FAQ</div>
                <h2 className="text-3xl font-bold tracking-tighter md:text-4xl/tight">Frequently Asked Questions</h2>
                <p className="max-w-[900px] text-muted-foreground md:text-xl">
                  Find answers to common questions about ClassEase.
                </p>
              </div>
            </div>

            <div className="mx-auto max-w-3xl mt-12">
              <Accordion type="single" collapsible className="w-full">
                {[
                  {
                    question: "How long does it take to implement ClassEase?",
                    answer:
                      "Most schools can be fully onboarded within 2-4 weeks, depending on the size of the institution and data migration needs. Our implementation team will work closely with you to ensure a smooth transition.",
                  },
                  {
                    question: "Is ClassEase compliant with education privacy regulations?",
                    answer:
                      "Yes, ClassEase is fully compliant with FERPA, COPPA, and other relevant education privacy regulations. We take data security and privacy seriously and implement industry-standard security measures to protect your data.",
                  },
                  {
                    question: "Can ClassEase integrate with other systems we're already using?",
                    answer:
                      "ClassEase offers robust API capabilities and pre-built integrations with popular education tools, student information systems, and learning management systems. Our team can help you set up custom integrations as needed.",
                  },
                  {
                    question: "What kind of support does ClassEase provide?",
                    answer:
                      "All plans include access to our knowledge base, community forums, and email support. Professional and Enterprise plans include priority support with faster response times, and Enterprise customers receive dedicated support with a named account manager.",
                  },
                  {
                    question: "Can we migrate our existing data to ClassEase?",
                    answer:
                      "Yes, we offer comprehensive data migration services to help you transfer student records, course information, and other essential data from your current systems to ClassEase. Our team will work with you to ensure data integrity throughout the process.",
                  },
                  {
                    question: "Is ClassEase accessible for users with disabilities?",
                    answer:
                      "ClassEase is designed with accessibility in mind and complies with WCAG 2.1 guidelines. We regularly test our platform with assistive technologies to ensure all users can effectively use our system.",
                  },
                ].map((item, i) => (
                  <AccordionItem key={i} value={`item-${i}`}>
                    <AccordionTrigger className="text-left">{item.question}</AccordionTrigger>
                    <AccordionContent>{item.answer}</AccordionContent>
                  </AccordionItem>
                ))}
              </Accordion>

              <div className="mt-8 text-center">
                <p className="text-muted-foreground mb-4">Still have questions? We are here to help.</p>
                <Button variant="outline">Contact Support</Button>
              </div>
            </div>
          </div>
        </section>

        <section id="contact" className="w-full py-12 md:py-24 lg:py-32 bg-sky-50">
          <div className="container px-4 md:px-6">
            <div className="grid gap-6 lg:grid-cols-2 lg:gap-12">
              <div className="flex flex-col justify-center space-y-4">
                <div className="space-y-2">
                  <div className="inline-block rounded-lg bg-sky-100 px-3 py-1 text-sm text-sky-700">Contact Us</div>
                  <h2 className="text-3xl font-bold tracking-tighter md:text-4xl/tight">
                    Ready to transform your school?
                  </h2>
                  <p className="max-w-[600px] text-muted-foreground md:text-xl">
                    Our team is here to answer your questions and help you get started with ClassEase.
                  </p>
                </div>
                <div className="space-y-4 mt-6">
                  <div className="flex items-center space-x-3">
                    <div className="rounded-full bg-sky-100 p-2">
                      <Phone className="h-4 w-4 text-sky-700" />
                    </div>
                    <div className="text-sm">
                      <p className="font-medium">Phone</p>
                      <p className="text-muted-foreground">+1 (555) 123-4567</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-3">
                    <div className="rounded-full bg-sky-100 p-2">
                      <Mail className="h-4 w-4 text-sky-700" />
                    </div>
                    <div className="text-sm">
                      <p className="font-medium">Email</p>
                      <p className="text-muted-foreground">info@classease.com</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-3">
                    <div className="rounded-full bg-sky-100 p-2">
                      <MapPin className="h-4 w-4 text-sky-700" />
                    </div>
                    <div className="text-sm">
                      <p className="font-medium">Address</p>
                      <p className="text-muted-foreground">123 Education Lane, Suite 400, San Francisco, CA 94107</p>
                    </div>
                  </div>
                </div>

                <div className="mt-6">
                  <h3 className="text-lg font-semibold mb-3">Follow Us</h3>
                  <div className="flex space-x-4">
                    <a href="#" className="rounded-full bg-sky-100 p-2 hover:bg-sky-200 transition-colors">
                      <Facebook className="h-5 w-5 text-sky-700" />
                    </a>
                    <a href="#" className="rounded-full bg-sky-100 p-2 hover:bg-sky-200 transition-colors">
                      <Twitter className="h-5 w-5 text-sky-700" />
                    </a>
                    <a href="#" className="rounded-full bg-sky-100 p-2 hover:bg-sky-200 transition-colors">
                      <Instagram className="h-5 w-5 text-sky-700" />
                    </a>
                    <a href="#" className="rounded-full bg-sky-100 p-2 hover:bg-sky-200 transition-colors">
                      <Linkedin className="h-5 w-5 text-sky-700" />
                    </a>
                  </div>
                </div>
              </div>
              <div className="flex items-center justify-center">
                <Card className="w-full max-w-md border-0 shadow-lg">
                  <CardContent className="p-6">
                    <form className="space-y-4">
                      <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                          <label htmlFor="first-name" className="text-sm font-medium">
                            First name
                          </label>
                          <input
                            id="first-name"
                            className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                            placeholder="John"
                          />
                        </div>
                        <div className="space-y-2">
                          <label htmlFor="last-name" className="text-sm font-medium">
                            Last name
                          </label>
                          <input
                            id="last-name"
                            className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                            placeholder="Doe"
                          />
                        </div>
                      </div>
                      <div className="space-y-2">
                        <label htmlFor="email" className="text-sm font-medium">
                          Email
                        </label>
                        <input
                          id="email"
                          type="email"
                          className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                          placeholder="john.doe@example.com"
                        />
                      </div>
                      <div className="space-y-2">
                        <label htmlFor="school" className="text-sm font-medium">
                          School Name
                        </label>
                        <input
                          id="school"
                          className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                          placeholder="Westfield Academy"
                        />
                      </div>
                      <div className="space-y-2">
                        <label htmlFor="interest" className="text-sm font-medium">
                          I&apos;m interested in
                        </label>
                        <select
                          id="interest"
                          className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                        >
                          <option value="">Select an option</option>
                          <option value="demo">Scheduling a demo</option>
                          <option value="quote">Getting a quote</option>
                          <option value="trial">Starting a free trial</option>
                          <option value="question">General question</option>
                        </select>
                      </div>
                      <div className="space-y-2">
                        <label htmlFor="message" className="text-sm font-medium">
                          Message
                        </label>
                        <textarea
                          id="message"
                          className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm min-h-[100px]"
                          placeholder="Tell us about your school and requirements..."
                        />
                      </div>
                      <Button className="w-full">Send Message</Button>
                    </form>
                  </CardContent>
                </Card>
              </div>
            </div>
          </div>
        </section>
      </main>
      <footer className="w-full border-t py-12 bg-gray-50">
        <div className="container px-4 md:px-6">
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-8">
            <div className="col-span-2 lg:col-span-1">
              <div className="flex items-center gap-2 mb-4">
                <GraduationCap className="h-6 w-6 text-sky-500" />
                <span className="text-xl font-bold text-sky-500">ClassEase</span>
              </div>
              <p className="text-sm text-muted-foreground mb-4">
                Simplifying school management and enhancing education through innovative technology.
              </p>
              <div className="flex space-x-4">
                <a href="#" className="text-muted-foreground hover:text-sky-500">
                  <Facebook className="h-5 w-5" />
                </a>
                <a href="#" className="text-muted-foreground hover:text-sky-500">
                  <Twitter className="h-5 w-5" />
                </a>
                <a href="#" className="text-muted-foreground hover:text-sky-500">
                  <Instagram className="h-5 w-5" />
                </a>
                <a href="#" className="text-muted-foreground hover:text-sky-500">
                  <Linkedin className="h-5 w-5" />
                </a>
              </div>
            </div>

            <div>
              <h3 className="font-semibold mb-4">Product</h3>
              <ul className="space-y-2">
                <li>
                  <a href="#" className="text-sm text-muted-foreground hover:text-sky-500">
                    Features
                  </a>
                </li>
                <li>
                  <a href="#" className="text-sm text-muted-foreground hover:text-sky-500">
                    Solutions
                  </a>
                </li>
                <li>
                  <a href="#" className="text-sm text-muted-foreground hover:text-sky-500">
                    Pricing
                  </a>
                </li>
                <li>
                  <a href="#" className="text-sm text-muted-foreground hover:text-sky-500">
                    Updates
                  </a>
                </li>
                <li>
                  <a href="#" className="text-sm text-muted-foreground hover:text-sky-500">
                    Roadmap
                  </a>
                </li>
              </ul>
            </div>

            <div>
              <h3 className="font-semibold mb-4">Resources</h3>
              <ul className="space-y-2">
                <li>
                  <a href="#" className="text-sm text-muted-foreground hover:text-sky-500">
                    Blog
                  </a>
                </li>
                <li>
                  <a href="#" className="text-sm text-muted-foreground hover:text-sky-500">
                    Documentation
                  </a>
                </li>
                <li>
                  <a href="#" className="text-sm text-muted-foreground hover:text-sky-500">
                    Help Center
                  </a>
                </li>
                <li>
                  <a href="#" className="text-sm text-muted-foreground hover:text-sky-500">
                    Webinars
                  </a>
                </li>
                <li>
                  <a href="#" className="text-sm text-muted-foreground hover:text-sky-500">
                    Case Studies
                  </a>
                </li>
              </ul>
            </div>

            <div>
              <h3 className="font-semibold mb-4">Company</h3>
              <ul className="space-y-2">
                <li>
                  <a href="#" className="text-sm text-muted-foreground hover:text-sky-500">
                    About Us
                  </a>
                </li>
                <li>
                  <a href="#" className="text-sm text-muted-foreground hover:text-sky-500">
                    Careers
                  </a>
                </li>
                <li>
                  <a href="#" className="text-sm text-muted-foreground hover:text-sky-500">
                    Partners
                  </a>
                </li>
                <li>
                  <a href="#" className="text-sm text-muted-foreground hover:text-sky-500">
                    Contact
                  </a>
                </li>
              </ul>
            </div>

            <div>
              <h3 className="font-semibold mb-4">Legal</h3>
              <ul className="space-y-2">
                <li>
                  <a href="#" className="text-sm text-muted-foreground hover:text-sky-500">
                    Terms of Service
                  </a>
                </li>
                <li>
                  <a href="#" className="text-sm text-muted-foreground hover:text-sky-500">
                    Privacy Policy
                  </a>
                </li>
                <li>
                  <a href="#" className="text-sm text-muted-foreground hover:text-sky-500">
                    Cookie Policy
                  </a>
                </li>
                <li>
                  <a href="#" className="text-sm text-muted-foreground hover:text-sky-500">
                    GDPR
                  </a>
                </li>
              </ul>
            </div>
          </div>

        </div>
        <div className="mt-12 pt-8 border-t px-5 md:px-7">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <p className="text-sm text-muted-foreground">
              © {new Date().getFullYear()} ClassEase. All rights reserved.
            </p>
            <div className="mt-4 md:mt-0">
              <select className="text-sm bg-transparent border rounded px-2 py-1 text-muted-foreground">
                <option value="en">English</option>
                <option value="es">Español</option>
                <option value="fr">Français</option>
                <option value="de">Deutsch</option>
              </select>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
