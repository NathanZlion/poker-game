'use client';

import { Input } from "@/components/ui/input";
import { Button } from "./ui/button";
import { cn } from "@/lib/utils";
import { useAppDispatch, useAppSelector } from "@/lib/hooks";
import { handSlice, startHand } from "@/lib/feature/hand/handSlice";

export default function Setup(
  { className }: React.ButtonHTMLAttributes<HTMLButtonElement>) {

  const { handId, stack } = useAppSelector(state => state.hand);
  const dispatch = useAppDispatch();

  return (
    <div className={cn("flex flex-row items-center gap-5", className)}>
      <p className="text-lg">Stack</p>

      <Input className="max-w-40" type="number" value={stack} onChange={(e) => {
        dispatch(handSlice.actions.setStack(parseInt(e.target.value)));
      }}/>
      <Button variant={"outline"}> Apply </Button>

      <Button
        className={cn("text-white", handId == null ? "bg-green-500" : "bg-red-500")}
        variant={handId == null ? "outline" : "destructive"}
        onClick={() => {
          dispatch(startHand(stack));
        }}
      >
        {
          handId == null ? "Start" : "Reset"
        }
      </Button>
    </div>
  );
}