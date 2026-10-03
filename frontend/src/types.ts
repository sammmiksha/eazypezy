export interface SareeQueryAttributes {
  primary_color?: string | null;
  secondary_color?: string | null;
  border_type?: string | null;
  zari_type?: string | null;
  finish?: string | null;
  fabric?: string | null;
  occasion?: string | null;
}

export interface ParsedSearchRequest {
  raw_query: string;
  detected_language: string;
  translated_query: string;
  clean_search_phrase: string;
  attributes: SareeQueryAttributes;
  budget_min?: number | null;
  budget_max?: number | null;
  deadline_days?: number | null;
  pincode?: string | null;
  clarifications_needed: string[];
}

export interface ProductOut {
  id: string;
  platform: string;
  platform_product_id: string;
  title: string;
  description?: string | null;
  brand?: string | null;
  seller?: string | null;
  product_url: string;
  image_urls: string[];
  price: number;
  mrp?: number | null;
  currency: string;
  primary_color?: string | null;
  secondary_color?: string | null;
  border_type?: string | null;
  zari_type?: string | null;
  finish?: string | null;
  fabric?: string | null;
  occasion?: string | null;
  in_stock: boolean;
  rating: number;
  rating_count: number;
  estimated_delivery_days?: number | null;
  delivery_status: string;
  match_score: number;
  why_matched: string;
}

export interface SearchResponse {
  parsed_query: ParsedSearchRequest;
  total_found: number;
  results: ProductOut[];
}
