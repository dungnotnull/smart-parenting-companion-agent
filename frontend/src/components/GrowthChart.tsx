import { useState, useEffect } from 'react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  ResponsiveContainer, ReferenceLine,
} from 'recharts';
import type { GrowthLog } from '../lib/types';

interface Props {
  childId: number | null;
  childSex: string;
}

const WHO_BOYS_WEIGHT: [number, number][] = [
  [0, 3.3], [1, 4.5], [2, 5.6], [3, 6.4], [4, 7.0], [5, 7.5], [6, 7.9],
  [7, 8.3], [8, 8.6], [9, 8.9], [10, 9.2], [11, 9.4], [12, 9.6],
  [18, 10.9], [24, 12.2], [36, 14.3], [48, 16.3], [60, 18.3],
];

const WHO_GIRLS_WEIGHT: [number, number][] = [
  [0, 3.2], [1, 4.2], [2, 5.1], [3, 5.8], [4, 6.4], [5, 6.9], [6, 7.3],
  [7, 7.6], [8, 7.9], [9, 8.2], [10, 8.5], [11, 8.7], [12, 8.9],
  [18, 10.2], [24, 11.5], [36, 13.9], [48, 16.1], [60, 18.2],
];

const WHO_BOYS_HEIGHT: [number, number][] = [
  [0, 49.9], [1, 54.7], [2, 58.4], [3, 61.4], [4, 63.9], [5, 65.9], [6, 67.6],
  [7, 69.2], [8, 70.6], [9, 72.0], [10, 73.3], [11, 74.5], [12, 75.7],
  [18, 82.3], [24, 87.8], [36, 96.1], [48, 103.3], [60, 110.0],
];

const WHO_GIRLS_HEIGHT: [number, number][] = [
  [0, 49.1], [1, 53.7], [2, 57.1], [3, 59.8], [4, 62.1], [5, 64.0], [6, 65.7],
  [7, 67.3], [8, 68.7], [9, 70.1], [10, 71.5], [11, 72.8], [12, 74.0],
  [18, 80.7], [24, 86.4], [36, 95.1], [48, 102.7], [60, 109.4],
];

export default function GrowthChart({ childId, childSex }: Props) {
  const [logs, setLogs] = useState<GrowthLog[]>([]);
  const [metric, setMetric] = useState<'weight' | 'height'>('weight');
  const [expanded, setExpanded] = useState(false);

  useEffect(() => {
    if (!childId) return;
    fetch(`/api/profile/${childId}/growth`)
      .then((r) => r.json())
      .then(setLogs)
      .catch(console.error);
  }, [childId]);

  if (!childId) return null;

  const whoData = metric === 'weight'
    ? (childSex === 'female' ? WHO_GIRLS_WEIGHT : WHO_BOYS_WEIGHT)
    : (childSex === 'female' ? WHO_GIRLS_HEIGHT : WHO_BOYS_HEIGHT);

  const whoCurve = whoData.map(([age, value]) => ({
    ageMonths: age,
    who50: value,
    who15: value * 0.9,
    who85: value * 1.1,
    label: '',
  }));

  const childData = logs
    .filter((l) => (metric === 'weight' ? l.weight_kg : l.height_cm) != null)
    .map((l) => {
      const dob = new Date(l.measured_date);
      return {
        ageMonths: 0,
        childValue: metric === 'weight' ? l.weight_kg : l.height_cm,
        date: l.measured_date,
        label: '',
      };
    });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const form = e.target as HTMLFormElement;
    const data = new FormData(form);
    const payload = {
      child_id: childId,
      measured_date: data.get('date') as string,
      weight_kg: data.get('weight') ? parseFloat(data.get('weight') as string) : undefined,
      height_cm: data.get('height') ? parseFloat(data.get('height') as string) : undefined,
    };
    const res = await fetch('/api/profile/growth', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (res.ok) {
      const updated = await fetch(`/api/profile/${childId}/growth`).then((r) => r.json());
      setLogs(updated);
      form.reset();
    }
  };

  return (
    <div className="border-t border-gray-200 p-4">
      <button
        onClick={() => setExpanded(!expanded)}
        className="flex items-center justify-between w-full text-sm font-semibold text-gray-600 uppercase tracking-wider"
      >
        Growth Tracker
        <span className="text-xs text-gray-400">{expanded ? '▲' : '▼'}</span>
      </button>

      {expanded && (
        <div className="mt-3 space-y-3">
          <div className="flex gap-2">
            <button
              onClick={() => setMetric('weight')}
              className={`flex-1 py-1 text-xs rounded-md font-medium transition-colors ${
                metric === 'weight' ? 'bg-primary-500 text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              Weight
            </button>
            <button
              onClick={() => setMetric('height')}
              className={`flex-1 py-1 text-xs rounded-md font-medium transition-colors ${
                metric === 'height' ? 'bg-primary-500 text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              Height
            </button>
          </div>

          {childData.length > 0 && (
            <div className="h-48 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={childData} margin={{ top: 5, right: 10, left: 0, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                  <XAxis dataKey="date" tick={{ fontSize: 10 }} />
                  <YAxis tick={{ fontSize: 10 }} />
                  <Tooltip />
                  <Line
                    type="monotone"
                    dataKey="childValue"
                    stroke="#22c55e"
                    strokeWidth={2}
                    dot={{ r: 4, fill: '#22c55e' }}
                    name={metric === 'weight' ? 'Weight (kg)' : 'Height (cm)'}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-2 p-3 bg-gray-50 rounded-lg">
            <input
              type="date"
              name="date"
              required
              className="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm"
            />
            <div className="flex gap-2">
              <input
                type="number"
                name="weight"
                step="0.1"
                placeholder="Weight (kg)"
                className="flex-1 px-3 py-1.5 border border-gray-300 rounded-md text-sm"
              />
              <input
                type="number"
                name="height"
                step="0.1"
                placeholder="Height (cm)"
                className="flex-1 px-3 py-1.5 border border-gray-300 rounded-md text-sm"
              />
            </div>
            <button
              type="submit"
              className="w-full py-1.5 bg-primary-500 text-white rounded-md text-sm font-medium hover:bg-primary-600"
            >
              Log Measurement
            </button>
          </form>
        </div>
      )}
    </div>
  );
}
