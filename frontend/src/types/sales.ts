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

export interface SalesRankingMetric {
  store_id: number;
  period_type: string;
  metric: string;
  rank: number;
  total_stores: number;
  metric_value: number;
  found: boolean;
}

export interface SalesRankings {
  sales_amount: SalesRankingMetric;
  transaction_count: SalesRankingMetric;
  average_transaction: SalesRankingMetric;
  no_sales_share: SalesRankingMetric;
}

export interface SalesRankingsResponse {
  success: boolean;
  message: string;
  data: {
    store_id: number;
    period_type: string;
    rankings: SalesRankings;
  };
}

export interface TopSalesStore {
  store_id: number;
  store_name: string;
  sales_amount: number;
  transaction_count: number;
  average_transaction: number;
  service_plan_sales: number;
  eset_quantity: number;
  office_quantity: number;
  no_sales_amount: number;
  no_sales_transactions: number;
  no_sales_share: number;
  no_sales_transaction_share: number;
}

export interface TopSalesStoresResponse {
  success: boolean;
  message: string;
  data: {
    period_type: string;
    order_by: string;
    limit: number;
    stores: TopSalesStore[];
  };
}