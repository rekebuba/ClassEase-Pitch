import { GraduationCap } from "lucide-react"

export default function AuthLayout({ children }: { children: React.ReactNode }) {
    return (
        <div className="min-h-screen flex">
            {/* Left side - Fixed Sidebar */}
            <div className="hidden lg:block lg:w-1/2 fixed top-0 left-0 bottom-0 bg-sky-500 text-white p-12 flex-col justify-between overflow-hidden">
                <div className="absolute inset-0 bg-sky-600 opacity-20">
                    {/* Background pattern */}
                    <svg
                        className="absolute inset-0 h-full w-full"
                        xmlns="http://www.w3.org/2000/svg"
                        width="100%"
                        height="100%"
                        viewBox="0 0 800 800"
                    >
                        <rect fill="none" width="800" height="800" />
                        <g>
                            <circle fill="rgba(255,255,255,0.05)" cx="400" cy="400" r="600" />
                            <circle fill="rgba(255,255,255,0.05)" cx="400" cy="400" r="500" />
                            <circle fill="rgba(255,255,255,0.05)" cx="400" cy="400" r="400" />
                            <circle fill="rgba(255,255,255,0.05)" cx="400" cy="400" r="300" />
                            <circle fill="rgba(255,255,255,0.05)" cx="400" cy="400" r="200" />
                            <circle fill="rgba(255,255,255,0.05)" cx="400" cy="400" r="100" />
                        </g>
                    </svg>
                </div>

                <div className="relative z-10 h-full flex flex-col justify-between">
                    <div className="flex items-center gap-2 mb-12">
                        <GraduationCap className="h-10 w-10 text-white" />
                        <span className="text-3xl font-bold text-white">ClassEase</span>
                    </div>

                    <div className="space-y-6">
                        <h1 className="text-4xl font-bold">Welcome to ClassEase</h1>
                        <p className="text-xl text-sky-100">
                            The all-in-one platform for administrators, teachers, and students to streamline education workflows.
                        </p>
                    </div>

                    <div className="space-y-8">
                        <div className="grid grid-cols-2 gap-4">
                            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
                                <div className="font-bold text-2xl mb-1">500+</div>
                                <div className="text-sky-100">Schools</div>
                            </div>
                            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
                                <div className="font-bold text-2xl mb-1">250k+</div>
                                <div className="text-sky-100">Students</div>
                            </div>
                            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
                                <div className="font-bold text-2xl mb-1">15k+</div>
                                <div className="text-sky-100">Teachers</div>
                            </div>
                            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
                                <div className="font-bold text-2xl mb-1">25+</div>
                                <div className="text-sky-100">Countries</div>
                            </div>
                        </div>

                        <div className="flex items-center gap-4">
                            <img
                                src="/placeholder.svg?height=48&width=48"
                                alt="User"
                                className="rounded-full border-2 border-white h-12 w-12"
                            />
                            <div>
                                <p className="font-medium">"ClassEase has transformed how we manage our school."</p>
                                <p className="text-sm text-sky-100">Sarah Johnson, Principal</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Right side - Scrollable content */}
            <div className="w-full lg:ml-[50%] min-h-screen flex items-center justify-center p-8">
                <div className="w-full max-w-md">{children}</div>
            </div>
        </div>
    )
}
