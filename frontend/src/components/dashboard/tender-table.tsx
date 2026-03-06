"use client"

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import type { Tender } from "@/data/mock-tenders"

interface TenderTableProps {
  tenders: Tender[]
}

export function TenderTable({ tenders }: TenderTableProps) {
  return (
    <div className="rounded-lg border border-white/10 bg-white/5 backdrop-blur-md">
      <Table>
        <TableHeader>
          <TableRow className="border-white/10 hover:bg-transparent">
            <TableHead className="text-muted-foreground">Название</TableHead>
            <TableHead className="text-muted-foreground">Тип ФЗ</TableHead>
            <TableHead className="text-muted-foreground">Цена</TableHead>
            <TableHead className="text-muted-foreground">Регион</TableHead>
            <TableHead className="text-muted-foreground">Срок</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {tenders.map((tender) => (
            <TableRow
              key={tender.id}
              className="border-white/10 hover:bg-white/5 transition-colors"
            >
              <TableCell className="font-medium max-w-xs truncate">
                {tender.title}
              </TableCell>
              <TableCell>
                <Badge
                  variant="outline"
                  className={
                    tender.fzType === "44-ФЗ"
                      ? "border-blue-500/50 text-blue-400"
                      : "border-amber-500/50 text-amber-400"
                  }
                >
                  {tender.fzType}
                </Badge>
              </TableCell>
              <TableCell className="text-muted-foreground">
                {tender.price}
              </TableCell>
              <TableCell className="text-muted-foreground">
                {tender.region}
              </TableCell>
              <TableCell className="text-muted-foreground">
                {tender.deadline}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  )
}
