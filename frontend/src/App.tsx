import { useState, useEffect, useCallback } from 'react';
import ChatWindow from './components/ChatWindow';
import ChatInput from './components/ChatInput';
import ProfilePanel from './components/ProfilePanel';
import DevelopmentalPanel from './components/DevelopmentalPanel';
import ChildDashboard from './components/ChildDashboard';
import { useWebSocket } from './hooks/useWebSocket';
import { api } from './lib/api';
import type { ChildProfile } from './lib/types';

export default function App() {
  const [profiles, setProfiles] = useState<ChildProfile[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [selectedChild, setSelectedChild] = useState<ChildProfile | null>(null);
  const [sidebarView, setSidebarView] = useState<'context' | 'dashboard' | 'info'>('context');

  const { messages, sendMessage, isStreaming } = useWebSocket(selectedId);

  const loadProfiles = useCallback(async () => {
    try {
      const list = await api.listChildren();
      setProfiles(list);
    } catch (err) {
      console.error('Failed to load profiles:', err);
    }
  }, []);

  useEffect(() => {
    loadProfiles();
  }, [loadProfiles]);

  useEffect(() => {
    if (!selectedId) {
      setSelectedChild(null);
      return;
    }
    api.getChild(selectedId).then(setSelectedChild).catch(console.error);
  }, [selectedId]);

  const handleCreateChild = useCallback(
    async (data: {
      name: string;
      dob: string;
      sex: string;
      preferred_language: string;
    }) => {
      try {
        await api.createChild(data);
        await loadProfiles();
      } catch (err) {
        console.error('Failed to create child:', err);
      }
    },
    [loadProfiles],
  );

  return (
    <div className="h-screen flex flex-col max-w-6xl mx-auto">
      <header className="flex items-center justify-between px-6 py-3 border-b border-gray-200 bg-white">
        <div>
          <h1 className="text-lg font-bold text-gray-900">Smart Parenting Companion</h1>
          <p className="text-xs text-gray-500">
            Evidence-based AI parenting guide — birth to adulthood, always learning
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setSidebarView('context')}
            className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${
              sidebarView === 'context'
                ? 'bg-primary-100 text-primary-700'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            Context
          </button>
          <button
            onClick={() => setSidebarView('dashboard')}
            className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${
              sidebarView === 'dashboard'
                ? 'bg-primary-100 text-primary-700'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            Dashboard
          </button>
          <button
            onClick={() => setSidebarView('info')}
            className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${
              sidebarView === 'info'
                ? 'bg-primary-100 text-primary-700'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            Info
          </button>
        </div>
      </header>

      <ProfilePanel
        profiles={profiles}
        selectedId={selectedId}
        onSelect={setSelectedId}
        onCreate={handleCreateChild}
      />

      <div className="flex-1 flex overflow-hidden">
        <main className="flex-1 flex flex-col min-w-0">
          <ChatWindow messages={messages} isStreaming={isStreaming} />
          <ChatInput
            onSend={sendMessage}
            isStreaming={isStreaming}
            disabled={!selectedId}
          />
        </main>

        <aside className="w-80 border-l border-gray-200 overflow-y-auto bg-gray-50 hidden lg:block">
          {sidebarView === 'context' && <DevelopmentalPanel selectedChild={selectedChild} />}
          {sidebarView === 'dashboard' && <ChildDashboard selectedChild={selectedChild} />}
          {sidebarView === 'info' && (
            <div className="p-4 text-sm text-gray-600 space-y-3">
              <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider">
                About
              </h3>
              <p>
                Smart Parenting Companion provides evidence-based parenting guidance
                grounded in peer-reviewed research from PubMed, AAP, WHO, and more.
              </p>
              <p>
                All your family data is encrypted locally. No personally identifiable
                information is ever sent to external services.
              </p>
              <div className="pt-3 border-t border-gray-200">
                <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
                  Evidence Levels
                </h3>
                <div className="space-y-1.5">
                  <div className="flex items-center gap-2">
                    <span className="evidence-badge-rct">RCT</span>
                    <span className="text-xs text-gray-500">Randomized Controlled Trial</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="evidence-badge-meta-analysis">Meta</span>
                    <span className="text-xs text-gray-500">Meta-analysis / Systematic Review</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="evidence-badge-guideline">Guideline</span>
                    <span className="text-xs text-gray-500">Official Clinical Guideline</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="evidence-badge-observational">Obs</span>
                    <span className="text-xs text-gray-500">Observational Study</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="evidence-badge-expert-opinion">Exp</span>
                    <span className="text-xs text-gray-500">Expert Opinion</span>
                  </div>
                </div>
              </div>
            </div>
          )}
        </aside>
      </div>
    </div>
  );
}
