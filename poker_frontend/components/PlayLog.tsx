import { cn } from "@/lib/utils";

export default function PlayLog(
    { className }: React.ButtonHTMLAttributes<HTMLButtonElement>) {
    return (
        <div className={cn("flex flex-row", className)}>
            PlayLog goes here
        </div>
    );
}