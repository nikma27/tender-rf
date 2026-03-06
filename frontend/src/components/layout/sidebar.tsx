"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import {
  Search,
  Sparkles,
  FileText,
  Settings,
} from "lucide-react"
import { cn } from "@/lib/utils"
import { ContactWidget } from "./contact-widget"

const navItems = [
  { href: "/", label: "Поиск", icon: Search },
  { href: "/ai-analysis", label: "AI Анализ", icon: Sparkles },
  { href: "/my-tenders", label: "Мои тендеры", icon: FileText },
  { href: "/settings", label: "Настройки", icon: Settings },
]

export function Sidebar() {
  const pathname = usePathname()

  return (
    <aside className="flex h-full w-60 flex-col border-r border-white/10 bg-white/5 backdrop-blur-md">
      <div className="flex h-16 items-center border-b border-white/10 px-6">
        <Link href="/" className="text-lg font-semibold tracking-tight">
          Tender RF
        </Link>
      </div>
      <nav className="flex-1 space-y-1 p-4">
        {navItems.map((item) => {
          const isActive = pathname === item.href
          const Icon = item.icon
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors",
                isActive
                  ? "bg-white/10 text-foreground"
                  : "text-muted-foreground hover:bg-white/5 hover:text-foreground"
              )}
            >
              <Icon className="size-4 shrink-0" />
              {item.label}
            </Link>
          )
        })}
      </nav>
      <div className="border-t border-white/10 p-4">
        <ContactWidget />
      </div>
    </aside>
  )
}
