import React, { useState } from 'react';
import { Terminal, Send, Clock, CheckCircle2, XCircle } from 'lucide-react';

interface CommandHistory {
  id: string;
  command: string;
  status: 'completed' | 'failed';
  timestamp: string;
  intent?: any;
}

function App() {
  const [command, setCommand] = useState('');
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState<CommandHistory[]>([]);
  const [error, setError] = useState<string | null>(null);

  const processCommand = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!command.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/process-command', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': 'your-secret-key', // In production, use environment variables
        },
        body: JSON.stringify({ command }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to process command');
      }

      const result = await response.json();

      setHistory((prev) => [
        {
          id: result.command_id || Date.now().toString(), // Fallback in case ID is missing
          command,
          status: result.status || 'failed', // Default to 'failed' if missing
          timestamp: new Date().toISOString(),
          intent: result.processed_intent,
        },
        ...prev,
      ]);

      setCommand('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto p-6">
        <div className="flex items-center gap-2 mb-8">
          <Terminal className="w-8 h-8 text-indigo-600" />
          <h1 className="text-2xl font-bold text-gray-900">NLP Command Processor</h1>
        </div>

        <form onSubmit={processCommand} className="mb-8">
          <div className="flex gap-2">
            <input
              type="text"
              value={command}
              onChange={(e) => setCommand(e.target.value)}
              placeholder="Enter a command (e.g., 'Schedule a team meeting tomorrow at 2 PM')"
              className="flex-1 px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading}
              className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              {loading ? (
                <>
                  <Clock className="animate-spin w-5 h-5" />
                  Processing...
                </>
              ) : (
                <>
                  <Send className="w-5 h-5" />
                  Send
                </>
              )}
            </button>
          </div>
          {error && <p className="mt-2 text-sm text-red-600">{error}</p>}
        </form>

        <div className="space-y-4">
          {history.map((item) => (
            <div key={item.id} className="bg-white p-4 rounded-lg shadow border border-gray-200">
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-center gap-2">
                  {item.status === 'completed' ? (
                    <CheckCircle2 className="w-5 h-5 text-green-500" />
                  ) : (
                    <XCircle className="w-5 h-5 text-red-500" />
                  )}
                  <p className="font-medium text-gray-900">{item.command}</p>
                </div>
                <span className="text-sm text-gray-500">
                  {new Date(item.timestamp).toLocaleTimeString()}
                </span>
              </div>
              {item.intent && (
                <pre className="mt-2 p-3 bg-gray-50 rounded text-sm overflow-x-auto">
                  {JSON.stringify(item.intent, null, 2)}
                </pre>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;
