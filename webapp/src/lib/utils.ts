import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

// Get date in UTC (in YYYY-MM-DD format)
export const getDateUTC = (numDays: number) => {
  const now = new Date()

  // Set time to 00:00:00 UTC to normalize
  const utcYear = now.getUTCFullYear()
  const utcMonth = now.getUTCMonth()
  const utcDate = now.getUTCDate()

  const date = new Date(Date.UTC(utcYear, utcMonth, utcDate + numDays))
  return date.toISOString().split('T')[0] // Get only the "YYYY-MM-DD"
}

export const getFormattedDate = (date: string | Date) => {
  return new Date(date).toISOString().split('T')[0]
} 

export const getTeamLogo = (teamName: string) => {
  const teamNameLower = teamName.toLowerCase();
  const teamNameWithoutAccent = teamNameLower.replace(/é/g, 'e').replace(/è/g, 'e').replace(/à/g, 'a').replace(/ç/g, 'c').replace(/ô/g, 'o').replace(/î/g, 'i').replace(/ü/g, 'u');
  const teamNameWithoutSpace = teamNameWithoutAccent.replace(/ /g, '-');
  const path = `/league-of-legends/${teamNameWithoutSpace}/${teamNameWithoutSpace}-logo.png`
  return path;
}
