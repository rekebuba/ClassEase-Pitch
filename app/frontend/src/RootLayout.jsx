import { Toaster } from "@/components/ui/toaster";

export default function RootLayout({ children }) {
    return (
        <div>
            <main>{children}</main>
            <Toaster />
        </div>
    );
}
