"use client";
import { useEffect, useState } from 'react';
import { fetchDashboardStats, fetchRecentCalls } from '@/lib/api';

interface Stats {
  total_calls: number;
  success_rate: number;
  appointments_scheduled: number;
  failed_calls: number;
}

interface Call {
  id: string;
  agent_id: string;
  lead_phone: string;
  status: string;
  duration: number;
  timestamp: string;
  summary: string;
}

export default function Dashboard() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [calls, setCalls] = useState<Call[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
        try {
            const statsData = await fetchDashboardStats();
            const callsData = await fetchRecentCalls();
            setStats(statsData);
            setCalls(callsData);
        } catch (e) {
            console.error(e);
        } finally {
            setLoading(false);
        }
    }
    loadData();
  }, []);

  if (loading) return <div className="p-4">Loading dashboard...</div>;

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-3xl font-bold">Agent Dashboard</h1>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white p-4 rounded shadow border">
            <h3 className="text-gray-500 text-sm">Total Calls</h3>
            <p className="text-2xl font-bold">{stats?.total_calls}</p>
        </div>
        <div className="bg-white p-4 rounded shadow border">
            <h3 className="text-gray-500 text-sm">Success Rate</h3>
            <p className="text-2xl font-bold">{(stats?.success_rate ? stats.success_rate * 100 : 0).toFixed(1)}%</p>
        </div>
        <div className="bg-white p-4 rounded shadow border">
            <h3 className="text-gray-500 text-sm">Scheduled</h3>
            <p className="text-2xl font-bold">{stats?.appointments_scheduled}</p>
        </div>
        <div className="bg-white p-4 rounded shadow border">
            <h3 className="text-gray-500 text-sm">Failed</h3>
            <p className="text-2xl font-bold">{stats?.failed_calls}</p>
        </div>
      </div>

      {/* Recent Calls */}
      <div className="bg-white rounded shadow border p-4">
        <h2 className="text-xl font-bold mb-4">Recent Calls</h2>
        <table className="min-w-full text-left">
            <thead>
                <tr className="border-b">
                    <th className="py-2">Time</th>
                    <th className="py-2">Agent</th>
                    <th className="py-2">Lead</th>
                    <th className="py-2">Status</th>
                    <th className="py-2">Duration</th>
                    <th className="py-2">Summary</th>
                </tr>
            </thead>
            <tbody>
                {calls.map(call => (
                    <tr key={call.id} className="border-b last:border-0">
                        <td className="py-2 text-sm">{new Date(call.timestamp).toLocaleTimeString()}</td>
                        <td className="py-2 text-sm">{call.agent_id}</td>
                        <td className="py-2 text-sm">{call.lead_phone}</td>
                        <td className="py-2 text-sm">
                            <span className={`px-2 py-1 rounded text-xs ${call.status === 'completed' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                                {call.status}
                            </span>
                        </td>
                        <td className="py-2 text-sm">{call.duration}s</td>
                        <td className="py-2 text-sm text-gray-600">{call.summary}</td>
                    </tr>
                ))}
            </tbody>
        </table>
      </div>
    </div>
  );
}
