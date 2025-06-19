"use client"

import { useEffect, useState } from 'react'
import { supabase } from '@/lib/supabase'
import { Match, Prediction } from '@/types'
import { EmblaOptionsType } from 'embla-carousel'
import EmblaCarouselMatches from '@/components/carousel/EmblaCarouselMatches'
import { YourPredictions } from './YourPredictions'
import { getDateUTC } from '@/lib/utils'
import '../css/base.css'
import '../css/sandbox.css'
import '../css/embla.css'

// Toast fade in/out animation
const toastStyle = `@keyframes fadein-out {
  0% { opacity: 0; transform: translateY(-20px); }
  10% { opacity: 1; transform: translateY(0); }
  90% { opacity: 1; transform: translateY(0); }
  100% { opacity: 0; transform: translateY(-20px); }
}
.animate-fadein-out {
  animation: fadein-out 2.5s cubic-bezier(.4,0,.2,1);
}`;

if (typeof window !== 'undefined') {
  // Inject the toast animation style only once
  if (!document.getElementById('toast-fadein-out-style')) {
    const style = document.createElement('style');
    style.id = 'toast-fadein-out-style';
    style.innerHTML = toastStyle;
    document.head.appendChild(style);
  }
}

import { useAuth } from '@/hooks/AuthProviders'
import { User } from '@/types'


const OPTIONS_CAROUSEL: EmblaOptionsType = { loop: true }

export default function Home() {
  const [matches, setMatches] = useState<Match[]>([])
  const [loading, setLoading] = useState(true)
  const [predictions, setPredictions] = useState<Prediction[]>([])
  const [emblaApi] = useState<any>(null)
  const [showToast, setShowToast] = useState(false);
  const { user } = useAuth() as { user: User };
  const [selectedDate, setSelectedDate] = useState(() => {
    // Default to yesterday
    
    const d = new Date();
    d.setDate(d.getDate() -1);
    d.setHours(0,0,0,0);
    
    return d;
  });
  useEffect(() => {
   
    if (user) {
      fetchPredictions()
    }
    console.log("the useeffect work, is the screen focused ?");


    // Definition de l'ouverture des channels realtime
    const channel = supabase
      .channel("ch_predictions")
      .on(
        "postgres_changes",
        {
          event: "*",
          schema: "public",
          table: "predictions",
          //filter: `id_shooting=eq.${shooting.id}`,
        },
        (payload) => {
          fetchPredictions()
          switch (payload.eventType) {
            case "INSERT":
              console.log("CASE INSERT prediction", payload.new);
              break;
            case "UPDATE":
              console.log("CASE UPDTE prediction", payload.new);
              break;
            case "DELETE":
              console.log("CASE DELETE prediction", payload.new);
              break;
            default:
              console.error(
                "Evenement realtime des predictions non pris en charge"
              );
              break;
          }
        }
      )
      .subscribe();

    return () => {
      supabase.removeChannel(channel);
    };

  }, [user])


  const handleVote = async (bo_id: string, vote: number) => {
    try {
      const { data, error } = await supabase
        .from('predictions')
        .upsert({
          bo_id,
          prediction: vote,
          user_id: user?.id
        })

      if (error) throw error
      
      // Refresh predictions
      //fetchPredictions()
      setShowToast(true);
      setTimeout(() => setShowToast(false), 2500);
    } catch (error) {
      console.error('Error voting:', error)
    }
  }


  const fetchPredictions = async () => {
    try {
      const { data, error } = await supabase
        .from('predictions')
        .select('*, matches(*)')
      
      console.log("my predictions", data)
      if (error) throw error
      setPredictions(data)
    } catch (error) {
      console.error('Error fetching predictions:', error)
    }
  }

  useEffect(() => {
    const fetchMatches = async () => {
      try {
        
        const { data, error } = await supabase
          .from('matches')
          .select('*')
        console.log("data", data)
        if (error) throw error
        setMatches(data)
      } catch (error) {
        console.error('Error fetching matches:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchMatches()
  }, [])

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>
  }

  return (
    <>
      {/* Toast notification */}
      {showToast && (
        <div className="fixed top-8 left-1/2 transform -translate-x-1/2 z-50">
          <div className="bg-green-500 text-white px-6 py-3 rounded-xl shadow-xl animate-fadein-out font-semibold flex items-center gap-2">
            <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" /></svg>
            Vote registered!
          </div>
        </div>
      )}

      <div className="min-h-screen">
        <div className="container mx-auto px-4">
          <h1 className="text-4xl font-bold text-white mb-8 text-center">Tomorrow's upcoming Pro Matches </h1>
          <h2 className="text-4xl font-bold text-white mb-8 text-center">
          {new Date(getDateUTC(1)+ " 00:00:00").toLocaleDateString("en-gb", { weekday: "long", year: "numeric", month: "long", day: "numeric"})}
        </h2>
        
        <div className="container mx-auto ">

          <EmblaCarouselMatches
            matches={matches}
            predictions={predictions}
            options={OPTIONS_CAROUSEL}
            handleVote={handleVote}
            
          />
        </div>

        <div className="mt-16">
          <YourPredictions
            predictions={predictions}
            matches={matches}
            userId={user?.id}
            selectedDate={selectedDate}
            setSelectedDate={setSelectedDate}
          />
        </div>
      </div>
    </div>
    </>
  )
}