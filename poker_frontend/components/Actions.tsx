'use client'

import { cn } from "@/lib/utils";
import { Button } from "./ui/button";
import { useAppDispatch, useAppSelector } from "@/lib/hooks";
import { performAction } from "@/lib/feature/hand/handSlice";
import { increaseRaiseSize, increaseBetSize, decreaseBetSize, decreaseRaiseSize } from "@/lib/feature/hand/handSlice";

export default function Actions(
    { className }: React.ButtonHTMLAttributes<HTMLButtonElement>) {

    const dispatch = useAppDispatch();
    const {
        loading,
        betSize,
        raiseSize,
        allowedActions,
    } = useAppSelector((state) => state.hand);
    const actionPending = loading === 'pending';

    return (
        <div className={cn("flex flex-row justify-start gap-2 ps-5", className)}>
            <Button variant={"outline"}
                className="bg-blue-400"
                disabled={actionPending || !allowedActions.includes("FOLD")}
                onClick={() => { dispatch(performAction({ actionType: "FOLD" })) }}
            >
                Fold
            </Button>

            <Button
                variant={"outline"} className="bg-green-400"
                onClick={() => { dispatch(performAction({ actionType: "CHECK" })) }}
                disabled={actionPending || !allowedActions.includes("CHECK")}
            >
                Check
            </Button>

            <Button
                variant={"outline"} className="bg-green-400"
                onClick={() => { dispatch(performAction({ actionType: "CALL" })) }}
                disabled={actionPending || !allowedActions.includes("CALL")}
            >
                Call
            </Button>

            <Button
                variant={"outline"} className="bg-orange-400"
                onClick={() => { dispatch(decreaseBetSize()) }}
                disabled={actionPending || !allowedActions.includes("BET")}
            >
                -
            </Button>

            <Button
                variant={"outline"} className="bg-orange-400"
                onClick={() => { dispatch(performAction({ actionType: "BET", amount: betSize })) }}
                disabled={actionPending || !allowedActions.includes("BET")}
            >
                Bet {betSize}
            </Button>

            <Button
                variant={"outline"} className="bg-orange-400"
                onClick={() => { dispatch(increaseBetSize()) }}
                disabled={actionPending || !allowedActions.includes("BET")}
            >
                +
            </Button>

            <Button
                variant={"outline"} className="bg-orange-400"
                onClick={() => { dispatch(decreaseRaiseSize()) }}
                disabled={actionPending || !allowedActions.includes("RAISE")}
            >
                -
            </Button>

            <Button
                variant={"outline"} className="bg-orange-400"
                onClick={() => { dispatch(performAction({ actionType: "RAISE", amount: raiseSize })) }}
                disabled={actionPending || !allowedActions.includes("RAISE")}
            >
                Raise {raiseSize}

            </Button>

            <Button
                variant={"outline"} className="bg-orange-400"
                onClick={() => { dispatch(increaseRaiseSize()) }}
                disabled={actionPending || !allowedActions.includes("RAISE")}
            >
                +
            </Button>

            <Button
                variant={"outline"} className="bg-destructive"
                onClick={() => { dispatch(performAction({ actionType: "ALL_IN" })) }}
                disabled={actionPending || !allowedActions.includes("ALL_IN")}
            >
                Allin
            </Button>
        </div>
    );
}