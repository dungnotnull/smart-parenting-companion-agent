import { useState } from 'react';
import type { ChildProfile } from '../lib/types';

interface Props {
  profiles: ChildProfile[];
  selectedId: number | null;
  onSelect: (id: number) => void;
  onCreate: (data: {
    name: string;
    dob: string;
    sex: string;
    preferred_language: string;
  }) => void;
}

export default function ProfilePanel({ profiles, selectedId, onSelect, onCreate }: Props) {
  const [showForm, setShowForm] = useState(false);
  const [name, setName] = useState('');
  const [dob, setDob] = useState('');
  const [sex, setSex] = useState('male');
  const [language, setLanguage] = useState('en');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onCreate({ name, dob, sex, preferred_language: language });
    setName('');
    setDob('');
    setShowForm(false);
  };

  return (
    <div className="border-b border-gray-200 p-4">
      <div className="flex items-center gap-2 mb-3">
        <h2 className="text-sm font-semibold text-gray-600 uppercase tracking-wider">
          Children
        </h2>
        <button
          onClick={() => setShowForm(!showForm)}
          className="ml-auto text-xs text-primary-600 hover:text-primary-800 font-medium"
        >
          {showForm ? 'Cancel' : '+ Add Child'}
        </button>
      </div>

      {profiles.length === 0 && !showForm && (
        <p className="text-sm text-gray-400">
          No children added yet. Create a profile to get started.
        </p>
      )}

      <div className="flex flex-wrap gap-2">
        {profiles.map((child) => (
          <button
            key={child.id}
            onClick={() => onSelect(child.id)}
            className={`px-3 py-1.5 rounded-full text-sm font-medium transition-colors ${
              selectedId === child.id
                ? 'bg-primary-500 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            {child.name}
            {child.stage && (
              <span className="ml-1.5 text-xs opacity-75">
                ({child.stage})
              </span>
            )}
          </button>
        ))}
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="mt-3 space-y-2 p-3 bg-gray-50 rounded-lg">
          <input
            type="text"
            placeholder="Child's name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-primary-400"
          />
          <input
            type="date"
            value={dob}
            onChange={(e) => setDob(e.target.value)}
            required
            className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-primary-400"
          />
          <select
            value={sex}
            onChange={(e) => setSex(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-primary-400"
          >
            <option value="male">Male</option>
            <option value="female">Female</option>
          </select>
          <select
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-primary-400"
          >
            <option value="en">English</option>
            <option value="vi">Tiếng Việt</option>
          </select>
          <button
            type="submit"
            className="w-full py-2 bg-primary-500 text-white rounded-md text-sm font-medium hover:bg-primary-600 transition-colors"
          >
            Create Profile
          </button>
        </form>
      )}
    </div>
  );
}
