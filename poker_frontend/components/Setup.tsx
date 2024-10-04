'use client';

import { Input } from "@/components/ui/input";
import { Button } from "./ui/button";
import { cn } from "@/lib/utils";
import { useAppDispatch, useAppSelector } from "@/lib/hooks";
import { handSlice, startHand } from "@/lib/feature/hand/handSlice";

export default function Setup(
  { className }: React.ButtonHTMLAttributes<HTMLButtonElement>) {

  const { handId, stack, loading } = useAppSelector(state => state.hand);
  const dispatch = useAppDispatch();

  return (
    <div className={cn("flex flex-row items-center gap-5", className)}>
      <p className="text-lg" data-testid="setup.stack-title">Stack</p>

      <Input
        className="max-w-40"
        type="number"
        value={stack}
        onChange={(e) => {
          dispatch(handSlice.actions.setStack(parseInt(e.target.value)));
        }}
        data-testid="setup.stack-size-input"
      />

      <Button variant={"outline"} data-testid="setup.apply-btn"> Apply </Button>

      <Button
        className={cn("text-white", handId == null ? "bg-green-500" : "bg-red-500")}
        variant={handId == null ? "outline" : "destructive"}
        disabled={loading === "pending"}
        onClick={() => {
          dispatch(startHand(stack));
        }}
        data-testid="setup.start-btn"
      >
        {
          handId == null ? "Start" : "Reset"
        }
      </Button>
    </div>
  );
}