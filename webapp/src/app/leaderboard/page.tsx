"use client";

import React, { useContext } from "react";
import { AuthContext } from "@/hooks/AuthProviders";
import type { Leaderboard } from "@/types";

export default function LeaderboardPage() {
  const { leaderboard } = useContext(AuthContext) as { leaderboard: Leaderboard[] };
  console.log("Leaderboard", leaderboard);
  return (
    <div className="max-w-3xl mx-auto py-10 px-4">
      <h1 className="text-4xl font-bold mb-8 text-center text-green-400 drop-shadow">Leaderboard</h1>
      <div className="overflow-x-auto rounded-lg shadow-lg bg-gray-900">
        <table className="min-w-full divide-y divide-gray-700">
          <thead className="bg-gray-800">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Rank</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">User</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Total Score</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Accuracy</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Number of predictions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-800">
            {leaderboard && leaderboard.length > 0 ? (
              leaderboard.map((row, idx) => (
                <tr key={row.user_id} className={idx < 3 ? "bg-gray-800" : ""}>
                  <td className="px-6 py-4 whitespace-nowrap text-xl font-bold text-green-300">
                    {row.rank === 1 ? "🥇" : row.rank === 2 ? "🥈" : row.rank === 3 ? "🥉" : row.rank}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-lg text-gray-200">{row.pseudo}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-lg text-green-400">{row.score?.toFixed(0)}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-lg text-green-400">{row.accuracy == -1 ? "N/A" : row.accuracy.toFixed(2) + "%"}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-lg text-green-400">{row.nb_predictions}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={3} className="px-6 py-8 text-center text-gray-400">No leaderboard data available.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div> 
  );
}
