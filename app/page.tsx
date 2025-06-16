// peacewatch-webapp (Next.js + Supabase + Tailwind + AI Integration)

// File: app/page.tsx
import Link from "next/link"

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-6 text-center">
      <h1 className="text-4xl font-bold mb-4">🕊️ PeaceWatch</h1>
      <p className="text-lg text-gray-600 mb-8">AI-powered community tool to monitor and report acts of harm or intimidation — with love, truth, and protection.</p>
      <div className="flex gap-4">
        <Link href="/report" className="bg-blue-600 text-white px-6 py-3 rounded-xl shadow hover:bg-blue-700 transition">Submit Report</Link>
        <Link href="/dashboard" className="bg-gray-200 px-6 py-3 rounded-xl hover:bg-gray-300 transition">View Dashboard</Link>
      </div>
    </main>
  )
}
