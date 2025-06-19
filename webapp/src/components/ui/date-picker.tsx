"use client";

import * as React from "react";
import { format } from "date-fns";
import { Calendar as CalendarIcon } from "lucide-react";

import { cn } from "@/lib/utils";
import { Button } from "./button";
import { Calendar } from "./calendar";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "./popover";

export function DatePicker({ date, setDate }: { date: Date | undefined; setDate: (date: Date | undefined) => void }) {
  const [open, setOpen] = React.useState(false);

  const handleDateSelect = (selectedDate: Date | undefined) => {
    setDate(selectedDate);
    if (!selectedDate){
      // set today UTC
      setDate(new Date())
    }
    setOpen(false); // Ferme le popover après sélection

  };
  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant={"outline"}
          className={cn(
            "w-[220px] justify-start text-left font-normal",
            !date && "text-muted-foreground"
          )}
        >
          <CalendarIcon className="mr-2 h-4 w-4" />
          {date ? format(date, "PPP") : <span>Pick a date</span>}
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-auto p-0" align="start">
        <Calendar
          mode="single"
          selected={date}
          onSelect={handleDateSelect}
          disabled={(date) =>
            // Disable date after tomorrow and before 1st may 2025
            date.getTime() >= new Date().getTime() || date.getTime() < new Date("2025-01-01").getTime()
          }
          initialFocus
        />
      </PopoverContent>
    </Popover>
  );
}
