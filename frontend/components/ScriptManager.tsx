"use client";
import { useEffect, useState } from 'react';
import { fetchScripts } from '@/lib/api';

interface Script {
  id: string;
  name: string;
  content: { question: string; answer: string }[];
  created_at: string;
}

export default function ScriptManager() {
  const [scripts, setScripts] = useState<Script[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
        try {
            const data = await fetchScripts();
            setScripts(data);
        } catch(e) {
            console.error(e);
        } finally {
            setLoading(false);
        }
    }
    load();
  }, []);

  if (loading) return <div>Loading scripts...</div>;

  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Script Management</h1>
        <button className="bg-blue-600 text-white px-4 py-2 rounded">New Script</button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {scripts.map(script => (
            <div key={script.id} className="bg-white p-4 rounded shadow border">
                <h2 className="text-xl font-semibold mb-2">{script.name}</h2>
                <p className="text-sm text-gray-500 mb-4">Created: {new Date(script.created_at).toLocaleDateString()}</p>
                <div className="text-sm bg-gray-50 p-2 rounded mb-4 max-h-40 overflow-y-auto">
                    {script.content.map((item, idx) => (
                        <div key={idx} className="mb-2">
                            <p className="font-semibold text-blue-800">Q: {item.question}</p>
                            <p className="text-gray-700">A: {item.answer}</p>
                        </div>
                    ))}
                </div>
                <button className="text-blue-600 text-sm hover:underline">Edit Script</button>
            </div>
        ))}
      </div>
    </div>
  );
}
