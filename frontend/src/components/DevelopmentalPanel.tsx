import { useState, useEffect } from 'react';
import type { ChildProfile } from '../lib/types';
import { api } from '../lib/api';

interface Props {
  selectedChild: ChildProfile | null;
}

export default function DevelopmentalPanel({ selectedChild }: Props) {
  if (!selectedChild?.developmental_context) {
    return (
      <div className="p-4 text-sm text-gray-400">
        Select a child to view developmental context.
      </div>
    );
  }

  const ctx = selectedChild.developmental_context;

  return (
    <div className="p-4 space-y-3 overflow-y-auto">
      <div>
        <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">
          Developmental Stage
        </h3>
        <p className="text-sm font-medium text-gray-800 capitalize">{ctx.stage}</p>
        <p className="text-xs text-gray-500">{ctx.age_months} months old</p>
      </div>

      <div>
        <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">
          Erikson Stage
        </h3>
        <p className="text-sm text-gray-700">{ctx.erikson_stage}</p>
      </div>

      <div>
        <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">
          Piaget Stage
        </h3>
        <p className="text-sm text-gray-700">{ctx.piaget_stage}</p>
      </div>

      <div>
        <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">
          Key Milestones
        </h3>
        <ul className="space-y-1">
          {ctx.key_milestones.map((m, i) => (
            <li key={i} className="text-sm text-gray-700 flex items-start gap-2">
              <span className="text-primary-500 mt-1">•</span>
              {m}
            </li>
          ))}
        </ul>
      </div>

      <div>
        <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">
          Stage Guidance
        </h3>
        <p className="text-sm text-gray-700 leading-relaxed">{ctx.stage_guidance}</p>
      </div>
    </div>
  );
}
