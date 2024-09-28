'use client';

import { Input } from "@/components/ui/input";
import { Button } from "./ui/button";
import { cn } from "@/lib/utils";
import { useAppDispatch, useAppSelector, useAppStore } from "@/lib/hooks";

export default function Setup(
  { className }: React.ButtonHTMLAttributes<HTMLButtonElement>) {

  const { handId } = useAppSelector(state => state.hand);

  return (
    <div className={cn("flex flex-row items-center gap-5", className)}>
      <p className="text-lg">Stack</p>

      <Input className="max-w-40" type="number" />
      <Button variant={"outline"}> Apply </Button>

      <Button
        className={cn("text-white", handId == null ? "bg-green-500" : "bg-red-500")}
        variant={handId == null ? "outline" : "destructive"}
      >
        {
          handId == null ? "Start" : "Reset"
        }
      </Button>
    </div>
  );
}