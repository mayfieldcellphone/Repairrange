"use client";
import React, { useEffect, useState } from 'react';
import { getAllSubscribers, setSubscriptionStatus, getFinancialStats } from '../../../lib/admin';
import { LayoutDashboard, MessageSquare, Zap, UploadCloud, DollarSign, Users, ShieldAlert, Github, Send } from 'lucide-react';

export default function Dashboard() {
  const [activeBot, setActiveBot] = useState('Mayfield Repair');
  const [view, setView] = useState<'bots' | 'finance' | 'admin'>('bots'); 
  const [subscribers, setSubscribers] = useState<any[]>([]);
  const [stats, setStats] = useState({ totalRevenue: '$0', activeCount: 0 });
  const [instruction, setInstruction] = useState('');
  const [aiLog, setAiLog] = useState<string[]>(["Hi! I am your BizHub Implementation Assistant. Tell me what to change in your bot's training or settings."]);
  const [isImplementing, setIsImplementing] = useState(false);

  useEffect(() => {
    async function loadData() {
      const data = await getAllSubscribers();
      const summary = await getFinancialStats();
      setSubscribers(data);
      setStats(summary);
    }
    loadData();
  }, [view]);

  const handleImplement = async () => {
    if (!instruction) return;
    setIsImplementing(true);
    setAiLog(prev => [...prev, `User: ${instruction}`]);
    
    try {
        const response = await fetch('/api/builder', {
            method: 'POST',
            body: JSON.stringify({
                instruction,
                shopId: activeBot.toLowerCase().replace(' ', '_'),
                currentData: {} 
            })
        });
        const data = await response.json();
        setAiLog(prev => [...prev, `AI: ${data.message || 'Action completed successfully.'}`]);
        setInstruction('');
    } catch (e) {
        setAiLog(prev => [...prev, "AI: I encountered an error during implementation."]);
    } finally {
        setIsImplementing(false);
    }
  };

  return (
    <div className="flex h-screen overflow-hidden bg-slate-50 font-sans text-slate-900">
      {/* SIDEBAR */}
      <aside className="w-64 bg-slate-900 text-white flex flex-col shadow-2xl">
        <div className="p-6 border-b border-slate-800 flex items-center gap-2">
          <Zap className="text-yellow-400 fill-yellow-400" size={24} />
          <span className="font-bold text-2xl tracking-tighter uppercase italic">BizHub AI</span>
        </div>
        <nav className="flex-1 p-4 space-y-2">
          <button onClick={() => setView('bots')} className={`w-full text-left px-4 py-2 rounded-lg flex items-center gap-3 transition-all ${view === 'bots' ? 'bg-blue-600 shadow-lg' : 'hover:bg-slate-800'}`}>
            <LayoutDashboard size={18} /> Bot Builder
          </button>
          <button onClick={() => setView('finance')} className={`w-full text-left px-4 py-2 rounded-lg flex items-center gap-3 transition-all ${view === 'finance' ? 'bg-green-600 shadow-lg' : 'hover:bg-slate-800'}`}>
            <DollarSign size={18} /> Finance Hub
          </button>
          <button onClick={() => setView('admin')} className={`w-full text-left px-4 py-2 rounded-lg flex items-center gap-3 transition-all ${view === 'admin' ? 'bg-red-600 shadow-lg' : 'hover:bg-slate-800'}`}>
            <Users size={18} /> Admin Console
          </button>
          <div className="mt-8 pt-4 border-t border-slate-800 text-[10px] uppercase font-bold text-slate-500 mb-2">My Entities</div>
          {['Mayfield Repair', 'SelfRepairKit', 'RepairBill'].map(bot => (
            <button key={bot} onClick={() => setActiveBot(bot)} className={`w-full text-left px-4 py-1.5 rounded text-sm ${activeBot === bot ? 'text-blue-400 font-bold' : 'text-slate-400 hover:text-white'}`}>
               • {bot}
            </button>
          ))}
        </nav>
      </aside>

      {/* MAIN CONTENT */}
      <main className="flex-1 flex flex-col overflow-auto bg-white">
        <header className="h-16 border-b px-8 flex items-center justify-between sticky top-0 bg-white/80 backdrop-blur-sm z-10">
          <h1 className="text-xl font-black text-slate-800 uppercase tracking-tight">{view === 'admin' ? 'Global Admin' : `${activeBot} Control`}</h1>
          <div className="flex gap-4">
             <button className="flex items-center gap-2 text-xs font-bold text-slate-500 hover:text-blue-600 uppercase tracking-widest"><Github size={14} /> Link Repo</button>
             <button className="bg-blue-600 text-white px-5 py-2 rounded-full text-xs font-black shadow-lg hover:scale-105 transition-all">DEPLOY LIVE</button>
          </div>
        </header>
        
        <div className="p-8 h-full">
          {view === 'bots' ? (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 h-full">
               <div className="lg:col-span-2 space-y-6">
                  <section className="p-8 border rounded-3xl bg-slate-50 shadow-inner flex flex-col items-center justify-center min-h-[300px] group border-slate-200 hover:border-blue-300 transition-all cursor-pointer">
                     <UploadCloud size={48} className="text-slate-300 group-hover:text-blue-500 transition-colors mb-4" />
                     <p className="font-bold text-slate-900">Upload Knowledge Data</p>
                     <p className="text-xs text-slate-500 text-center max-w-xs mt-2 font-medium">Inject PDFs, CSVs or Website Links. The Implementation AI will parse them instantly.</p>
                  </section>
                  <div className="grid grid-cols-2 gap-4">
                     <div className="p-4 border rounded-2xl bg-white shadow-sm font-bold text-xs uppercase text-slate-400">Total Conversations: <span className="text-slate-900 block text-lg">1,248</span></div>
                     <div className="p-4 border rounded-2xl bg-white shadow-sm font-bold text-xs uppercase text-slate-400">AI Accuracy: <span className="text-green-600 block text-lg">98.2%</span></div>
                  </div>
               </div>

               {/* IMPLEMENTATION BOT (SIDEBAR CHAT) */}
               <div className="flex flex-col border rounded-3xl shadow-2xl bg-slate-900 text-white overflow-hidden max-h-[600px]">
                  <div className="p-4 bg-slate-800 font-black text-[10px] uppercase tracking-[0.2em] flex items-center justify-between">
                     <div className="flex items-center gap-2"><span className="w-2 h-2 bg-green-400 rounded-full animate-pulse" /> AI Architect</div>
                     <Settings size={14} className="text-slate-500" />
                  </div>
                  <div className="flex-1 p-4 overflow-auto space-y-4 text-xs font-medium">
                     {aiLog.map((log, i) => (
                        <div key={i} className={`p-3 rounded-2xl ${log.startsWith('User') ? 'bg-blue-600 ml-4' : 'bg-slate-800 mr-4 border border-slate-700'}`}>
                           {log}
                        </div>
                     ))}
                  </div>
                  <div className="p-4 bg-slate-800">
                     <div className="flex gap-2 items-center bg-slate-900 p-2 rounded-2xl border border-slate-700">
                        <input 
                           value={instruction}
                           onChange={(e) => setInstruction(e.target.value)}
                           disabled={isImplementing}
                           className="flex-1 bg-transparent border-none focus:ring-0 text-white placeholder-slate-600 text-xs" 
                           placeholder="Type instruction..." 
                        />
                        <button onClick={handleImplement} disabled={isImplementing} className="p-2 bg-blue-600 rounded-xl text-white hover:bg-blue-500 transition-all">
                           <Send size={16} />
                        </button>
                     </div>
                  </div>
               </div>
            </div>
          ) : view === 'finance' ? (
            <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
               <div className="p-12 bg-white border border-slate-100 rounded-[3rem] shadow-2xl relative overflow-hidden">
                  <div className="absolute top-0 right-0 w-64 h-64 bg-blue-50/50 rounded-full -mr-32 -mt-32 blur-3xl" />
                  <div className="text-slate-400 text-xs font-black uppercase tracking-[0.3em] mb-4 relative">Total Platform Revenue</div>
                  <div className="text-7xl font-black text-slate-900 tracking-tighter relative">{stats.totalRevenue}</div>
                  <div className="mt-8 flex gap-4 relative">
                     <span className="px-4 py-1.5 bg-green-100 text-green-700 rounded-full text-xs font-black">+{stats.activeCount} ACTIVE SHOPS</span>
                  </div>
               </div>
            </div>
          ) : (
            <div className="bg-white border rounded-3xl shadow-xl overflow-hidden animate-in fade-in duration-500">
               <table className="w-full text-left text-sm font-medium">
                  <thead className="bg-slate-50 text-slate-400 uppercase text-[10px] font-black tracking-widest border-b">
                     <tr><th className="p-6 text-slate-900">Tenant</th><th className="p-6">Status</th><th className="p-6 text-right">Actions</th></tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                     {subscribers.map((sub) => (
                        <tr key={sub.id} className="hover:bg-slate-50/50 transition-all group">
                           <td className="p-6 font-black text-slate-800 text-base">{sub.name}</td>
                           <td className="p-6">
                              <span className={`px-3 py-1 rounded-full text-[10px] font-black uppercase border ${sub.status === 'active' ? 'bg-green-100 text-green-700 border-green-200' : 'bg-red-100 text-red-700 border-red-200'}`}>
                                 {sub.status}
                              </span>
                           </td>
                           <td className="p-6 text-right opacity-0 group-hover:opacity-100 transition-opacity">
                              <button className="text-blue-600 font-black text-xs mr-4">ANALYZE</button>
                              <button className="text-red-600 font-black text-xs underline decoration-2 underline-offset-4">SUSPEND</button>
                           </td>
                        </tr>
                     ))}
                  </tbody>
               </table>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
