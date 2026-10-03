import React, { useState, useEffect } from 'react';
import { Search, Mic, MicOff, Truck, Star, ExternalLink, Sparkles, TrendingDown, CheckCircle2, ShieldCheck } from 'lucide-react';
import { SearchResponse, ProductOut, ParsedSearchRequest } from './types';

const API_BASE = "http://localhost:8000/api/v1";

const PRESET_QUERIES = [
  "iPhone 18 1TB",
  "mujhe sabse sasta iPhone 18 1TB chahiye",
  "Sony WH-1000XM5",
  "purple saree with golden border under 1500",
  "Nike Air Jordan 1"
];

export default function App() {
  const [query, setQuery] = useState("iPhone 18 1TB");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [response, setResponse] = useState<SearchResponse | null>(null);
  const [isListening, setIsListening] = useState(false);

  const executeSearch = async (searchQuery: string) => {
    if (!searchQuery.trim()) return;
    setLoading(true);
    setError(null);

    try {
      const res = await fetch(`${API_BASE}/search`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: searchQuery }),
      });

      if (!res.ok) {
        throw new Error(`Search request failed with status ${res.status}`);
      }

      const data: SearchResponse = await res.json();
      setResponse(data);
    } catch (err: any) {
      setError(err.message || "Failed to execute search. Make sure backend is running on port 8000.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    executeSearch(query);
  }, []);

  const handleVoiceToggle = () => {
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Speech recognition is not supported in this browser. Please use Chrome or Edge.");
      return;
    }

    if (isListening) {
      setIsListening(false);
      return;
    }

    try {
      const recognition = new SpeechRecognition();
      recognition.lang = 'en-IN';
      recognition.interimResults = false;

      recognition.onstart = () => setIsListening(true);
      recognition.onend = () => setIsListening(false);
      recognition.onerror = () => setIsListening(false);

      recognition.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        setQuery(transcript);
        executeSearch(transcript);
      };

      recognition.start();
    } catch {
      setIsListening(false);
    }
  };

  return (
    <div style={{ maxWidth: '1240px', margin: '0 auto', padding: '24px 16px' }}>
      {/* Header */}
      <header style={{ marginBottom: '24px', borderBottom: '1px solid var(--border-subtle)', paddingBottom: '20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '12px' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <h1 style={{ fontSize: '26px', fontWeight: 800, letterSpacing: '-0.02em', color: '#fff' }}>
                EasyPezy
              </h1>
              <span style={{
                fontSize: '11px',
                fontWeight: 700,
                padding: '3px 8px',
                borderRadius: '6px',
                background: '#1d4ed8',
                color: '#fff',
                letterSpacing: '0.05em',
                textTransform: 'uppercase'
              }}>
                Universal Deal Finder
              </span>
            </div>
            <p style={{ color: 'var(--text-muted)', fontSize: '14px', marginTop: '4px' }}>
              Search anything online across all platforms in any language. Find the highest discount and best price instantly.
            </p>
          </div>
          <div style={{ display: 'flex', gap: '8px' }}>
            <span style={{
              fontSize: '12px',
              padding: '6px 12px',
              borderRadius: '8px',
              background: '#1e293b',
              border: '1px solid var(--border-subtle)',
              color: '#94a3b8'
            }}>
              Multilingual NLP • Cross-Platform Aggregation
            </span>
          </div>
        </div>
      </header>

      {/* Search Input Bar */}
      <section style={{ marginBottom: '20px' }}>
        <form onSubmit={(e) => { e.preventDefault(); executeSearch(query); }}>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            background: 'var(--bg-secondary)',
            border: '1px solid var(--border-subtle)',
            borderRadius: '12px',
            padding: '8px 12px',
            boxShadow: '0 4px 20px rgba(0,0,0,0.3)'
          }}>
            <Search size={20} color="var(--text-muted)" style={{ marginRight: '10px' }} />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search gadgets, clothing, appliances in any language (e.g. iPhone 18 1TB, sabse sasta iPhone)"
              style={{
                flex: 1,
                background: 'transparent',
                border: 'none',
                outline: 'none',
                color: '#fff',
                fontSize: '16px'
              }}
            />
            <button
              type="button"
              onClick={handleVoiceToggle}
              title="Voice Search (Speak in any language)"
              style={{
                padding: '8px',
                borderRadius: '8px',
                background: isListening ? '#dc2626' : 'rgba(255,255,255,0.06)',
                color: '#fff',
                marginRight: '8px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}
            >
              {isListening ? <MicOff size={18} /> : <Mic size={18} />}
            </button>
            <button
              type="submit"
              disabled={loading}
              style={{
                background: 'var(--accent-blue)',
                color: '#fff',
                fontWeight: 600,
                fontSize: '14px',
                padding: '10px 20px',
                borderRadius: '8px'
              }}
            >
              {loading ? "Searching..." : "Compare Deals"}
            </button>
          </div>
        </form>

        {/* Preset query chips */}
        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', marginTop: '12px' }}>
          <span style={{ fontSize: '12px', color: 'var(--text-muted)', alignSelf: 'center' }}>Try queries:</span>
          {PRESET_QUERIES.map((q) => (
            <button
              key={q}
              onClick={() => { setQuery(q); executeSearch(q); }}
              style={{
                fontSize: '12px',
                padding: '5px 12px',
                borderRadius: '6px',
                background: 'rgba(255,255,255,0.04)',
                border: '1px solid var(--border-subtle)',
                color: 'var(--text-main)',
                transition: 'background 0.15s'
              }}
            >
              {q}
            </button>
          ))}
        </div>
      </section>

      {/* Error Banner */}
      {error && (
        <div style={{
          padding: '12px 16px',
          background: 'rgba(239, 68, 68, 0.15)',
          border: '1px solid #ef4444',
          borderRadius: '8px',
          marginBottom: '20px',
          color: '#fca5a5',
          fontSize: '14px'
        }}>
          {error}
        </div>
      )}

      {/* Best Deal Comparison Banner */}
      {response && response.deal_comparison && (
        <div style={{
          background: 'linear-gradient(90deg, #1e3a8a 0%, #172554 100%)',
          border: '1px solid #3b82f6',
          borderRadius: '12px',
          padding: '16px 20px',
          marginBottom: '20px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: '12px'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{
              width: '40px',
              height: '40px',
              borderRadius: '8px',
              background: '#2563eb',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#fff'
            }}>
              <TrendingDown size={22} />
            </div>
            <div>
              <span style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.05em', color: '#93c5fd', fontWeight: 700 }}>
                Cross-Platform Price Alert
              </span>
              <h3 style={{ fontSize: '17px', fontWeight: 700, color: '#fff' }}>
                Lowest price on {response.deal_comparison.lowest_platform} at Rs. {response.deal_comparison.lowest_price.toLocaleString()}
              </h3>
              <p style={{ fontSize: '13px', color: '#bfdbfe' }}>
                Found across {response.deal_comparison.total_sellers_found} platforms. You save Rs. {response.deal_comparison.max_savings.toLocaleString()} compared to highest seller.
              </p>
            </div>
          </div>
          <div style={{ textAlign: 'right' }}>
            <span style={{
              fontSize: '12px',
              padding: '6px 12px',
              borderRadius: '6px',
              background: '#10b981',
              color: '#fff',
              fontWeight: 700
            }}>
              Save Rs. {response.deal_comparison.max_savings.toLocaleString()}
            </span>
          </div>
        </div>
      )}

      {/* Extracted Parameters Bar */}
      {response && response.parsed_query && (
        <section style={{
          background: 'var(--bg-secondary)',
          border: '1px solid var(--border-subtle)',
          borderRadius: '10px',
          padding: '14px 16px',
          marginBottom: '24px'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '10px', flexWrap: 'wrap', gap: '8px' }}>
            <span style={{ fontSize: '12px', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-muted)' }}>
              Extracted Parameters
            </span>
            <div style={{ display: 'flex', gap: '12px', fontSize: '12px', color: 'var(--text-muted)' }}>
              <span>Language: <strong style={{ color: '#fff' }}>{response.parsed_query.detected_language.toUpperCase()}</strong></span>
              <span>Clean search: <strong style={{ color: '#fff' }}>"{response.parsed_query.clean_search_phrase}"</strong></span>
            </div>
          </div>

          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
            {response.parsed_query.attributes.brand && (
              <span style={badgeStyle}>
                Brand: <strong style={{ marginLeft: '4px', color: '#fff' }}>{response.parsed_query.attributes.brand}</strong>
              </span>
            )}
            {response.parsed_query.attributes.model_name && (
              <span style={badgeStyle}>
                Model: <strong style={{ marginLeft: '4px', color: '#fff' }}>{response.parsed_query.attributes.model_name}</strong>
              </span>
            )}
            {response.parsed_query.attributes.category && (
              <span style={badgeStyle}>
                Category: <strong style={{ marginLeft: '4px', color: '#fff' }}>{response.parsed_query.attributes.category}</strong>
              </span>
            )}
            {response.parsed_query.attributes.specs && Object.entries(response.parsed_query.attributes.specs).map(([k, v]) => (
              <span key={k} style={badgeStyle}>
                {k}: <strong style={{ marginLeft: '4px', color: '#fff' }}>{String(v)}</strong>
              </span>
            ))}
            {response.parsed_query.budget_max && (
              <span style={badgeStyle}>
                Max Budget: <strong style={{ marginLeft: '4px', color: '#fff' }}>Rs. {response.parsed_query.budget_max.toLocaleString()}</strong>
              </span>
            )}
            {response.parsed_query.pincode && (
              <span style={badgeStyle}>
                Pincode: <strong style={{ marginLeft: '4px', color: '#fff' }}>{response.parsed_query.pincode}</strong>
              </span>
            )}
          </div>
        </section>
      )}

      {/* Results Header */}
      {response && (
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <h2 style={{ fontSize: '18px', fontWeight: 700 }}>
            Platforms Selling This Item ({response.total_found})
          </h2>
          <span style={{ fontSize: '13px', color: 'var(--text-muted)' }}>
            Ranked by lowest price & maximum discount
          </span>
        </div>
      )}

      {/* Results Grid */}
      {response && response.results.length > 0 ? (
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(340px, 1fr))',
          gap: '20px'
        }}>
          {response.results.map((product) => (
            <div
              key={`${product.platform}-${product.id}`}
              style={{
                background: 'var(--bg-card)',
                border: product.is_best_deal ? '2px solid #10b981' : '1px solid var(--border-subtle)',
                borderRadius: '12px',
                overflow: 'hidden',
                display: 'flex',
                flexDirection: 'column',
                position: 'relative'
              }}
            >
              {/* Best Deal Flag Header */}
              {product.is_best_deal && (
                <div style={{
                  background: '#10b981',
                  color: '#fff',
                  fontSize: '12px',
                  fontWeight: 800,
                  letterSpacing: '0.04em',
                  padding: '4px 12px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between'
                }}>
                  <span>BEST DEAL • LOWEST PRICE</span>
                  {product.price_difference_vs_highest ? (
                    <span>Save Rs. {product.price_difference_vs_highest.toLocaleString()}</span>
                  ) : null}
                </div>
              )}

              {/* Product Image */}
              <div style={{ position: 'relative', height: '230px', background: '#0f172a' }}>
                <img
                  src={product.image_urls[0] || 'https://images.unsplash.com/photo-1695048133142-1a20484d2569?auto=format&fit=crop&w=800&q=80'}
                  alt={product.title}
                  style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                />
                {/* Platform Tag */}
                <span style={{
                  position: 'absolute',
                  top: '12px',
                  left: '12px',
                  padding: '4px 10px',
                  background: 'rgba(15, 23, 42, 0.9)',
                  backdropFilter: 'blur(4px)',
                  borderRadius: '6px',
                  fontSize: '12px',
                  fontWeight: 700,
                  color: '#fff',
                  border: '1px solid rgba(255,255,255,0.15)'
                }}>
                  {product.platform}
                </span>

                {product.discount_percent > 0 && (
                  <span style={{
                    position: 'absolute',
                    top: '12px',
                    right: '12px',
                    padding: '4px 8px',
                    background: '#e11d48',
                    borderRadius: '6px',
                    fontSize: '11px',
                    fontWeight: 800,
                    color: '#fff'
                  }}>
                    {Math.round(product.discount_percent)}% OFF
                  </span>
                )}
              </div>

              {/* Details */}
              <div style={{ padding: '16px', display: 'flex', flexDirection: 'column', flex: 1 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: '8px' }}>
                  <span style={{ fontSize: '12px', color: 'var(--text-muted)', fontWeight: 600 }}>
                    Seller: {product.seller || product.brand}
                  </span>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <Star size={13} fill="#f59e0b" color="#f59e0b" />
                    <span style={{ fontSize: '12px', fontWeight: 600 }}>{product.rating}</span>
                    <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>({product.rating_count})</span>
                  </div>
                </div>

                <h3 style={{
                  fontSize: '15px',
                  fontWeight: 600,
                  marginBottom: '10px',
                  lineHeight: '1.4',
                  display: '-webkit-box',
                  WebkitLineClamp: 2,
                  WebkitBoxOrient: 'vertical',
                  overflow: 'hidden'
                }}>
                  {product.title}
                </h3>

                {/* Price Display */}
                <div style={{ display: 'flex', alignItems: 'baseline', gap: '8px', marginBottom: '12px' }}>
                  <span style={{ fontSize: '20px', fontWeight: 800, color: '#fff' }}>
                    Rs. {product.price.toLocaleString()}
                  </span>
                  {product.mrp && product.mrp > product.price && (
                    <span style={{ fontSize: '13px', color: 'var(--text-muted)', textDecoration: 'line-through' }}>
                      Rs. {product.mrp.toLocaleString()}
                    </span>
                  )}
                </div>

                {/* Specs Chips */}
                {product.specs && Object.keys(product.specs).length > 0 && (
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', marginBottom: '12px' }}>
                    {Object.entries(product.specs).map(([key, val]) => (
                      <span
                        key={key}
                        style={{
                          fontSize: '11px',
                          padding: '2px 6px',
                          background: 'rgba(255,255,255,0.05)',
                          borderRadius: '4px',
                          color: '#94a3b8'
                        }}
                      >
                        {key}: <strong style={{ color: '#e2e8f0' }}>{String(val)}</strong>
                      </span>
                    ))}
                  </div>
                )}

                {/* Delivery SLA */}
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  padding: '6px 10px',
                  background: 'rgba(255,255,255,0.03)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: '6px',
                  fontSize: '12px',
                  marginBottom: '12px'
                }}>
                  <Truck size={14} color="#38bdf8" />
                  <span>
                    Delivery: <strong style={{ color: '#fff' }}>{product.estimated_delivery_days} days</strong> ({product.delivery_status})
                  </span>
                </div>

                {/* Why This Matched Box */}
                <div style={{
                  background: product.is_best_deal ? 'rgba(16, 185, 129, 0.08)' : 'rgba(59, 130, 246, 0.08)',
                  border: product.is_best_deal ? '1px solid rgba(16, 185, 129, 0.3)' : '1px solid rgba(59, 130, 246, 0.25)',
                  borderRadius: '8px',
                  padding: '10px 12px',
                  fontSize: '12px',
                  color: product.is_best_deal ? '#a7f3d0' : '#bfdbfe',
                  marginBottom: '16px',
                  flex: 1
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '4px', marginBottom: '4px', fontWeight: 600, color: product.is_best_deal ? '#34d399' : '#60a5fa' }}>
                    <Sparkles size={12} />
                    <span>Price & Match Breakdown</span>
                  </div>
                  <p style={{ lineHeight: '1.4' }}>{product.why_matched}</p>
                </div>

                {/* Outbound Link to Store */}
                <a
                  href={product.product_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: '6px',
                    padding: '10px',
                    borderRadius: '8px',
                    background: product.is_best_deal ? '#10b981' : '#1e293b',
                    border: '1px solid var(--border-subtle)',
                    color: '#fff',
                    fontSize: '13px',
                    fontWeight: 700,
                    textAlign: 'center',
                    transition: 'background 0.15s'
                  }}
                >
                  <span>Buy on {product.platform}</span>
                  <ExternalLink size={14} />
                </a>
              </div>
            </div>
          ))}
        </div>
      ) : response && !loading ? (
        <div style={{
          textAlign: 'center',
          padding: '48px 16px',
          background: 'var(--bg-secondary)',
          borderRadius: '12px',
          border: '1px solid var(--border-subtle)'
        }}>
          <p style={{ color: 'var(--text-muted)', fontSize: '15px' }}>
            No platforms found for this item with the current filters.
          </p>
        </div>
      ) : null}
    </div>
  );
}

const badgeStyle: React.CSSProperties = {
  fontSize: '12px',
  padding: '4px 8px',
  borderRadius: '6px',
  background: 'rgba(255,255,255,0.06)',
  border: '1px solid var(--border-subtle)',
  color: 'var(--text-muted)'
};
