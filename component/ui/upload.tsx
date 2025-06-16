// File: components/ui/upload.tsx
"use client"
export function Upload({ file, setFile }: { file: File | null, setFile: (file: File) => void }) {
  return (
    <div className="border-2 border-dashed p-4 rounded-lg text-center">
      <input type="file" accept="image/*,video/*,audio/*" onChange={(e) => {
        const f = e.target.files?.[0]
        if (f) setFile(f)
      }} />
      {file && <p className="mt-2 text-sm text-gray-600">Selected: {file.name}</p>}
    </div>
  )
}

