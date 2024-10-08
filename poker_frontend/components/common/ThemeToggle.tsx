"use client"

import { useTheme } from "next-themes";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";


export function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  return (
    <div className="flex items-center space-x-2">
      <Switch id="dark-mode" 
        onCheckedChange={(checked) => {
          setTheme(checked ? "dark" : "light")
        }}
        defaultChecked={theme === "dark"}
      />
      <Label htmlFor="dark-mode" className="hidden lg:block">Dark Mode</Label>
    </div>
  );
}