// File: app/api/report/route.ts
import { NextResponse } from "next/server"
import { createClient } from "@supabase/supabase-js"
import fs from "fs/promises"
import path from "path"

export async function POST(req: Request) {
  const form = await req.formData()
  const file = form.get("file") as File
  const description = form.get("description") as string

  const buffer = Buffer.from(await file.arrayBuffer())
  const supabase = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.SUPABASE_SERVICE_ROLE_KEY!)

  const fileName = `evidence/${Date.now()}-${file.name}`
  const { data, error } = await supabase.storage.from("reports").upload(fileName, buffer, { contentType: file.type, upsert: true })
  if (error) return NextResponse.json({ error: error.message }, { status: 500 })

  // Insert metadata into DB
  const { error: insertError } = await supabase.from("incidents").insert({ description, file_url: data?.path })
  if (insertError) return NextResponse.json({ error: insertError.message }, { status: 500 })

  // Placeholder: Trigger AI analysis later here (e.g., webhook or background worker)

  return NextResponse.json({ success: true })
}
