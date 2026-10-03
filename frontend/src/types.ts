export interface ExtractedAttributes {
  category?: string | null;
  brand?: string | null;
  model_name?: string | null;
  specs?: Record<string, any>;
  color?: string | null;
}

export interface ParsedSearchRequest {
  raw_query: string;
  detected_language: string;
  translated_query: string;
  clean_search_phrase: string;
  attributes: ExtractedAttributes;
  budget_min?: number | null;
  budget_max?: number | null;
  deadline_days?: number | null;
  pincode?: string | null;
  sort_by: string;
  clarifications_needed: string[];
}

export interface ProductOut {
  id: string;
  platform: string;
  platform_product_id: string;
  title: string;
  category: string;
  description?: string | null;
  brand?: string | null;
  seller?: string | null;
  product_url: string;
  image_urls: string[];
  price: number;
  mrp?: number | null;
  discount_percent: number;
  currency: string;
  specs: Record<string, any>;
  in_stock: boolean;
  rating: number;
  rating_count: number;
  estimated_delivery_days?: number | null;
  delivery_status: string;
  match_score: number;
  is_best_deal: boolean;
  price_difference_vs_highest?: number | null;
  why_matched: string;
}

export interface PlatformDealComparison {
  product_group: string;
  lowest_platform: string;
  lowest_price: number;
  highest_price: number;
  max_savings: number;
  total_sellers_found: number;
}

export interface SearchResponse {
  parsed_query: ParsedSearchRequest;
  total_found: number;
  deal_comparison?: PlatformDealComparison | null;
  results: ProductOut[];
}
