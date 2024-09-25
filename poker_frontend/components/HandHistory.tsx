'use client'

import { useAppDispatch, useAppSelector } from "@/lib/hooks";
import { cn } from "@/lib/utils";

export default function HandHistory(
    { className }: React.ButtonHTMLAttributes<HTMLButtonElement>) {
    
    const dispatch = useAppDispatch();
    const { loading } = useAppSelector((state) => state.history);

    return (
        <div className={cn("bg-secondary p-4", className)}>
            <div
                className="animate-pulse bg-blue-600 sticky top-0"
                style={{ height: ".4rem", display: loading ? "block" : "none" }}
            ></div>

            <div className="text-xl px-2"> Hand History</div>

            <div className="flex flex-col gap-3 p-3 ">
                <div className="container p-3 bg-blue-200 dark:bg-blue-800">
                    Lorem ipsum dolor sit amet consectetur, adipisicing elit.
                    est ducimus illo, ipsum similique aliquid iusto minima
                    unde omnis ut adipisci amet molestiae tempora perspiciatis
                    voluptatibus fuga aperiam? Animi, laboriosam dolore
                    minus, fugit perspiciatis hic vitae id unde doloremque enim!
                </div>
            </div>
        </div>
    );
}