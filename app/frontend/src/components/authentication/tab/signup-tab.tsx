import {
    Card,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";

export default function SignupTab() {
  return (
    <Card className="border-0 shadow-lg animate-fade-left">
      <CardHeader className="space-y-1">
        <CardTitle className="text-2xl font-bold text-center">
          Create an account
        </CardTitle>
        <CardDescription className="text-center">
          This Feature is under development. Please check back later.
        </CardDescription>
      </CardHeader>
    </Card>
  );
}
