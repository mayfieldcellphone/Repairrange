"use client";
import React, { useEffect, useState } from 'react';
import { LayoutDashboard, MessageSquare, Zap, UploadCloud, DollarSign, Users, ShieldAlert, CreditCard } from 'lucide-react';

// SaaS Color Theme
const statusColors: Record<string, string> = {
  active: 'bg-green-100 text-green-700 border-green-200',
  suspended: 'bg-red-100 text-red-700 border-red-200',
  trial: 'bg-blue-100 text-blue-700 border-blue-200'
};

export default function Dashboard() {
  const [activeBot, setActiveBot] = useState('Mayfield Repair');
  const [view, setView] = useState<'bots' | 'finance' | 'admin'>('bots'); 
  const [subscribers, setSubscribers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  // Initial UI state (Mock data for build stability)
  useEffect(() => {
    setSubscribers([
      { id: '1', name: "Mayfield Repair", status: "active", plan: "Pro", revenue: "$4,200" },
      { id: '2', name: "SelfRepairKit", status: "active", plan: "Enterprise", revenue: "$8,900" },
      { id: '3', name: "RepairBill", status: "trial", plan: "Basic", revenue: "$0" },
    ]);
    setLoading(false);
  }, []);

  return (
    <div className="flex h-screen overflow-hidden bg-slate-50 font-sans text-slate-900">
      {/* SIDEBAR */}
      <aside className="w-64 bg-slate-900 text-white flex flex-col">
        <div className="p-6 border-b border-slate-800 flex items-center gap-2">
          <Zap className="text-yellow-400 fill-yellow-400" />
          <span className="font-bold text-xl tracking-tight uppercase">BizHub AI</span>
        </div>
        
        <nav className="flex-1 p-4 space-y-2">
          <button onClick={() => setView('bots')} className={`w-full text-left px-4 py-2 rounded-lg flex items-center gap-3 ${view === 'bots' ? 'bg-blue-600' : 'hover:bg-slate-800'}`}>
            <LayoutDashboard size={18} /> AI Bot Manager
          </button>
          <button onClick={() => setView('finance')} className={`w-full text-left px-4 py-2 rounded-lg flex items-center gap-3 ${view === 'finance' ? 'bg-green-600' : 'hover:bg-slate-800'}`}>
            <DollarSign size={18} /> Financial Hub
          </button>
          <button onClick={() => setView('admin')} className={`w-full text-left px-4 py-2 rounded-lg flex items-center gap-3 ${view === 'admin' ? 'bg-red-600' : 'hover:bg-slate-800'}`}>
            <Users size={18} /> Admin Console
          </button>
        </nav>
      </aside>

      {/* MAIN CONTENT */}
      <main className="flex-1 flex flex-col overflow-auto">
        <header className="h-16 border-b px-8 flex items-center justify-between bg-white shadow-sm">
          <h1 className="text-xl font-bold">{activeBot} Settings</h1>
          <button className="bg-blue-600 text-white px-4 py-1.5 rounded-lg text-sm font-bold">
            Deploy to WhatsApp
          </button>
        </header>
        
        <div className="p-8">
          {view === 'admin' ? (
            <div className="space-y-6">
              <div className="bg-amber-50 border border-amber-200 p-4 rounded-xl flex items-center gap-3 text-amber-800">
                <ShieldAlert size={20} />
                <p className="text-sm font-bold">Owner Mode: Use caution when managing tenants.</p>
              </div>

              <div className="bg-white border rounded-xl overflow-hidden">
                <table className="w-full text-left text-sm">
                  <thead className="bg-slate-50 border-b">
                    <tr>
                      <th className="p-4">Business</th>
                      <th className="p-4">Status</th>
                      <th className="p-4">Control</th>
                    </tr>
                  </thead>
                  <tbody>
                    {subscribers.map((sub) => (
                      <tr key={sub.id} className="border-b">
                        <td className="p-4 font-bold">{sub.name}</td>
                        <td className="p-4">
                           <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase border ${statusColors[sub.status]}`}>
                              {sub.status}
                           </span>
                        </td>
                        <td className="p-4">
                          <button className="text-blue-600 font-bold text-xs">SUSPEND</button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          ) : view === 'finance' ? (
            <div className="p-10 bg-white border rounded-3xl shadow-sm">
               <h2 className="text-slate-400 text-xs font-bold uppercase mb-2">Total SaaS Revenue</h2>
               <div className="text-5xl font-black">$13,100.00</div>
            </div>
          ) : (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
               <section className="p-10 border-2 border-dashed border-slate-200 rounded-3xl bg-white flex flex-col items-center justify-center text-slate-400">
                  <UploadCloud size={64} className="mb-4" />
                  <p className="font-bold text-slate-600 text-lg">AI Knowledge Portal</p>
                  <p className="text-sm">Drag PDFs or CSVs to train {activeBot}</p>
               </section>
               <section className="p-8 border rounded-3xl bg-slate-900 text-white min-h-[400px]">
                  <div className="font-bold flex items-center gap-2 mb-4">
                     <Zap size={18} className="text-yellow-400" /> Implementation Assistant
                  </div>
                  <div className="bg-slate-800 p-4 rounded-xl text-sm italic text-slate-500 border border-slate-700">
                     Ready for instructions. I can parse files and implement AI logic automatically.
                  </div>
               </section>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
