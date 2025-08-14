import React, { useState } from 'react';
import axios from 'axios';

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000/ingest-youtube";

const App: React.FC = () => {
  const [youtubeUrl, setYoutubeUrl] = useState<string>('');
  const [summary, setSummary] = useState<string>('');
  const [qaOutput, setQaOutput] = useState<string>('');
  const [language, setLanguage] = useState<string>('en');
  const [loading, setLoading] = useState<boolean>(false);
  const [summaryType, setSummaryType] = useState<string>('study_guide');

  const handleUrlChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setYoutubeUrl(event.target.value);
  };

  const handleSummarize = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      params.append('youtube_url', youtubeUrl);
      params.append('language', language);
      params.append('summary_type', summaryType);

      const response = await axios.post(BACKEND_URL, params, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });
      setSummary(response.data.summary);
      setQaOutput(response.data.answer);
    } catch (error: any) {
      console.error("Error fetching summary:", error);
      let errorMessage = "Error fetching summary: ";
      if (error.response) {
        errorMessage += `Status: ${error.response.status}, Data: ${JSON.stringify(error.response.data)}`;
      } else if (error.request) {
        errorMessage += error.message;
      }
      setSummary(errorMessage);
      setQaOutput("");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow">
        <div className="mx-auto max-w-7xl py-6 px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold tracking-tight text-gray-900">YouTube Summarizer & Q&A</h1>
        </div>
      </header>
      <main>
        <div className="mx-auto max-w-7xl py-6 sm:px-6 lg:px-8">
          {/* Input area */}
          <div className="px-4 py-6 sm:px-0">
            <input
              type="text"
              className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md"
              placeholder="Enter YouTube URL"
              value={youtubeUrl}
              onChange={handleUrlChange}
            />
            <select
              className="mt-2 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md"
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
            >
              <option value="en">English</option>
              <option value="hi">Hindi</option>
            </select>
            <select
              className="mt-2 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md"
              value={summaryType}
              onChange={(e) => setSummaryType(e.target.value)}
            >
              <option value="study_guide">Study Guide</option>
              <option value="medium_articles_ai_ml">Medium Articles AI/ML</option>
              <option value="medium_articles_cloud">Medium Articles Cloud</option>
            </select>
            <button
              className="mt-4 inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              onClick={handleSummarize}
              disabled={loading}
            >
              {loading ? "Summarizing..." : "Summarize & Q&A"}
            </button>
          </div>

          <div className="px-4 py-6 sm:px-0">
            <div className="border-4 border-dashed border-gray-200 rounded-lg min-h-96 p-4">
              <h2 className="text-xl font-semibold text-gray-700">Summary</h2>
              <p className="mt-2 text-gray-500">{summary}</p>
              <h2 className="text-xl font-semibold text-gray-700 mt-4">Q&A</h2>
              <p className="mt-2 text-gray-500">{qaOutput}</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
