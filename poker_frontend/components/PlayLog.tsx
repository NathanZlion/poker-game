'use client';

import { useAppSelector } from "@/lib/hooks";
import { cn } from "@/lib/utils";
import { useEffect } from "react";
import { ScrollArea } from "./ui/scroll-area";

export default function PlayLog(
    { className }: React.ButtonHTMLAttributes<HTMLButtonElement>) {

    const { handId, logs, loading, gameHasEnded, pot_amount } = useAppSelector(state => state.hand);
    const _s = useAppSelector(state => state.hand);

    useEffect(() => {
        // Scroll to bottom
        const scroll = document.getElementById("scroll-to-bottom");
        if (scroll) scroll.scrollIntoView({ behavior: "smooth" });
    }, [_s.logs]);

    return (
        <ScrollArea className={cn("", className)} id="play-logs-wrapper">
            {
                logs.map((log, index) => {
                    return (
                        <p key={`playlog_${index}`} className="block"> {log} </p>
                    );
                })
            }

            {/* loading new logs showed */}
            {loading == "pending" ? <p className="block" id="loading-indicator">...</p> : ""}

            {/* Before the game has started */}
            {loading == "idle" && logs.length === 0 && <p className="block">Game not started.</p>}

            {/* Game ended */}
            {
                gameHasEnded && (
                    <div>
                        <p className="font-bold block"> {`Hand #${handId} ended`} </p>
                        <p className="font-bold block"> {`Final pot  was ${pot_amount}.`} </p>
                    </div>
                )
            }

            { /* This is a hack to scroll to bottom of the div whenever there is a new log added */}
            <div id="scroll-to-bottom"></div>
        </ScrollArea>
    );
}