import PlayLog from "@/components/PlayLog";
import Setup from "@/components/Setup";
import HandHistory from "@/components/HandHistory";
import Actions from "@/components/Actions";

export default function Home() {
  return (
    <div className=" items-center justify-items-center sm:p-10 font-[family-name:var(--font-geist-sans)] border border-red-500 flex-1 h-full ">
      <div className="px-10 gap-4 h-full justify-between grid grid-cols-5">
        <div className="flex flex-col gap-3 overflow-y-auto w-full col-span-3">
          <h1 className="text-xl"> Playing Field Log </h1>
          <Setup />
          <PlayLog className="border flex-1" />
          <Actions />
        </div>
        <div className="flex flex-col gap-3 overflow-y-auto h-full col-span-2">
          <div className="bg-white z-20 w-full text-2xl"> Hand History </div>
          <HandHistory className="mt-10"/>
        </div>
      </div>
    </div>
  );
}
