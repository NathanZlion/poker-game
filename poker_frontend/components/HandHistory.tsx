'use client'

import { useAppDispatch, useAppSelector } from "@/lib/hooks";
import { cn } from "@/lib/utils";
import { fetchHandHistory } from "@/lib/feature/handHistory/handHistorySlice";
import { useEffect } from "react";
import { ScrollArea } from "@radix-ui/react-scroll-area";


export default function HandHistory(
    { className }: React.ButtonHTMLAttributes<HTMLButtonElement>) {

    const dispatch = useAppDispatch();
    const { loading, value: handHistories } = useAppSelector((state) => state.history);

    useEffect(() => {
        dispatch(fetchHandHistory());
    }, []);

    return (
        <ScrollArea className={cn("", className) }>
            
            {/* the list of histories */}
            {
                handHistories.map((handHistory, index) => {
                    return (
                        <div key={`hand_history_${index}`} className="my-3 bg-blue-200 dark:bg-blue-800 p-4">
                            <p className="text-wrap"> Hand #{handHistory.id}</p>
                            <p className="text-wrap"> Stack: {handHistory.stack}; Dealer: {handHistory.dealer}; Big Blind: {handHistory.big_blind_player}; Small Blind: {handHistory.small_blind_player} </p>
                            <p className="text-wrap"> Hands : {
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
                    );
                })
            }
        </ScrollArea>
    );
}