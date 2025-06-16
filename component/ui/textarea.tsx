// File: components/ui/textarea.tsx
import * as React from "react"
import { cn } from "@/lib/utils"
export const Textarea = React.forwardRef(({ className, ...props }: React.TextareaHTMLAttributes<HTMLTextAreaElement>, ref) => {
  return <textarea ref={ref} className={cn("w-full p-2 border rounded-md", className)} {...props} />
})
Textarea.displayName = "Textarea"
