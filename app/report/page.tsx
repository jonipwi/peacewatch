// File: app/report/page.tsx
"use client"
import { useState } from "react"
import { Upload } from "@/components/ui/upload"
import { Textarea } from "@/components/ui/textarea"
import { Button } from "@/components/ui/button"

export default function ReportPage() {
  const [description, setDescription] = useState("")
  const [file, setFile] = useState<File | null>(null)

  const handleSubmit = async () => {
    if (!file || !description) return alert("Please upload evidence and describe the event.")
    const formData = new FormData()
    formData.append("file", file)
    formData.append("description", description)

    const response = await fetch("/api/report", { method: "POST", body: formData })
    const result = await response.json()

    if (result.success) {
      alert("Report submitted and AI processing started.")
      setDescription("")
      setFile(null)
    } else {
      alert("Error submitting report: " + result.error)
    }
  }

  return (
    <div className="max-w-xl mx-auto p-6">
      <h2 className="text-2xl font-semibold mb-4">📤 Submit Report</h2>
      <Upload file={file} setFile={setFile} />
      <Textarea
        placeholder="Describe what happened, where, and when."
        className="mt-4"
        rows={5}
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />
      <Button onClick={handleSubmit} className="mt-4 w-full">Submit</Button>
    </div>
  )
}
