"use client"
// AuthProvider.js
import React, { createContext, useState, useEffect, useContext } from "react";
import { supabase } from '@/lib/supabase'


const AuthContext = createContext({});

const AuthProvider = (props) => {
  const [loadingUser, setLoadingUser] = useState(true);
  const [user, setUser] = useState(null);
  const [leaderboard, setLeaderboard] = useState([]);

  const getSessionSupabase = async (session) => {
    try {
      console.log("Get session supabase...");
      setLoadingUser(true);
      console.log("Session supabase", session);
      // const { data, error:errorDamn } = await supabase.auth.getSession();
      
      // if (errorDamn) throw new Error(errorDamn);

      // const session = data.session;

      if (session) {
        const userId = session.user.id;

        // Utiliser Redux pour récupérer et stocker les informations de l'utilisateur
        console.log("Session found, fetching user info", userId);
        const { data, error } = await supabase.from('users').select('*').eq('id', userId).single()
        if (error) throw error;
        setUser(data);
        console.log("User info fetched: ", data);
        // fetch view leaderboard
        const { data: leaderboard, error: leaderboardError } = await supabase.from('leaderboard').select('*').order('rank', { ascending: true })
        console.log("Leaderboard auth", leaderboard);  
        if (leaderboardError) throw leaderboardError;
        setLeaderboard(leaderboard);
      } else {
        console.log("No session found, signin anonymously");
        const { data, error } = await supabase.auth.signInAnonymously()
        if (error) throw error;
        console.log("User signed in anonymously", data.user);
        setUser(data.user);
      }
    } catch (error) {
      console.log("Erreur fetching session", error.message);
    } finally {
      setLoadingUser(false);
    }
  };

  useEffect(() => {
    console.log("Auth provider mounted");
    
    const { data: authListener } = supabase.auth.onAuthStateChange(
      async (event, session) => {
        console.log(`Supabase auth event: ${event}`);
        console.log("Session ", session);
        getSessionSupabase(session);
      }
    );

    return () => {
      authListener.subscription.unsubscribe();
    };
  }, []);

  return (
    <AuthContext.Provider value={{ loadingUser, user, leaderboard }}>
      {props.children}
    </AuthContext.Provider>
  );
};

export { AuthContext, AuthProvider };

//Hook personnalisé pour accéder facilement au contexte Auth
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};