import { Input } from "@/components/ui/input";
import { Button } from "./ui/button";
import { cn } from "@/lib/utils";

export default function Setup(
  { className }: React.ButtonHTMLAttributes<HTMLButtonElement>) {
  return (
    <div className={cn("flex flex-row items-center gap-5", className)}>
      <p className="text-lg">Stack</p>
      <Input className="max-w-40" type="number" />
      <Button variant={"outline"}> Apply </Button>
      <Button variant={"destructive"}> Reset </Button>
    </div>
  );
}