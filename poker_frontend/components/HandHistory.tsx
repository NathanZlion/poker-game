'use client'

import { useAppDispatch, useAppSelector } from "@/lib/hooks";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { IoReload } from "react-icons/io5";
import { fetchHandHistory } from "@/lib/feature/handHistory/handHistorySlice";
import { useEffect } from "react";


export default function HandHistory(
    { className }: React.ButtonHTMLAttributes<HTMLButtonElement>) {
    
    const dispatch = useAppDispatch();
    const { loading, value : handHistories } = useAppSelector((state) => state.history);

    useEffect(()=>{
        dispatch(fetchHandHistory());
    }, []);


    return (
        <div className={cn("bg-secondary p-4 relative", className)}>

            {/* loading indicatior bar at the top */}
            <div
                className={cn(
                    "absolute top-0 left-0 w-full h-1 bg-blue-400 animate-pulse",
                    loading == "pending" ? "block" : "hidden"
                )}
            >
            </div>

            <div className="flex justify-end">
                <Button
                    className="ms-auto"
                    variant={"ghost"}
                    onClick={() => dispatch(fetchHandHistory())}
                >
                    < IoReload />
                </Button>
            </div>

            <div className="text-xl px-2"> Hand History</div>

            {
                handHistories.map((handHistory, index) => (
                    <div key={index} className={cn("flex flex-col gap-3 p-3", loading == "pending" ? "animate-pulse" : "")}>
                        <div className="container p-3 bg-blue-200 dark:bg-blue-800">
                            <p> Hand #{handHistory.id}</p>
                            <p> Stack: {handHistory.stack}; Dealer: {handHistory.dealer}; Big Blind: {handHistory.big_blind_player}; Small Blind: {handHistory.small_blind_player} </p>
                            <p> Hands : {
                                Object.entries(handHistory.hands).map((
                                    [player, hand]
                                ) => {
                                    return `${player}: ${hand}; `
                                })
                            }
                            </p>
                            <p>Actions: {handHistory.actions}</p>
                            <p> Winnings : {
                                Object.entries(handHistory.winnings).map((
                                    [player, winning]
                                ) => {
                                    // Ensure the winning has a sign infront of it
                                    const formattedWinning = winning > 0 ? `+${winning}` : `${winning}`;
                                    return `${player}: ${formattedWinning}; `
                                })
                            }
                            </p>
                        </div>
                    </div>
                ))
            }
        </div>
    );
}