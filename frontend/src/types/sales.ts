export interface SalesSummary {
  store_id: number;
  period_type: string;
  sales_amount: number;
  transaction_count: number;
  average_transaction: number;
  service_plan_sales: number;
  eset_quantity: number;
  office_quantity: number;
}

export interface SalesSummaryResponse {
  success: boolean;
  message: string;
  data: SalesSummary;
}

export interface DepartmentSalesBreakdown {
  department_code: string;
  department_name: string;
  sales_amount: number;
  transaction_count: number;
  service_plan_sales: number;
  eset_quantity: number;
  office_quantity: number;
}

export interface DepartmentSalesBreakdownResponse {
  success: boolean;
  message: string;
  data: DepartmentSalesBreakdown[];
}