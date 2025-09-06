import React, { useState } from "react";
import { motion } from "framer-motion";
import { AlertCircle, CheckCircle2, Lightbulb, RefreshCcw } from "lucide-react";

const Results = ({ results, onNewAnalysis }) => {
  const [showRecommendations, setShowRecommendations] = useState(true);

  if (!results) {
    return (
      <p className="text-gray-500 text-center mt-6">
        🚀 No results yet. Upload an image first!
      </p>
    );
  }

  if (results.error) {
    return (
      <div className="bg-red-100 border border-red-300 text-red-700 p-4 rounded-lg mt-6 max-w-xl mx-auto flex items-center gap-2">
        <AlertCircle className="w-5 h-5" />
        <span>
          <strong>Error:</strong> {results.error}
        </span>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 25 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="max-w-3xl mx-auto mt-8 p-6 rounded-2xl shadow-lg bg-gradient-to-r from-blue-50 to-cyan-100"
    >
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
          <CheckCircle2 className="w-6 h-6 text-green-500" />
          Analysis Results
        </h2>
        <button
          onClick={onNewAnalysis}
          className="flex items-center gap-2 bg-cyan-600 text-white px-4 py-2 rounded-lg hover:bg-cyan-700 transition shadow-md"
        >
          <RefreshCcw className="w-4 h-4" />
          New Analysis
        </button>
      </div>

      {/* Overall Score */}
      <div
        className={`text-white rounded-xl p-6 text-center shadow-md ${
          results.overall_score >= 0.7
            ? "bg-green-400"
            : results.overall_score >= 0.4
            ? "bg-yellow-400 text-gray-800"
            : "bg-red-400"
        }`}
      >
        <p className="text-lg font-semibold">Overall Score</p>
        <p className="text-4xl font-bold">{results.overall_score}</p>
      </div>

      {/* Detailed Scores */}
      <h3 className="text-lg font-semibold mt-6 text-gray-800">Detailed Scores</h3>
      <div className="grid grid-cols-2 gap-4 mt-3">
        {Object.entries(results.detailed_scores || {}).map(([key, value]) => (
          <motion.div
            key={key}
            whileHover={{ scale: 1.05 }}
            className="bg-white shadow-md p-4 rounded-lg flex flex-col items-center transition hover:shadow-lg"
          >
            <span className="font-bold capitalize text-gray-700">{key}</span>
            <span
              className={`text-lg font-semibold ${
                value >= 0.7
                  ? "text-green-500"
                  : value >= 0.4
                  ? "text-yellow-500"
                  : "text-red-500"
              }`}
            >
              {value}
            </span>
          </motion.div>
        ))}
      </div>

      {/* Issues */}
      <h3 className="text-lg font-semibold mt-6 text-red-600 flex items-center gap-2">
        <AlertCircle className="w-5 h-5" /> Issues
      </h3>
      <div className="bg-white p-4 rounded-lg shadow-md mt-2">
        {(results.issues || []).length > 0 ? (
          <ul className="list-disc pl-5 space-y-2">
            {results.issues.map((issue, i) => (
              <li key={i} className="text-red-600">
                {issue.reason ? `${issue.reason} (${issue.type})` : JSON.stringify(issue)}
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-green-600 font-medium flex items-center gap-2">
            <CheckCircle2 className="w-5 h-5" /> No issues found
          </p>
        )}
      </div>

      {/* Recommendations */}
      <div className="mt-6">
        <button
          onClick={() => setShowRecommendations(!showRecommendations)}
          className="flex items-center gap-2 text-cyan-700 font-semibold hover:underline"
        >
          <Lightbulb className="w-5 h-5" />
          {showRecommendations ? "Hide Recommendations" : "Show Recommendations"}
        </button>

        {showRecommendations && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
            className="mt-4 space-y-4"
          >
            {(results.recommendations || []).length > 0 ? (
              results.recommendations.map((rec, i) => (
                <motion.div
                  key={i}
                  whileHover={{ scale: 1.02 }}
                  className="bg-teal-50 p-5 rounded-lg shadow-md hover:shadow-lg transition border border-teal-100"
                >
                  <p className="font-bold text-gray-800">{rec.title || "Suggestion"}</p>
                  <p className="text-gray-600 mt-1">{rec.description || ""}</p>
                  {rec.css_fix && (
                    <pre className="bg-gray-900 text-green-400 text-xs mt-3 p-3 rounded-lg whitespace-pre-wrap break-words max-w-full overflow-x-auto hover:bg-gray-800 transition">
                      {rec.css_fix}
                    </pre>
                  )}
                </motion.div>
              ))
            ) : (
              <p className="text-gray-600">No recommendations</p>
            )}
          </motion.div>
        )}
      </div>
    </motion.div>
  );
};

export default Results;
