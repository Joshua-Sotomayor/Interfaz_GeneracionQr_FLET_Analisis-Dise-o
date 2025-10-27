import { QRCodeSVG } from "qrcode.react";
import { Card } from "./ui/card";
import { Download } from "lucide-react";
import { Button } from "./ui/button";

interface QRData {
  operatorName: string;
  operatorCode: string;
  productType: string;
  quantity: string;
  supplier: string;
  date: string;
}

interface QRDisplayProps {
  data: QRData;
}

export function QRDisplay({ data }: QRDisplayProps) {
  // Generate QR content WITHOUT operator info
  const qrContent = JSON.stringify({
    producto: data.productType,
    cantidad: data.quantity,
    proveedor: data.supplier,
    fecha: data.date,
  });

  const handleDownload = () => {
    const svg = document.getElementById("qr-code");
    if (!svg) return;

    const svgData = new XMLSerializer().serializeToString(svg);
    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");
    const img = new Image();

    img.onload = () => {
      canvas.width = img.width;
      canvas.height = img.height;
      ctx?.drawImage(img, 0, 0);
      const pngFile = canvas.toDataURL("image/png");

      const downloadLink = document.createElement("a");
      downloadLink.download = `QR-${data.productType}-${Date.now()}.png`;
      downloadLink.href = pngFile;
      downloadLink.click();
    };

    img.src = "data:image/svg+xml;base64," + btoa(svgData);
  };

  return (
    <Card className="p-6 shadow-lg rounded-2xl max-w-lg w-full">
      <div className="space-y-6">
        <div>
          <h3 className="mb-4 text-[#22543D]">Información del Lote</h3>
          <div className="space-y-2 bg-accent/50 p-4 rounded-lg">
            <div className="flex justify-between">
              <span className="text-muted-foreground">Operador:</span>
              <span>{data.operatorName}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Código operador:</span>
              <span>{data.operatorCode}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Producto:</span>
              <span>{data.productType}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Cantidad:</span>
              <span>{data.quantity}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Proveedor:</span>
              <span>{data.supplier}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Fecha:</span>
              <span>{data.date}</span>
            </div>
          </div>
        </div>

        <div className="flex flex-col items-center space-y-4">
          <div className="bg-white p-4 rounded-lg border-2 border-[#38A169]">
            <QRCodeSVG
              id="qr-code"
              value={qrContent}
              size={200}
              level="H"
              includeMargin={true}
            />
          </div>
          
          <Button
            onClick={handleDownload}
            variant="outline"
            className="w-full"
          >
            <Download className="mr-2 h-4 w-4" />
            Descargar código QR
          </Button>
          
          <p className="text-sm text-muted-foreground text-center">
            El código QR contiene: Producto, Cantidad, Proveedor y Fecha
          </p>
        </div>
      </div>
    </Card>
  );
}
