export interface SystemsSummary {
  store_id: number;
  period_type: string;
  found: boolean;
  primary_units: number;
  asp: number;
  rpu: number;
  attach_units_per_primary: number;
  total_attach_rpu: number;
  service_plans_attach_percent: number;
  eset_attach_percent: number;
  office_attach_percent: number;
  monitors_attach_percent: number;
  mice_keyboard_attach_percent: number;
  all_other_attach_percent: number;
}

export interface SystemsSummaryResponse {
  success: boolean;
  message: string;
  data: SystemsSummary;
}

export interface SystemsRankingMetric {
  store_id: number;
  period_type: string;
  metric: string;
  rank: number;
  total_stores: number;
  metric_value: number;
  found: boolean;
}

export interface SystemsRankings {
  rpu: SystemsRankingMetric;
  total_attach_rpu: SystemsRankingMetric;
  asp: SystemsRankingMetric;
  primary_units: SystemsRankingMetric;
}

export interface SystemsRankingsResponse {
  success: boolean;
  message: string;
  data: {
    store_id: number;
    period_type: string;
    rankings: SystemsRankings;
  };
}

export interface SystemsAssociate {
  associate_name: string;
  primary_units: number;
  asp: number;
  rpu: number;
  total_attach_rpu: number;
  service_plans_attach_percent: number;
  eset_attach_percent: number;
  office_attach_percent: number;
  monitors_attach_percent?: number;
}

export interface TopSystemsAssociatesResponse {
  success: boolean;
  message: string;
  data: {
    store_id: number;
    period_type: string;
    limit: number;
    associates: SystemsAssociate[];
  };
}