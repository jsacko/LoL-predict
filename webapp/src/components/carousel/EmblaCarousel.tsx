import { useRef, useEffect, useState } from 'react'
import  useEmblaCarousel from 'embla-carousel-react'
import type { EmblaOptionsType } from 'embla-carousel'

interface EmblaCarouselProps {
  children: React.ReactNode
  options?: EmblaOptionsType
  onInit?: (api: any) => void
}

export function EmblaCarousel({ children, options = { loop: true, align: 'center' }, onInit }: EmblaCarouselProps) {
  const [emblaRef, emblaApi] = useEmblaCarousel(options)

  useEffect(() => {
    if (emblaApi && onInit) {
      onInit(emblaApi)
    }
  }, [emblaApi, onInit])

  return (
    <div className="embla" ref={emblaRef}>
      <div className="embla__container">
        {children}
      </div>
    </div>
  )
}
