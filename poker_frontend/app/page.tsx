import Image from "next/image";
import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from "@/components/ui/resizable"
import PlayLog from "@/components/PlayLog";
import Setup from "@/components/Setup";
import HandHistory from "@/components/HandHistory";
import Actions from "@/components/Actions";

export default function Home() {
  const defaultLayout = [70, 30]

  return (
    <div className="grid grid-rows-[1fr_20px] items-center justify-items-center h-full sm:p-10 font-[family-name:var(--font-geist-sans)] border flex-1">
      <ResizablePanelGroup
        direction="horizontal"
        className="border"
        autoSaveId={"react-resizable-panels:layout:mainlayout"}
      >
        <ResizablePanel
          defaultSize={defaultLayout[0]}
        >
          <div className="flex flex-col h-full border gap-3">
            <h1 className="text-xl"> Playing Field Log </h1>
            <Setup />
            <PlayLog className="flex-1"/>
            <Actions />
          </div>

        </ResizablePanel>

        <ResizableHandle withHandle className="text-black" />

        <ResizablePanel
          defaultSize={defaultLayout[1]}
          collapsible={true}
        >
          <HandHistory/>
        </ResizablePanel>
      </ResizablePanelGroup>

      <footer className="row-start-3 flex gap-6 flex-wrap items-center justify-center">
        <a
          className="flex items-center gap-2 hover:underline hover:underline-offset-4"
          href="https://bicyclecards.com/how-to-play/texas-holdem-poker"
          target="_blank"
          rel="noopener noreferrer"
        >
          <Image
            aria-hidden
            src="https://nextjs.org/icons/file.svg"
            alt="File icon"
            width={16}
            height={16}
          />
          Learn Game Rules
        </a>
      </footer>
    </div>
  );
}
