import { useState, useEffect } from 'react';

interface KnowledgeStats {
  total_chunks: number;
  collection_name: string;
}

interface CrawlLog {
  id: number;
  source: string;
  papers_found: number;
  papers_added: number;
  topics: string;
  notable_findings: string;
  status: string;
  created_at: string;
}

export default function AdminDashboard() {
  const [stats, setStats] = useState<KnowledgeStats | null>(null);
  const [crawlLogs, setCrawlLogs] = useState<CrawlLog[]>([]);
  const [crawling, setCrawling] = useState(false);
  const [crawlResult, setCrawlResult] = useState<string | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);

  const loadStats = async () => {
    try {
      const res = await fetch('/api/admin/knowledge-stats');
      if (res.ok) setStats(await res.json());
    } catch (e) {
      setLoadError('Failed to load stats');
    }
  };

  const loadCrawlLogs = async () => {
    try {
      const res = await fetch('/api/admin/crawl-logs');
      if (res.ok) setCrawlLogs(await res.json());
    } catch (e) {
      setLoadError('Failed to load crawl logs');
    }
  };

  useEffect(() => {
    loadStats();
    loadCrawlLogs();
  }, []);

  const triggerCrawl = async () => {
    setCrawling(true);
    setCrawlResult(null);
    try {
      const res = await fetch('/api/admin/trigger-crawl', { method: 'POST' });
      const data = await res.json();
      setCrawlResult(JSON.stringify(data, null, 2));
      loadStats();
      loadCrawlLogs();
    } catch (e) {
      setCrawlResult('Crawl failed: ' + (e as Error).message);
    }
    setCrawling(false);
  };

  return (
    <div className="p-6 max-w-4xl mx-auto space-y-6">
      <div>
        <h1 className="text-xl font-bold text-gray-900">Admin Dashboard</h1>
        <p className="text-sm text-gray-500">Knowledge base management and ingestion monitoring</p>
      </div>

      {loadError && (
        <div className="bg-red-50 border border-red-200 text-red-700 rounded-lg p-3 text-sm">
          {loadError}
        </div>
      )}

      <div className="grid grid-cols-2 gap-4">
        <div className="bg-white border border-gray-200 rounded-xl p-4">
          <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
            Knowledge Base Size
          </h3>
          <p className="text-3xl font-bold text-primary-600">
            {stats?.total_chunks ?? '—'}
          </p>
          <p className="text-xs text-gray-400 mt-0.5">chunks indexed</p>
        </div>
        <div className="bg-white border border-gray-200 rounded-xl p-4">
          <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
            Collection
          </h3>
          <p className="text-lg font-semibold text-gray-700">
            {stats?.collection_name ?? '—'}
          </p>
          <p className="text-xs text-gray-400 mt-0.5">vector store collection</p>
        </div>
      </div>

      <div className="bg-white border border-gray-200 rounded-xl p-4">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider">
            Ingestion Control
          </h3>
          <button
            onClick={triggerCrawl}
            disabled={crawling}
            className="px-4 py-1.5 bg-primary-500 text-white rounded-lg text-sm font-medium hover:bg-primary-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {crawling ? 'Running...' : 'Trigger Crawl Now'}
          </button>
        </div>
        {crawlResult && (
          <pre className="bg-gray-50 border border-gray-200 rounded-lg p-3 text-xs text-gray-700 overflow-x-auto max-h-48">
            {crawlResult}
          </pre>
        )}
      </div>

      <div className="bg-white border border-gray-200 rounded-xl p-4">
        <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
          Crawl History
        </h3>
        {crawlLogs.length === 0 ? (
          <p className="text-sm text-gray-400">No crawl logs yet.</p>
        ) : (
          <div className="space-y-2 max-h-80 overflow-y-auto">
            {crawlLogs.map((log) => (
              <div
                key={log.id}
                className="border border-gray-100 rounded-lg p-3 text-sm"
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="font-medium text-gray-700">{log.source}</span>
                  <span className="text-xs text-gray-400">
                    {new Date(log.created_at).toLocaleString()}
                  </span>
                </div>
                <p className="text-gray-600">
                  Found: {log.papers_found} | Added: {log.papers_added}
                  {' | '}
                  <span className={log.status === 'success' ? 'text-green-600' : 'text-red-600'}>
                    {log.status}
                  </span>
                </p>
                {log.notable_findings && (
                  <p className="text-xs text-gray-500 mt-1 line-clamp-2">
                    {log.notable_findings}
                  </p>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
