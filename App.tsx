import { useState, useEffect } from "react";
import { QRGenerator } from "./components/QRGenerator";
import { QRDisplay } from "./components/QRDisplay";
import { HistoryTable } from "./components/HistoryTable";
import { Toaster } from "./components/ui/sonner";
import { toast } from "sonner@2.0.3";
import { Package } from "lucide-react";

interface QRData {
  operatorName: string;
  operatorCode: string;
  productType: string;
  quantity: string;
  supplier: string;
  date: string;
}

interface HistoryRecord extends QRData {
  id: string;
}

export default function App() {
  const [generatedData, setGeneratedData] = useState<QRData | null>(null);
  const [history, setHistory] = useState<HistoryRecord[]>([]);

  useEffect(() => {
    // Load history from localStorage on mount
    const storedHistory = JSON.parse(localStorage.getItem("qrHistory") || "[]");
    setHistory(storedHistory);
  }, []);

  const handleGenerate = (data: QRData) => {
    setGeneratedData(data);

    // Save to history
    const newRecord: HistoryRecord = {
      ...data,
      id: Date.now().toString(),
    };

    const updatedHistory = [newRecord, ...history].slice(0, 10); // Keep last 10 records
    setHistory(updatedHistory);
    localStorage.setItem("qrHistory", JSON.stringify(updatedHistory));

    // Show success toast
    toast.success("✅ Código generado exitosamente", {
      description: `Lote de ${data.productType} registrado correctamente`,
      duration: 3000,
    });

    // Scroll to results
    setTimeout(() => {
      document.getElementById("qr-results")?.scrollIntoView({ behavior: "smooth" });
    }, 100);
  };

  const handleReset = () => {
    setGeneratedData(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-[#C6F6D5]/20">
      <Toaster position="top-center" />
      
      {/* Header */}
      <header className="bg-white shadow-sm border-b-2 border-[#38A169]">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
          <div className="flex items-center justify-center gap-3">
            <Package className="h-8 w-8 text-[#22543D]" />
            <div className="text-center">
              <h1 className="text-[#22543D]">LoteTracker</h1>
              <p className="text-sm text-muted-foreground">
                Sistema de trazabilidad por código QR
              </p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <div className="flex flex-col items-center gap-8">
          {/* Form Section */}
          <QRGenerator
            onGenerate={handleGenerate}
            onReset={handleReset}
            isGenerating={generatedData !== null}
          />

          {/* Results Section */}
          {generatedData && (
            <div id="qr-results" className="w-full flex justify-center">
              <QRDisplay data={generatedData} />
            </div>
          )}

          {/* History Section */}
          {history.length > 0 && (
            <HistoryTable records={history} />
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-16 bg-[#C6F6D5] border-t border-[#38A169]">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
          <p className="text-center text-sm text-[#22543D]">
            Prototipo de sistema de trazabilidad para PYMEs – Desarrollado con React + Tailwind
          </p>
        </div>
      </footer>
    </div>
  );
}
