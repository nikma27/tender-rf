import { TenderTable } from "@/components/dashboard/tender-table";
import { DocumentDropzone } from "@/components/dashboard/document-dropzone";
import { mockTenders } from "@/data/mock-tenders";

export default function DashboardPage() {
  return (
    <div className="flex flex-col gap-8 p-8">
      <header>
        <h1 className="text-2xl font-semibold tracking-tight">
          Дашборд
        </h1>
        <p className="mt-1 text-muted-foreground">
          Обзор тендеров и AI-анализ документации
        </p>
      </header>

      <section className="space-y-4">
        <h2 className="text-lg font-medium">Тендеры</h2>
        <div className="p-4">
          <TenderTable tenders={mockTenders} />
        </div>
      </section>

      <section className="space-y-4">
        <h2 className="text-lg font-medium">AI-анализ документации</h2>
        <p className="text-sm text-muted-foreground">
          Загрузите PDF или Word документ для выявления скрытых рисков
        </p>
        <DocumentDropzone />
      </section>
    </div>
  );
}
