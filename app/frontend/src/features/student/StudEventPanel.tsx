import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

const StudentEventPanel = ({ events }) => {
  return (
    <div className="flex flex-col space-y-10">
      {/* Upcoming Events */}
      <Card className="w-[35rem] h-auto">
        <CardHeader>
          <CardTitle>Upcoming Events</CardTitle>
          <CardDescription>Events Description</CardDescription>
        </CardHeader>
        <CardContent className="p-4">
          <div className="flex items-center space-x-4">
            <div className="bg-red-500 text-white p-2 rounded-lg">
              <p className="text-lg font-bold">Feb</p>
              <p className="text-xl font-extrabold">21</p>
            </div>
            <div>
              <p className="font-medium">
                #ALX_SE last chance - how to optimize for your learning + Q&A w
                Julien
              </p>
              <p className="text-gray-500 text-sm">🕒 7:00 PM</p>
              <a
                href="https://x.com/i/spaces/1rmxPyaWBAmKN"
                className="text-blue-500 hover:underline text-sm"
              >
                Join here
              </a>
            </div>
          </div>
        </CardContent>
      </Card>
      {/* Current Projects */}
      <Card className=" md:col-span-2">
        <CardHeader>
          <CardTitle className="text-red-400">Announcement</CardTitle>
          <CardDescription>Description</CardDescription>
        </CardHeader>
        <CardContent className="p-4">
          <h2 className="text-lg font-semibold mb-2">Current projects</h2>
          <p className="text-gray-500">None, enjoy the silence.</p>
        </CardContent>
      </Card>
    </div>
  );
};

export default StudentEventPanel;
