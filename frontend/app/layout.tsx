import type { Metadata } from 'next';
import './globals.css';
import { BookOpen, Atom } from 'lucide-react';

export const metadata: Metadata = {
  title: 'MATLAB Scientific Computing Academy',
  description: 'Learn MATLAB through coding examples, numerical methods, physics, optics and photonics simulations.',
};
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body><header className="topbar"><a className="brand" href="/"><span className="brandmark"><Atom size={22}/></span><span>MATLAB <b>Scientific Academy</b></span></a><nav><a href="/#curriculum"><BookOpen size={16}/> Curriculum</a><a href="/simulations">Simulations</a><a className="nav-cta" href="/#start">Start learning <span>↗</span></a></nav></header>{children}<footer><div className="footer-inner"><div className="brand footer-brand"><span className="brandmark"><Atom size={20}/></span><span>MATLAB <b>Scientific Academy</b></span></div><p>Learn the code. Understand the science. Build the model.</p><small>Independent learning resource. MATLAB is a registered trademark of The MathWorks, Inc.</small></div></footer></body></html>
}
