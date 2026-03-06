"use client"

import { useCallback, useState } from "react"
import { Upload, FileText, Loader2, AlertTriangle, FileWarning, Clock, Wrench, TrendingUp } from "lucide-react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

const API_URL = "http://localhost:8000/api/analyze"

export interface AnalysisResult {
  file_name: string
  hidden_risks: string[]
  unclear_terms: string[]
  short_deadlines: string[]
  technical_traps: string[]
  margin_estimation: string
}

const ACCEPTED_TYPES = [
  "application/pdf",
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
]

const MAX_SIZE = 10 * 1024 * 1024 // 10MB

function AnalysisResultsCard({ result }: { result: AnalysisResult }) {
  const sections = [
    {
      key: "hidden_risks",
      title: "Скрытые риски",
      items: result.hidden_risks,
      icon: AlertTriangle,
      className: "border-amber-500/30 bg-amber-500/5",
    },
    {
      key: "unclear_terms",
      title: "Неоднозначные формулировки",
      items: result.unclear_terms,
      icon: FileWarning,
      className: "border-blue-500/30 bg-blue-500/5",
    },
    {
      key: "short_deadlines",
      title: "Сжатые сроки",
      items: result.short_deadlines,
      icon: Clock,
      className: "border-orange-500/30 bg-orange-500/5",
    },
    {
      key: "technical_traps",
      title: "Технические ловушки",
      items: result.technical_traps,
      icon: Wrench,
      className: "border-red-500/30 bg-red-500/5",
    },
  ]

  return (
    <div className="space-y-4">
      <p className="text-sm text-muted-foreground">
        Анализ: <span className="font-medium text-foreground">{result.file_name}</span>
      </p>

      <div className="grid gap-4 sm:grid-cols-2">
        {sections.map(({ key, title, items, icon: Icon, className }) =>
          items.length > 0 ? (
            <Card key={key} className={cn("border backdrop-blur-md", className)}>
              <CardHeader className="pb-2">
                <CardTitle className="flex items-center gap-2 text-sm font-medium">
                  <Icon className="size-4" />
                  {title}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-1.5 text-sm">
                  {items.map((item, i) => (
                    <li key={i} className="flex gap-2">
                      <span className="text-muted-foreground">•</span>
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          ) : null
        )}
      </div>

      {result.margin_estimation && (
        <Card className="border-emerald-500/30 bg-emerald-500/5 backdrop-blur-md">
          <CardHeader className="pb-2">
            <CardTitle className="flex items-center gap-2 text-sm font-medium">
              <TrendingUp className="size-4" />
              Рекомендация по марже
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm">{result.margin_estimation}</p>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

export function DocumentDropzone() {
  const [isDragActive, setIsDragActive] = useState(false)
  const [file, setFile] = useState<File | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [result, setResult] = useState<AnalysisResult | null>(null)

  const validateFile = useCallback((f: File) => {
    setError(null)
    if (!ACCEPTED_TYPES.includes(f.type)) {
      setError("Поддерживаются только PDF и Word (.pdf, .docx)")
      return false
    }
    if (f.size > MAX_SIZE) {
      setError("Максимальный размер файла — 10 МБ")
      return false
    }
    return true
  }, [])

  const onDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault()
      setIsDragActive(false)
      const droppedFile = e.dataTransfer.files[0]
      if (droppedFile && validateFile(droppedFile)) {
        setFile(droppedFile)
        setResult(null)
      }
    },
    [validateFile]
  )

  const onDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragActive(true)
  }, [])

  const onDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragActive(false)
  }, [])

  const onFileSelect = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const selectedFile = e.target.files?.[0]
      if (selectedFile && validateFile(selectedFile)) {
        setFile(selectedFile)
        setResult(null)
      }
    },
    [validateFile]
  )

  const removeFile = useCallback(() => {
    setFile(null)
    setError(null)
    setResult(null)
  }, [])

  const analyzeFile = useCallback(async () => {
    if (!file) return
    setIsLoading(true)
    setError(null)
    setResult(null)

    try {
      const formData = new FormData()
      formData.append("file", file)

      const res = await fetch(API_URL, {
        method: "POST",
        body: formData,
      })

      if (!res.ok) {
        const data = await res.json().catch(() => ({}))
        const detail = data.detail
        const msg = Array.isArray(detail)
          ? detail.map((e: { msg?: string }) => e.msg || JSON.stringify(e)).join(", ")
          : typeof detail === "string"
            ? detail
            : `Ошибка ${res.status}`
        throw new Error(msg)
      }

      const data: AnalysisResult = await res.json()
      setResult(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Ошибка при анализе документа")
    } finally {
      setIsLoading(false)
    }
  }, [file])

  return (
    <div className="space-y-6">
      <div
        onDrop={onDrop}
        onDragOver={onDragOver}
        onDragLeave={onDragLeave}
        className={cn(
          "relative flex flex-col items-center justify-center rounded-lg border-2 border-dashed transition-all duration-200 min-h-[140px] p-6",
          "border-white/20 bg-white/5 backdrop-blur-md",
          isDragActive && "border-primary/50 bg-white/10",
          error && "border-destructive/50"
        )}
      >
        <input
          type="file"
          accept=".pdf,.docx"
          onChange={onFileSelect}
          className="absolute inset-0 cursor-pointer opacity-0"
          disabled={isLoading}
        />
        {file ? (
          <div className="flex w-full flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div className="flex items-center gap-3 min-w-0">
              <div className="flex size-10 shrink-0 items-center justify-center rounded-lg bg-white/10">
                <FileText className="size-5 text-muted-foreground" />
              </div>
              <div className="min-w-0">
                <p className="truncate text-sm font-medium">{file.name}</p>
                <p className="text-xs text-muted-foreground">
                  {(file.size / 1024).toFixed(1)} КБ
                </p>
              </div>
            </div>
            <div className="flex gap-2 shrink-0">
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={removeFile}
                disabled={isLoading}
              >
                Удалить
              </Button>
              <Button
                type="button"
                size="sm"
                onClick={analyzeFile}
                disabled={isLoading}
              >
                {isLoading ? (
                  <>
                    <Loader2 className="size-4 animate-spin" />
                    Анализ...
                  </>
                ) : (
                  "Анализировать"
                )}
              </Button>
            </div>
          </div>
        ) : (
          <>
            <Upload className="size-10 text-muted-foreground mb-2" />
            <p className="text-sm text-muted-foreground text-center">
              Перетащите PDF или Word документ сюда
            </p>
            <p className="text-xs text-muted-foreground/80 mt-1">
              или нажмите для выбора (макс. 10 МБ)
            </p>
          </>
        )}
        {error && (
          <p className="mt-2 text-xs text-destructive">{error}</p>
        )}
      </div>

      {isLoading && (
        <div className="flex flex-col items-center justify-center gap-3 rounded-lg border border-white/10 bg-white/5 p-8 backdrop-blur-md">
          <Loader2 className="size-10 animate-spin text-muted-foreground" />
          <p className="text-sm text-muted-foreground">
            AI анализирует документ...
          </p>
          <p className="text-xs text-muted-foreground/80">
            Это может занять 10–30 секунд
          </p>
        </div>
      )}

      {result && !isLoading && (
        <div className="rounded-lg border border-white/10 bg-white/5 p-6 backdrop-blur-md">
          <AnalysisResultsCard result={result} />
        </div>
      )}
    </div>
  )
}
