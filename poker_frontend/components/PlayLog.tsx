'use client';

import { useAppSelector } from "@/lib/hooks";
import { cn } from "@/lib/utils";
import { useEffect } from "react";

export default function PlayLog(
    { className }: React.ButtonHTMLAttributes<HTMLButtonElement>) {

  const { handId, logs, loading, gameHasEnded, lastPotAmount } = useAppSelector(state => state.hand);
  const _s = useAppSelector(state => state.hand);

    useEffect(() => {
        // Scroll to bottom
        const scroll = document.getElementById("scroll-to-bottom");
        if (scroll) scroll.scrollIntoView({ behavior: "smooth" });
    }, [_s.logs]);

    return (
        <div className={cn("flex flex-col", className)}>

            {
                logs.map((log, index)=>{
                    return (
                        <p key={`playlog_${index}`} className="block"> {log} </p>
                    );
                })
            }

            {/* loading new logs showed */}
            {loading == "pending" ? <p className="block">...</p> : ""}

            {/* Before the game has started */}
            {loading == "idle" && logs.length === 0 && <p className="block">Game not started.</p>}

            {/* Game ended */}
            {
                gameHasEnded && (
                    <div>
                        <p className="font-bold block"> {`Hand #${handId} ended`} </p>
                        <p> {`Final pot  was #${lastPotAmount}.`} </p>
                    </div>
                )
            }

            { /* This is a hack to scroll to bottom of the div whenever there is a new log added */}
            <div id="scroll-to-bottom"></div>
        </div>
    );
}