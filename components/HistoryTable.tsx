import { Card } from "./ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "./ui/table";
import { ScrollArea } from "./ui/scroll-area";

interface HistoryRecord {
  id: string;
  operatorName: string;
  productType: string;
  quantity: string;
  supplier: string;
  date: string;
}

interface HistoryTableProps {
  records: HistoryRecord[];
}

export function HistoryTable({ records }: HistoryTableProps) {
  if (records.length === 0) {
    return null;
  }

  return (
    <Card className="p-6 shadow-lg rounded-2xl max-w-6xl w-full">
      <h3 className="mb-4 text-[#22543D]">Historial de Registros</h3>
      <ScrollArea className="h-[300px]">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Operador</TableHead>
              <TableHead>Producto</TableHead>
              <TableHead>Cantidad</TableHead>
              <TableHead>Proveedor</TableHead>
              <TableHead>Fecha</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {records.map((record) => (
              <TableRow key={record.id}>
                <TableCell>{record.operatorName}</TableCell>
                <TableCell>{record.productType}</TableCell>
                <TableCell>{record.quantity}</TableCell>
                <TableCell>{record.supplier}</TableCell>
                <TableCell>{record.date}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </ScrollArea>
    </Card>
  );
}
