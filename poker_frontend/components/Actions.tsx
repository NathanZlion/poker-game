'use client'

import { cn } from "@/lib/utils";
import { Button } from "./ui/button";
import { useAppDispatch, useAppSelector } from "@/lib/hooks";
import { performAction } from "@/lib/feature/hand/handSlice";

export default function Actions(
    { className }: React.ButtonHTMLAttributes<HTMLButtonElement>) {

    const dispatch = useAppDispatch();
    const {
        loading,
        betSize,
        allowedActions,
        raiseSize
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
                disabled={actionPending || !allowedActions.includes("CHECK")}
                onClick={() => { dispatch(performAction({ actionType: "CHECK" })) }}
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
                onClick={() => { dispatch({ type: 'handSlice/decrementBetSize' }) }}
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
                onClick={() => { dispatch({ type: 'handSlice/incrementBetSize' }) }}
                disabled={actionPending || !allowedActions.includes("BET")}
            >
                +
            </Button>

            <Button
                variant={"outline"} className="bg-orange-400"
                disabled={actionPending || !allowedActions.includes("RAISE")}
                onClick={() => { dispatch({ type: 'handSlice/decrementRaiseSize' }) }}
            >
                -
            </Button>

            <Button
                variant={"outline"} className="bg-orange-400"
                onClick={() => { dispatch(performAction({ actionType: "RAISE", amount: betSize })) }}
                disabled={actionPending || !allowedActions.includes("RAISE")}
            >
                Raise {raiseSize}

            </Button>

            <Button
                variant={"outline"} className="bg-orange-400"
                disabled={actionPending || !allowedActions.includes("RAISE")}
            >
                +
            </Button>

            <Button
                variant={"outline"} className="bg-destructive"
                disabled={actionPending || !allowedActions.includes("ALLIN")}
            >
                Allin
            </Button>
        </div>
    );
}