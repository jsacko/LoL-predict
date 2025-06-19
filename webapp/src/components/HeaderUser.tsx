"use client"
import React from "react";
import Image from "next/image";
import Link from "next/link";
import { supabase } from "@/lib/supabase";
import { RulesDialog } from "./RulesDialog";
import { useAuth } from "@/hooks/AuthProviders";
import { User, Leaderboard } from "@/types";
import { Button } from '@/components/ui/button'

import AuthModal from "./AuthModal";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function HeaderUser() {

  const [authModalOpen, setAuthModalOpen] = useState(false);

  const { user, leaderboard } = useAuth() as { user: User, leaderboard: Leaderboard[] };
  const router = useRouter();
  return (
    <header className="w-full flex items-center justify-between px-6 py-4 ">
      <div className="flex items-center gap-4">
      
      <Button variant="default" className="h-12 px-6 text-lg cursor-pointer" onClick={() => {router.push("/")}}>
        Home
      
      </Button>

      {user?.email !== null && <button className="text-white font-bold py-2 px-6 rounded-md shadow-lg text-lg transition-all duration-200 cursor-pointer bg-red-700" onClick={() => {
        supabase.auth.signOut();
      }}>
          Sign out
        </button>}
        <RulesDialog />
        </div>
        

      <div className="flex items-center gap-4">
      <Link href="/leaderboard">
      <button className="bg-gradient-to-r from-blue-500 to-cyan-400 hover:from-blue-600 hover:to-cyan-500 text-white font-bold py-2 px-6 rounded-md shadow-lg text-lg transition-all duration-200">
          Leaderboard
        </button>
        </Link>
      <span className="text-2xl text-gray-400">Rank: <span className="text-green-400 font-semibold"> {leaderboard.find((leader) => leader.user_id === user?.id)?.rank || "N/A"}</span></span>
      <span className="text-2xl text-gray-400">Accuracy: <span className="text-green-400 font-semibold">
        {(() => {
            const userEntry = leaderboard.find(leader => leader.user_id === user?.id);
            const accuracy = userEntry?.accuracy;
            if (accuracy === undefined || accuracy === -1) return ' N/A';
            return (accuracy * 100).toFixed(2) + '%';
          })()}
        </span>
      </span>
      <span className="text-2xl text-gray-400">Score: <span className="text-green-400 font-semibold"> {leaderboard.find((leader) => leader.user_id === user?.id)?.score?.toFixed(0) || 0}</span></span>
      
      <span className="text-2xl font-bold text-white">{user?.pseudo}</span>
      {
            user?.email === null && (
              <>
                <Button
                  variant="outline"
                  className="text-black font-bold py-2 px-6 rounded-md shadow-lg text-lg transition-all duration-200 cursor-pointer"
                  onClick={() => setAuthModalOpen(true)}
                >
                  Login
                </Button>
                <AuthModal open={authModalOpen} onClose={() => setAuthModalOpen(false)} />
              </>
            ) 
          }

      </div>
    </header>
  );
}
