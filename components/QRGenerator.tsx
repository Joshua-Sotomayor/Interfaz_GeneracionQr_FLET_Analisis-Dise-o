import { useState, useEffect } from "react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Card } from "./ui/card";

interface QRFormData {
  operatorName: string;
  operatorCode: string;
  productType: string;
  quantity: string;
  supplier: string;
  date: string;
}

interface QRGeneratorProps {
  onGenerate: (data: QRFormData) => void;
  onReset: () => void;
  isGenerating: boolean;
}

export function QRGenerator({ onGenerate, onReset, isGenerating }: QRGeneratorProps) {
  const [formData, setFormData] = useState<QRFormData>({
    operatorName: "",
    operatorCode: "",
    productType: "",
    quantity: "",
    supplier: "",
    date: "",
  });

  const [suggestions, setSuggestions] = useState({
    products: [] as string[],
    suppliers: [] as string[],
  });

  const [showProductSuggestions, setShowProductSuggestions] = useState(false);
  const [showSupplierSuggestions, setShowSupplierSuggestions] = useState(false);

  useEffect(() => {
    // Load suggestions from localStorage
    const storedProducts = JSON.parse(localStorage.getItem("products") || "[]");
    const storedSuppliers = JSON.parse(localStorage.getItem("suppliers") || "[]");
    setSuggestions({
      products: storedProducts,
      suppliers: storedSuppliers,
    });
  }, []);

  const handleChange = (field: keyof QRFormData, value: string) => {
    setFormData({ ...formData, [field]: value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validate required fields
    if (!formData.operatorName || !formData.operatorCode || !formData.productType || !formData.quantity || !formData.supplier) {
      alert("Por favor, complete todos los campos requeridos");
      return;
    }

    // If no date provided, use current date
    const finalData = {
      ...formData,
      date: formData.date || new Date().toLocaleString("es-ES"),
    };

    // Save to suggestions
    const updatedProducts = [...new Set([...suggestions.products, formData.productType])];
    const updatedSuppliers = [...new Set([...suggestions.suppliers, formData.supplier])];
    localStorage.setItem("products", JSON.stringify(updatedProducts));
    localStorage.setItem("suppliers", JSON.stringify(updatedSuppliers));

    onGenerate(finalData);
  };

  const handleNewCode = () => {
    setFormData({
      operatorName: "",
      operatorCode: "",
      productType: "",
      quantity: "",
      supplier: "",
      date: "",
    });
    onReset();
  };

  const filteredProductSuggestions = suggestions.products.filter((p) =>
    p.toLowerCase().includes(formData.productType.toLowerCase())
  );

  const filteredSupplierSuggestions = suggestions.suppliers.filter((s) =>
    s.toLowerCase().includes(formData.supplier.toLowerCase())
  );

  return (
    <Card className="p-6 shadow-lg rounded-2xl max-w-lg w-full">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="operatorName">Nombre del operador *</Label>
          <Input
            id="operatorName"
            type="text"
            value={formData.operatorName}
            onChange={(e) => handleChange("operatorName", e.target.value)}
            placeholder="Ej: Juan Pérez"
            required
            className="bg-input-background"
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="operatorCode">Código del operador *</Label>
          <Input
            id="operatorCode"
            type="text"
            value={formData.operatorCode}
            onChange={(e) => handleChange("operatorCode", e.target.value)}
            placeholder="Ej: OP-001"
            required
            className="bg-input-background"
          />
        </div>

        <div className="space-y-2 relative">
          <Label htmlFor="productType">Tipo de producto *</Label>
          <Input
            id="productType"
            type="text"
            value={formData.productType}
            onChange={(e) => handleChange("productType", e.target.value)}
            onFocus={() => setShowProductSuggestions(true)}
            onBlur={() => setTimeout(() => setShowProductSuggestions(false), 200)}
            placeholder="Ej: Cúrcuma"
            required
            className="bg-input-background"
          />
          {showProductSuggestions && filteredProductSuggestions.length > 0 && (
            <div className="absolute z-10 w-full bg-white border border-border rounded-md shadow-lg mt-1 max-h-40 overflow-y-auto">
              {filteredProductSuggestions.map((product, index) => (
                <div
                  key={index}
                  className="px-3 py-2 hover:bg-accent cursor-pointer"
                  onMouseDown={() => handleChange("productType", product)}
                >
                  {product}
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="space-y-2">
          <Label htmlFor="quantity">Cantidad de producto *</Label>
          <Input
            id="quantity"
            type="number"
            value={formData.quantity}
            onChange={(e) => handleChange("quantity", e.target.value)}
            placeholder="Ej: 100"
            required
            min="0"
            step="0.01"
            className="bg-input-background"
          />
        </div>

        <div className="space-y-2 relative">
          <Label htmlFor="supplier">Proveedor *</Label>
          <Input
            id="supplier"
            type="text"
            value={formData.supplier}
            onChange={(e) => handleChange("supplier", e.target.value)}
            onFocus={() => setShowSupplierSuggestions(true)}
            onBlur={() => setTimeout(() => setShowSupplierSuggestions(false), 200)}
            placeholder="Ej: Agro Sur S.A."
            required
            className="bg-input-background"
          />
          {showSupplierSuggestions && filteredSupplierSuggestions.length > 0 && (
            <div className="absolute z-10 w-full bg-white border border-border rounded-md shadow-lg mt-1 max-h-40 overflow-y-auto">
              {filteredSupplierSuggestions.map((supplier, index) => (
                <div
                  key={index}
                  className="px-3 py-2 hover:bg-accent cursor-pointer"
                  onMouseDown={() => handleChange("supplier", supplier)}
                >
                  {supplier}
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="space-y-2">
          <Label htmlFor="date">Fecha de producción</Label>
          <Input
            id="date"
            type="datetime-local"
            value={formData.date}
            onChange={(e) => handleChange("date", e.target.value)}
            className="bg-input-background"
          />
          <p className="text-sm text-muted-foreground">
            Si no se ingresa, se usará la fecha y hora actual
          </p>
        </div>

        <div className="flex gap-3 pt-2">
          <Button
            type="submit"
            className="flex-1 bg-[#38A169] hover:bg-[#2F855A]"
          >
            {isGenerating ? "Generar nuevo código QR" : "Generar código QR"}
          </Button>
          
          {isGenerating && (
            <Button
              type="button"
              variant="outline"
              onClick={handleNewCode}
              className="flex-1"
            >
              Nuevo código
            </Button>
          )}
        </div>
      </form>
    </Card>
  );
}
