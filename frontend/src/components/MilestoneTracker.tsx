import { useState, useEffect } from 'react';
import { api } from '../lib/api';
import type { MilestoneLog } from '../lib/types';

interface Props {
  childId: number | null;
}

const MILESTONE_DOMAINS = ['motor', 'language', 'cognitive', 'social-emotional', 'self-care'];
const DOMAIN_LABELS: Record<string, string> = {
  motor: 'Motor',
  language: 'Language',
  cognitive: 'Cognitive',
  'social-emotional': 'Social-Emotional',
  'self-care': 'Self-Care',
};

export default function MilestoneTracker({ childId }: Props) {
  const [milestones, setMilestones] = useState<MilestoneLog[]>([]);
  const [domain, setDomain] = useState('motor');
  const [label, setLabel] = useState('');
  const [achievedDate, setAchievedDate] = useState('');
  const [notes, setNotes] = useState('');
  const [expanded, setExpanded] = useState(false);

  useEffect(() => {
    if (!childId) return;
    fetch(`/api/profile/${childId}/milestones`)
      .then((r) => r.json())
      .then(setMilestones)
      .catch(console.error);
  }, [childId]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!childId || !label || !achievedDate) return;
    const res = await fetch('/api/profile/milestone', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ child_id: childId, domain, milestone_label: label, achieved_date: achievedDate, notes }),
    });
    if (res.ok) {
      setLabel('');
      setNotes('');
      const updated = await fetch(`/api/profile/${childId}/milestones`).then((r) => r.json());
      setMilestones(updated);
    }
  };

  if (!childId) return null;

  return (
    <div className="border-t border-gray-200 p-4">
      <button
        onClick={() => setExpanded(!expanded)}
        className="flex items-center justify-between w-full text-sm font-semibold text-gray-600 uppercase tracking-wider"
      >
        Milestone Tracker
        <span className="text-xs text-gray-400">{expanded ? '▲' : '▼'}</span>
      </button>

      {expanded && (
        <div className="mt-3 space-y-3">
          <form onSubmit={handleSubmit} className="space-y-2 p-3 bg-gray-50 rounded-lg">
            <select
              value={domain}
              onChange={(e) => setDomain(e.target.value)}
              className="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm"
            >
              {MILESTONE_DOMAINS.map((d) => (
                <option key={d} value={d}>{DOMAIN_LABELS[d]}</option>
              ))}
            </select>
            <input
              type="text"
              placeholder="Milestone (e.g., 'First steps')"
              value={label}
              onChange={(e) => setLabel(e.target.value)}
              required
              className="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm"
            />
            <input
              type="date"
              value={achievedDate}
              onChange={(e) => setAchievedDate(e.target.value)}
              required
              className="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm"
            />
            <input
              type="text"
              placeholder="Notes (optional)"
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              className="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm"
            />
            <button
              type="submit"
              className="w-full py-1.5 bg-primary-500 text-white rounded-md text-sm font-medium hover:bg-primary-600"
            >
              Log Milestone
            </button>
          </form>

          {milestones.length > 0 && (
            <div className="space-y-1 max-h-48 overflow-y-auto">
              {milestones.map((m) => (
                <div key={m.id} className="flex items-center gap-2 text-sm py-1">
                  <span className={`inline-block w-2 h-2 rounded-full ${
                    m.domain === 'motor' ? 'bg-blue-400' :
                    m.domain === 'language' ? 'bg-green-400' :
                    m.domain === 'cognitive' ? 'bg-purple-400' :
                    m.domain === 'social-emotional' ? 'bg-pink-400' :
                    'bg-yellow-400'
                  }`} />
                  <span className="font-medium">{m.milestone_label}</span>
                  <span className="text-gray-400 text-xs">{m.achieved_date}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
