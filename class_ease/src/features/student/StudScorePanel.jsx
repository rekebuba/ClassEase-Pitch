import { useState } from "react";
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"
import { Calendar, AlertCircle, CheckCircle } from "lucide-react";
import { studentApi } from "@/api";

const StudentScorePanel = ({ yearlyScore, isAssesOpen }) => {

    return (
        <div className="flex flex-col space-y-10">
            {/* Reports */}
            <Card className="w-[35rem]">
                <CardContent className="p-4 flex justify-between items-center">
                    <h2 className="text-lg font-semibold">Reports</h2>
                    <p className="text-red-500 flex items-center cursor-pointer hover:underline">
                        <AlertCircle className="h-5 w-5 mr-1" /> 1 report
                    </p>
                </CardContent>
            </Card>

            {/* Scores */}
            <Card className=" lg:col-span-2">
                <CardContent className="p-4">
                    <div className="flex justify-between items-center mb-3">
                        <h2 className="text-lg font-semibold">Scores - Short Specializations &nbsp;
                            <span className="bg-green-500 text-white px-2 py-1 text-sm rounded-lg">Validated</span>
                        </h2>
                        <p className="text-xl font-bold">134.88%</p>
                    </div>
                    <p
                    className="text-red-500 hover:underline text-sm cursor-pointer text-right"
                    onClick={() => isAssesOpen(true)}
                    >Score details</p>
                    <div className="mt-3 space-y-2">
                        {yearlyScore && yearlyScore.map((item, index) => (
                            <div key={index} className={`flex justify-between border-b-2 border-gray-100 pb-2 ${index === 0 ? 'border-t-2' : ''}`}>
                                <p>Grade {item.grade}</p>
                                <p className="flex items-center">
                                    {item.final_score}% <CheckCircle className="h-5 w-5 text-green-500 ml-1" />
                                </p>
                            </div>
                        ))}
                    </div>
                </CardContent>
            </Card>
        </div>
    )
};

export default StudentScorePanel;
