import React, { useState } from "react";
import ImageUpload from "./components/ImageUpload";
import Results from "./components/Results";
import { motion } from "framer-motion";
import { Sun, Moon } from "lucide-react";

function App() {
  const [results, setResults] = useState(null);
  const [darkMode, setDarkMode] = useState(false);

  return (
    <div
      className={`min-h-screen flex flex-col items-center p-6 transition-colors duration-500 ${
        darkMode
          ? "bg-black text-gray-100" // 🔥 Full black background in dark mode
          : "bg-gradient-to-br from-indigo-100 via-white to-pink-100 text-gray-900"
      }`}
    >
      {/* Dark Mode Toggle */}
      <div className="w-full flex justify-end mb-4">
        <button
          onClick={() => setDarkMode(!darkMode)}
          className={`flex items-center gap-2 px-4 py-2 rounded-xl shadow-md transition ${
            darkMode
              ? "bg-gray-900 hover:bg-gray-800 text-blue-300 border border-gray-700"
              : "bg-white hover:bg-gray-200 text-indigo-600"
          }`}
        >
          {darkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
          {darkMode ? "Light Mode" : "Dark Mode"}
        </button>
      </div>

      {/* Header Section */}
      <motion.div
        initial={{ opacity: 0, y: -30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.7 }}
        className="text-center mb-10"
      >
        <h1
          className={`text-5xl font-extrabold drop-shadow-lg ${
            darkMode
              ? "bg-gradient-to-r from-yellow-400 to-pink-400 bg-clip-text text-transparent"
              : "bg-gradient-to-r from-indigo-600 to-pink-500 bg-clip-text text-transparent"
          }`}
        >
          UX Review Tool
        </h1>
        <p
          className={`mt-4 text-lg ${
            darkMode ? "text-gray-300" : "text-gray-700"
          }`}
        >
          Upload a landing page screenshot and get a UX score with <br />
          <span
            className={`font-semibold ${
              darkMode ? "text-blue-300" : "text-indigo-600"
            }`}
          >
            actionable tips & design recommendations.
          </span>
        </p>
      </motion.div>

      {/* Content Area */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-4xl"
      >
        {!results ? (
          <motion.div
            whileHover={{ scale: 1.02 }}
            transition={{ type: "spring", stiffness: 180, damping: 18 }}
            className={`rounded-3xl p-10 border backdrop-blur-xl shadow-2xl transition-all duration-300 ${
              darkMode
                ? "bg-black border-gray-800 hover:shadow-gray-700/50" // 🔥 Black card
                : "bg-white/90 border-gray-200 hover:shadow-xl"
            }`}
          >
            <h2
              className={`text-2xl font-bold mb-6 ${
                darkMode ? "text-yellow-300" : "text-indigo-600"
              }`}
            >
              Upload Screenshot
            </h2>
            <ImageUpload onResults={setResults} />
          </motion.div>
        ) : (
          <motion.div
            key="results"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.5 }}
          >
            <Results results={results} onNewAnalysis={() => setResults(null)} />
          </motion.div>
        )}
      </motion.div>

      {/* Footer */}
      <motion.footer
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1, duration: 1 }}
        className={`mt-12 text-sm text-center ${
          darkMode ? "text-gray-500" : "text-gray-500"
        }`}
      >
        <motion.p
          animate={{ y: [0, -4, 0] }}
          transition={{ repeat: Infinity, duration: 3 }}
        >
          Built to improve your landing page UX.
        </motion.p>
      </motion.footer>
    </div>
  );
}

export default App;
