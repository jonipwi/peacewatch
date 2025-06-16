// File: components/ui/button.tsx
export function Button({ children, ...props }: React.ButtonHTMLAttributes<HTMLButtonElement>) {
  return (
    <button {...props} className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition" >
      {children}
    </button>
  )
}
