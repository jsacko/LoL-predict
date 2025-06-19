"use client"
import { Dialog, DialogTrigger, DialogContent, DialogHeader, DialogTitle, DialogDescription } from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'

// components/RulesDialog.tsx
export function RulesDialog() {
    return (
      <Dialog>
        <DialogTrigger asChild>
          <Button variant="outline" className="h-12 px-6 text-lg cursor-pointer">
            Rules
          </Button>
        </DialogTrigger>
        <DialogContent className="bg-white text-black sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>📜 Prediction Rules</DialogTitle>
            <DialogDescription className="space-y-2 text-3xl mt-4">
              <p>🎯 Predict the winner of each League of Legends professional match before it starts.</p>
              <p>✅ You earn <strong>100 points for each correct prediction</strong>, multiplied by your accuracy.</p>
              <p>So, the higher your accuracy is, the more points you get — especially if you make a lot of predictions!</p>
              <p>💡 Formula: 
                <code className="bg-gray-100 p-1 rounded ml-1">score = correctPredictions × (1 + accuracy) × 100</code>
              </p>
              <p>🏆 If your accuracy is higher than the AI’s, you'll gain a <strong>20% bonus</strong> on your score!</p>
              <p><br></br>Have fun !</p>
            </DialogDescription>
          </DialogHeader>
        </DialogContent>
      </Dialog>
    )
  }