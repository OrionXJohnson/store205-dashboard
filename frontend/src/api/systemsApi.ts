import { apiClient } from "./client";

import type {
  SystemsRankingsResponse,
  SystemsSummaryResponse,
  TopSystemsAssociatesResponse,
} from "../types/systems";

export async function fetchSystemsSummary(
  storeId: number,
  periodType: string
): Promise<SystemsSummaryResponse> {
  const response = await apiClient.get<SystemsSummaryResponse>(
    `/systems/store/${storeId}/${periodType}/summary`
  );

  return response.data;
}

export async function fetchSystemsRankings(
  storeId: number,
  periodType: string
): Promise<SystemsRankingsResponse> {
  const response = await apiClient.get<SystemsRankingsResponse>(
    `/systems/store/${storeId}/${periodType}/rankings`
  );

  return response.data;
}

export async function fetchTopSystemsRpuAssociates(
  storeId: number,
  periodType: string,
  limit = 5
): Promise<TopSystemsAssociatesResponse> {
  const response = await apiClient.get<TopSystemsAssociatesResponse>(
    `/systems/store/${storeId}/${periodType}/top-rpu-associates`,
    {
      params: {
        limit,
      },
    }
  );

  return response.data;
}

export async function fetchTopSystemsAttachAssociates(
  storeId: number,
  periodType: string,
  limit = 5,
  minimumPrimaryUnits = 3
): Promise<TopSystemsAssociatesResponse> {
  const response = await apiClient.get<TopSystemsAssociatesResponse>(
    `/systems/store/${storeId}/${periodType}/top-attach-associates`,
    {
      params: {
        limit,
        minimum_primary_units: minimumPrimaryUnits,
      },
    }
  );

  return response.data;
}