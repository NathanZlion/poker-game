'use client'

import { cn } from "@/lib/utils";
import { Button } from "./ui/button";
import { useAppDispatch, useAppSelector } from "@/lib/hooks";
import { action } from "@/lib/feature/hand/handSlice";

export default function Actions(
    { className }: React.ButtonHTMLAttributes<HTMLButtonElement>) {

    const dispatch = useAppDispatch();
    const {
        loading,
        canAllIn,
        betSize,
        canBet,
        canCall,
        canCheck,
        canFold,
        canRaise,
        raiseSize
    } = useAppSelector((state) => state.hand);
    const actionPending = loading == 'pending';

    return (
        <div className={cn("flex flex-row justify-start gap-2 ps-5", className)}>
            <Button variant={"outline"}
                className="bg-blue-400" disabled={actionPending || !canFold}
                onClick={() => { dispatch(action({ actionType: "Fold" })) }}
            >
                Fold
            </Button>

            <Button
                variant={"outline"} className="bg-green-400"
                disabled={actionPending || !canCheck}
                onClick={() => { dispatch(action({ actionType: "Fold" })) }}
            >
                Check
            </Button>

            <Button
                variant={"outline"} className="bg-green-400"
                onClick={() => { dispatch(action({ actionType: "Call" })) }}
                disabled={actionPending || !canCall}
            >
                Call
            </Button>

            <Button
                variant={"outline"} className="bg-orange-400"
                onClick={() => { dispatch({ type: 'handSlice/decrementBetSize' }) }}
                disabled={actionPending || !canBet}
            >
                -
            </Button>

            <Button
                variant={"outline"} className="bg-orange-400"
                onClick={() => { dispatch(action({ actionType: "Bet", amount: betSize })) }}
                disabled={actionPending || !canBet}
            >
                Bet {betSize}
            </Button>

            <Button
                variant={"outline"} className="bg-orange-400"
                onClick={() => { dispatch({ type: 'handSlice/incrementBetSize' }) }}
                disabled={actionPending || !canBet}
            >
                +
            </Button>

            <Button
                variant={"outline"} className="bg-orange-400"
                disabled={actionPending || !canRaise}
                onClick={() => { dispatch({ type: 'handSlice/decrementRaiseSize' }) }}
            >
                -
            </Button>

            <Button
                variant={"outline"} className="bg-orange-400"
                onClick={() => { dispatch(action({ actionType: "Raise", amount: betSize })) }}
                disabled={actionPending || !canRaise}
            >
                Raise {raiseSize}

            </Button>

            <Button
                variant={"outline"} className="bg-orange-400"
                disabled={actionPending || !canRaise}
            >
                +
            </Button>

            <Button
                variant={"outline"} className="bg-destructive"
                disabled={actionPending || !canAllIn}
            >
                Allin
            </Button>

            {/*
                <div>
                    <div>{count}</div>
                    <button onClick={() => {
                        dispatch({ type: 'counter/incremented' })
                    }}>+</button>
                </div>
            */}

        </div>
    );
}