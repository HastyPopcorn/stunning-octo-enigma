import React, { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";

const items = [
  "Louis", "Ben", "Dan", "Alisha", "Zak", "Corin", "Cuish", "Morgan", "Perry", 
  "Sadie", "Leah", "Amy", "Charlie", "Harry", "Sean", "Ruby", "Tanith", "Reece", 
  "Eleanor", "Makoto", "Masami", "Meriel"
];

const shufflePairs = (arr) => {
  let pairs = [];
  for (let i = 0; i < arr.length; i++) {
    for (let j = i + 1; j < arr.length; j++) {
      pairs.push([arr[i], arr[j]]);
    }
  }
  return pairs.sort(() => Math.random() - 0.5);
};

export default function VotingApp() {
  const [pairs, setPairs] = useState(shufflePairs(items));
  const [pairIndex, setPairIndex] = useState(0);
  const [scores, setScores] = useState(() => {
    let initialScores = {};
    items.forEach((item) => (initialScores[item] = 0));
    return initialScores;
  });
  const [showResults, setShowResults] = useState(false);

  const vote = (winner) => {
    setScores((prevScores) => ({
      ...prevScores,
      [winner]: prevScores[winner] + 1,
    }));
    if (pairIndex + 1 < pairs.length) {
      setPairIndex(pairIndex + 1);
    } else {
      setShowResults(true);
    }
  };

  return (
    <div className="flex flex-col items-center p-6">
      {!showResults ? (
        <div className="text-center">
          <h2 className="text-xl font-bold mb-4">Which do you prefer?</h2>
          <div className="flex gap-4">
            <Button onClick={() => vote(pairs[pairIndex][0])} className="text-lg p-4">
              {pairs[pairIndex][0]}
            </Button>
            <Button onClick={() => vote(pairs[pairIndex][1])} className="text-lg p-4">
              {pairs[pairIndex][1]}
            </Button>
          </div>
        </div>
      ) : (
        <div className="text-center">
          <h2 className="text-xl font-bold mb-4">Popularity Ranking</h2>
          {Object.entries(scores)
            .sort((a, b) => b[1] - a[1])
            .map(([item, score], index) => (
              <p key={item} className="text-lg">{index + 1}. {item} (Score: {score})</p>
            ))}
        </div>
      )}
    </div>
  );
}