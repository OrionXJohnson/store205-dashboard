import { apiClient } from "./client";
import type {
  DepartmentSalesBreakdownResponse,
  SalesRankingsResponse,
  SalesSummaryResponse,
  TopSalesStoresResponse,
} from "../types/sales";

export async function fetchStoreSalesSummary(
  storeId: number,
  periodType: string
): Promise<SalesSummaryResponse> {
  const response = await apiClient.get<SalesSummaryResponse>(
    `/sales/store/${storeId}/${periodType}`
  );

  return response.data;
}

export async function fetchDepartmentSalesBreakdown(
  storeId: number,
  periodType: string
): Promise<DepartmentSalesBreakdownResponse> {
  const response = await apiClient.get<DepartmentSalesBreakdownResponse>(
    `/sales/store/${storeId}/${periodType}/departments`
  );

  return response.data;
}

export async function fetchStoreSalesRankings(
  storeId: number,
  periodType: string
): Promise<SalesRankingsResponse> {
  const response = await apiClient.get<SalesRankingsResponse>(
    `/sales/store/${storeId}/${periodType}/rankings`
  );

  return response.data;
}

export async function fetchTopSalesStores(
  periodType: string,
  limit = 10,
  orderBy = "sales_amount"
): Promise<TopSalesStoresResponse> {
  const response = await apiClient.get<TopSalesStoresResponse>(
    `/sales/top-stores/${periodType}`,
    {
      params: {
        limit,
        order_by: orderBy,
      },
    }
  );

  return response.data;
}