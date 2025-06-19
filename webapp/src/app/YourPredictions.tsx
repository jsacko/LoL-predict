"use client";

import { useMemo } from "react";
import { DatePicker } from "@/components/ui/date-picker";
import { Button } from "@/components/ui/button";
import { Prediction, Match } from "@/types";
import { format, isBefore, isSameDay, subDays, addDays } from "date-fns";
import { getFormattedDate } from "@/lib/utils";
import { ArrowLeftIcon, ArrowRightIcon } from "lucide-react";

export function YourPredictions({
  matches,
  predictions,
  userId,
  selectedDate,
  setSelectedDate,
}: {
  matches: Match[];
  predictions: Prediction[];
  userId: string;
  selectedDate: Date;
  setSelectedDate: (d: Date) => void;
}) {
  // Only show predictions made before today and by the user
  const today = new Date();
  const filteredMatches = useMemo(() =>
    matches.filter(
      (m) =>
        m.date &&
        getFormattedDate(m.date) === getFormattedDate(selectedDate)
    ), [matches, selectedDate]);
    // print matches >  1st may 2025
    console.log("matchhs",matches.length)
  const filteredPredictions = useMemo(() =>
    predictions.filter(
      (p) =>
        p.user_id === userId &&
        p.matches.date &&
        getFormattedDate(p.matches.date) === getFormattedDate(selectedDate)
    ), [predictions, userId, selectedDate]);


    return (
    <div className="bg-gray-800 rounded-lg p-6">
      <div className="flex items-center gap-4 mb-6">
             
        <Button
          variant="outline"
          size="icon"
          onClick={() => {
            console.log("previous", subDays(selectedDate, 1));
            setSelectedDate(subDays(selectedDate, 1))
          }}
          aria-label="Previous Day"
          className="cursor-pointer hover:scale-110 transition-all duration-200"
        >
          <ArrowLeftIcon className="h-6 w-6" />
        </Button>
        <DatePicker date={selectedDate} setDate={setSelectedDate as any} />
        <Button
          variant="outline"
          size="icon"
          onClick={() => setSelectedDate(addDays(selectedDate, 1))}
          aria-label="Next Day"
          disabled={getFormattedDate(selectedDate) === getFormattedDate(today)}
          className="cursor-pointer hover:scale-110 transition-all duration-200"

        >
          <ArrowRightIcon className="h-6 w-6" />
        </Button>
      </div>
      <h2 className="text-2xl font-bold text-white mb-4 text-center">
        Your Predictions for {format(selectedDate, "PPP")}
      </h2>
      {filteredMatches.length === 0 ? (
        <p className="text-gray-400 text-center">No predictions for this date.</p>
      ) : (
        <div className="space-y-4">
          {filteredMatches.map((match) => { 
            const myPrediction = filteredPredictions.find((p) => p.bo_id === match.bo_id)
            return(
            <div key={match.bo_id} className="flex   justify-between items-center bg-gray-900 rounded-lg p-4 shadow">
            <div className="flex flex-col gap-1" >
            <span className="text-white font-semibold">
                {match.teamname_a} vs {match.teamname_b}
              </span>

              
              
              <span className="text-[#38bdf8] text-lg md:text-xl font-semibold  py-2 ">
                AI prediction: <span className="font-bold text-white">{match.prediction === 0 ? match.teamname_a : match.teamname_b}</span>
              </span>
              <span className="text-[#38bdf8] text-lg md:text-xl font-semibold  py-2 ">
                Your prediction: <span className="font-bold text-white">{myPrediction ? myPrediction.prediction === 0 ? match.teamname_a : match.teamname_b : "No prediction"}</span>
              </span>
              </div>
              <span className="text-[#38bdf8] text-lg md:text-xl font-semibold  py-2 ">
                Result : <span className="font-bold text-white">{match.result !== null ? match.result === 0 ? match.teamname_a : match.teamname_b : "Incoming..."}</span>
              </span>
              <span className="text-gray-400">
                {getFormattedDate(match?.date || new Date()) }
              </span>
            </div>
            
              
            
          )})}
        </div>
      )}
    </div>
  );
}
