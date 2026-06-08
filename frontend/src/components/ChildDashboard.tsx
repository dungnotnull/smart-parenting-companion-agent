import type { ChildProfile } from '../lib/types';
import MilestoneTracker from './MilestoneTracker';
import GrowthChart from './GrowthChart';

interface Props {
  selectedChild: ChildProfile | null;
}

export default function ChildDashboard({ selectedChild }: Props) {
  if (!selectedChild) return null;

  return (
    <div className="flex flex-col">
      <MilestoneTracker childId={selectedChild.id} />
      <GrowthChart childId={selectedChild.id} childSex={selectedChild.sex} />
      {selectedChild.developmental_context && (
        <div className="border-t border-gray-200 p-4">
          <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
            Upcoming Milestones to Watch
          </h3>
          <ul className="space-y-1.5">
            {selectedChild.developmental_context.key_milestones.slice(0, 5).map((m, i) => (
              <li key={i} className="text-sm text-gray-700 flex items-start gap-2">
                <span className="text-amber-400 mt-0.5">○</span>
                {m}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
