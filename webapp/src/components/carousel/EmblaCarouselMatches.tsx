import React, { useState, useMemo, useCallback, useEffect } from 'react'
import { EmblaOptionsType } from 'embla-carousel'
import { DotButton, useDotButton } from './EmblaCarouselDotButton'
import {
  PrevButton,
  NextButton,
  usePrevNextButtons
} from './EmblaCarouselArrowButtons'
import useEmblaCarousel from 'embla-carousel-react'
import { Button } from '@/components/ui/button'
import { Match } from '@/types'
import { useAuth } from '@/hooks/AuthProviders'
import { Prediction } from '@/types'
import { getDateUTC, getTeamLogo } from '@/lib/utils'
import { User } from '@/types'

type PropType = {
  matches: Match[]
  predictions: Prediction[]
  options?: EmblaOptionsType
  handleVote: (matchId: string, vote: number) => void
}

const tomorrowDate = getDateUTC(1)

const EmblaCarousel: React.FC<PropType> = (props) => {
  const { matches, predictions, options, handleVote } = props
  const { user } = useAuth() as { user: User }
  const [emblaRef, emblaApi] = useEmblaCarousel(options)
  const { prevBtnDisabled, nextBtnDisabled, onPrevButtonClick, onNextButtonClick } = usePrevNextButtons(emblaApi)
  const [selectedIndex, setSelectedIndex] = useState(0)
  const scrollSnaps = useMemo(() => emblaApi ? emblaApi.scrollSnapList() : [], [emblaApi])

  const filteredMatches = useMemo(() => matches.filter(match => match.date && match.date.split(" ")[0] === tomorrowDate), [matches])

  const onDotButtonClick = useCallback(
    (index: number) => {
      if (!emblaApi) return
      emblaApi.scrollTo(index)
    },
    [emblaApi]
  )

  useEffect(() => {
    if (!emblaApi) return
    setSelectedIndex(emblaApi.selectedScrollSnap())
    emblaApi.on('select', () => setSelectedIndex(emblaApi.selectedScrollSnap()))
  }, [emblaApi])

  return (
    <div className="">
    <section className="flex aspect-[16/9]">
      <div className="flex flex-col items-center justify-center px-2">
        <PrevButton 
          onClick={onPrevButtonClick} 
          disabled={prevBtnDisabled} 
        />
        </div>
      <div className="w-full h-full overflow-hidden " ref={emblaRef}>
        <div className="flex touch-pan-y pinch-zoom -ml-4 h-full  ">
          {filteredMatches.map((match, index) => (
            <div 
              key={match.bo_id} 
              className="flex-none w-[90%] h-full pl-4 flex items-center justify-center"
            >
              <div className="bg-[#101217] h-full w-full rounded-3xl border border-[#22232a] p-6 md:p-10 flex flex-col justify-between shadow-2xl transition-transform duration-300 hover:scale-[1.015]">
                {/* Header */}
                <div className="flex flex-col gap-2 md:gap-4 items-center w-full">
                  <div className="flex flex-row items-center w-full mb-2">
                    <span className="flex-1 basis-2/5 text-2xl md:text-4xl font-extrabold text-white text-center ">
                      {match.teamname_a}
                    </span>
                    <span className="flex-1 basis-1/5 text-center text-[#38bdf8] text-2xl md:text-4xl font-black uppercase tracking-widest">
                      VS
                    </span>
                    <span className="flex-1 basis-2/5 text-2xl md:text-4xl font-extrabold text-white text-center ">
                      {match.teamname_b}
                    </span>
                  </div>
                  {match.date && (
                    <p className="text-gray-400 text-center text-base md:text-lg mb-2 w-full">
                      {match.date} UTC
                    </p>
                  )}
                </div>

                {/* Teams and VS */}
                <div className="flex flex-1 items-center justify-center gap-4 md:gap-12 w-full mb-4">
                  {/* Team A */}
                  <div className="flex flex-col items-center flex-1 min-w-0">
                  <img
                    src={getTeamLogo(match.teamname_a || "")}
                    alt={match.teamname_a}
                    onError={(e) => { e.currentTarget.src = '/team_logo.webp'; }}
                    className="w-16 h-16 md:w-24 md:h-24 rounded-full mb-2 border-4 border-[#23272f] shadow-md object-cover transition-transform duration-200 hover:scale-105"
                  />

                    
                    <span className="text-white text-lg md:text-2xl font-bold leading-tight text-center break-words">
                      {match.teamname_a}
                    </span>
                  </div>
                  {/* VS */}
                  <div className="flex flex-col items-center justify-center flex-none">
                    <span className="text-3xl md:text-5xl font-black text-[#74788b] mb-2">VS</span>
                  </div>
                  {/* Team B */}
                  <div className="flex flex-col items-center flex-1 min-w-0">
                    <img src={getTeamLogo(match.teamname_b || "") || '/team_logo.webp'} alt={match.teamname_b} onError={(e) => { e.currentTarget.src = '/team_logo.webp'; }} className="w-16 h-16 md:w-24 md:h-24 rounded-full mb-2 border-4 border-[#23272f] shadow-md object-cover transition-transform duration-200 hover:scale-105" />
                    <span className="text-white text-lg md:text-2xl font-bold leading-tight text-center break-words">
                      {match.teamname_b}
                    </span>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4 md:gap-8 w-full mb-2 mt-auto">
                  <div className="flex flex-col items-center">
                    {(() => {
                      const userPrediction = predictions?.find(p => p.matches.bo_id === match.bo_id && p.user_id === user?.id);
                      const votedA = userPrediction && userPrediction.prediction === 0;
                      return (
                        <Button
                          variant={votedA ? "secondary" : "default"}
                          className={`w-full max-w-[220px] text-base md:text-lg font-semibold rounded-xl mb-1 shadow-lg transition-all duration-200 ${votedA ? 'bg-green-600 cursor-not-allowed opacity-80' : 'bg-gradient-to-r from-blue-600 to-blue-400 hover:from-blue-700 hover:to-blue-500'}`}
                          onClick={() => handleVote(match.bo_id!, 0)}
                          disabled={votedA}
                        >
                          {votedA ? (
                            <span className="flex items-center gap-1">Your Vote <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" /></svg></span>
                          ) : (
                            <>Vote {match.teamname_a}</>
                          )}
                        </Button>
                      );
                    })()}
                    <span className="text-[#7dd3fc] text-base md:text-lg font-medium">{predictions.filter(p => p.matches.bo_id === match.bo_id && p.prediction === 0).length} votes</span>
                  </div>
                  <div className="flex flex-col items-center">
                    {(() => {
                      const userPrediction = predictions?.find(p => p.matches.bo_id === match.bo_id && p.user_id === user?.id);
                      const votedB = userPrediction && userPrediction.prediction === 1;
                      return (
                        <Button
                          variant={votedB ? "secondary" : "default"}
                          className={`w-full max-w-[220px] text-base md:text-lg font-semibold rounded-xl mb-1 shadow-lg transition-all duration-200 ${votedB ? 'bg-green-600 cursor-not-allowed opacity-80' : 'bg-gradient-to-r from-red-600 to-pink-500 hover:from-red-700 hover:to-pink-600'}`}
                          onClick={() => handleVote(match.bo_id!, 1)}
                          disabled={votedB}
                        >
                          {votedB ? (
                            <span className="flex items-center gap-1">Your Vote <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" /></svg></span>
                          ) : (
                            <>Vote {match.teamname_b}</>
                          )}
                        </Button>
                      );
                    })()}
                    <span className="text-[#fca5a5] text-base md:text-lg font-medium">{ predictions.filter(p => p.matches.bo_id === match.bo_id && p.prediction === 1).length } votes</span>
                  </div>
                </div>

                {/* AI prediction */}
                <div className="w-full flex justify-center mt-4">
                  <span className="text-[#38bdf8] text-lg md:text-xl font-semibold bg-[#191c23] px-4 py-2 rounded-full shadow-sm">
                    AI predicts: <span className="font-bold text-white">{match.prediction === 0 ? match.teamname_a : match.teamname_b}</span>
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
      <div className="flex flex-col items-center justify-center px-2">
      <NextButton 
            onClick={onNextButtonClick} 
            disabled={nextBtnDisabled} 
          />
      </div>
      
    </section>
    <div className="flex justify-center items-center">
    <div className="mt-6 flex justify-between items-center gap-4">
      <div className="flex flex-wrap justify-end -mr-2 gap-2">
        {scrollSnaps.map((_, index) => (
          <button
            key={index}
            onClick={() => onDotButtonClick(index)}
            className={`
              w-8 h-8 flex items-center justify-center rounded-full transition-colors duration-200
              border-2
              ${index === selectedIndex
                ? 'border-white bg-white bg-opacity-10'
                : 'border-gray-600 hover:border-white'}
            `}
            aria-label={`Go to slide ${index + 1}`}
          >
            <span
              className={`
                w-4.5 h-4.5 rounded-full transition-colors duration-200
                ${index === selectedIndex ? 'bg-white' : 'bg-gray-500'}
              `}
            ></span>
          </button>
        ))}
      </div>
</div>
    </div>
    </div>
  )
}

export default EmblaCarousel
