import { apiClient } from "./client";
import type {
  DepartmentSalesBreakdownResponse,
  SalesSummaryResponse,
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