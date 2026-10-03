import React, { useState, useEffect } from 'react';
import { Search, Mic, MicOff, Truck, Star, ExternalLink, Sparkles, TrendingDown } from 'lucide-react';
import { SearchResponse, ProductOut } from './types';

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
    <div style={{ maxWidth: '1240px', margin: '0 auto', padding: '32px 16px' }}>
      {/* Header */}
      <header style={{ marginBottom: '28px', borderBottom: '1px solid #522B5B', paddingBottom: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '14px' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <h1 style={{ fontSize: '28px', fontWeight: 800, letterSpacing: '-0.02em', color: '#FBE4D8' }}>
                EasyPezy
              </h1>
              <span style={{
                fontSize: '11px',
                fontWeight: 700,
                padding: '4px 10px',
                borderRadius: '999px',
                background: '#522B5B',
                color: '#FBE4D8',
                letterSpacing: '0.06em',
                textTransform: 'uppercase',
                border: '1px solid #854F6C'
              }}>
                Universal Deal Finder
              </span>
            </div>
            <p style={{ color: '#DFB6B2', fontSize: '14px', marginTop: '6px' }}>
              Search anything online across all platforms in any language. Find the highest discount and best price instantly.
            </p>
          </div>
          <div style={{ display: 'flex', gap: '8px' }}>
            <span style={{
              fontSize: '12px',
              padding: '6px 14px',
              borderRadius: '999px',
              background: '#2B124C',
              border: '1px solid #522B5B',
              color: '#DFB6B2'
            }}>
              Multilingual NLP • Cross-Platform Aggregation
            </span>
          </div>
        </div>
      </header>

      {/* Search Input Bar */}
      <section style={{ marginBottom: '24px' }}>
        <form onSubmit={(e) => { e.preventDefault(); executeSearch(query); }}>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            background: '#2B124C',
            border: '1px solid #854F6C',
            borderRadius: '16px',
            padding: '10px 14px',
            boxShadow: '0 8px 30px rgba(25, 0, 25, 0.6)'
          }}>
            <Search size={20} color="#DFB6B2" style={{ marginRight: '10px' }} />
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
                color: '#FBE4D8',
                fontSize: '16px'
              }}
            />
            <button
              type="button"
              onClick={handleVoiceToggle}
              title="Voice Search (Speak in any language)"
              style={{
                padding: '9px',
                borderRadius: '10px',
                background: isListening ? '#854F6C' : 'rgba(223, 182, 178, 0.12)',
                color: '#FBE4D8',
                marginRight: '10px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                border: '1px solid #522B5B'
              }}
            >
              {isListening ? <MicOff size={18} /> : <Mic size={18} />}
            </button>
            <button
              type="submit"
              disabled={loading}
              style={{
                background: '#854F6C',
                color: '#FBE4D8',
                fontWeight: 700,
                fontSize: '14px',
                padding: '10px 22px',
                borderRadius: '10px',
                border: '1px solid #DFB6B2',
                transition: 'background 0.2s'
              }}
            >
              {loading ? "Searching..." : "Compare Deals"}
            </button>
          </div>
        </form>

        {/* Preset query chips */}
        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', marginTop: '14px' }}>
          <span style={{ fontSize: '12px', color: '#DFB6B2', alignSelf: 'center' }}>Try queries:</span>
          {PRESET_QUERIES.map((q) => (
            <button
              key={q}
              onClick={() => { setQuery(q); executeSearch(q); }}
              style={{
                fontSize: '12px',
                padding: '5px 12px',
                borderRadius: '999px',
                background: '#2B124C',
                border: '1px solid #522B5B',
                color: '#FBE4D8',
                transition: 'border-color 0.15s, background 0.15s'
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
          background: 'rgba(133, 79, 108, 0.25)',
          border: '1px solid #854F6C',
          borderRadius: '10px',
          marginBottom: '20px',
          color: '#FBE4D8',
          fontSize: '14px'
        }}>
          {error}
        </div>
      )}

      {/* Best Deal Comparison Banner */}
      {response && response.deal_comparison && (
        <div style={{
          background: 'linear-gradient(135deg, #2B124C 0%, #522B5B 100%)',
          border: '1px solid #DFB6B2',
          borderRadius: '16px',
          padding: '18px 22px',
          marginBottom: '24px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: '14px',
          boxShadow: '0 6px 25px rgba(25, 0, 25, 0.4)'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
            <div style={{
              width: '44px',
              height: '44px',
              borderRadius: '10px',
              background: '#854F6C',
              border: '1px solid #DFB6B2',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#FBE4D8'
            }}>
              <TrendingDown size={22} />
            </div>
            <div>
              <span style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.06em', color: '#DFB6B2', fontWeight: 700 }}>
                Cross-Platform Price Alert
              </span>
              <h3 style={{ fontSize: '18px', fontWeight: 800, color: '#FBE4D8' }}>
                Lowest price on {response.deal_comparison.lowest_platform} at Rs. {response.deal_comparison.lowest_price.toLocaleString()}
              </h3>
              <p style={{ fontSize: '13px', color: '#DFB6B2' }}>
                Found across {response.deal_comparison.total_sellers_found} platforms. You save Rs. {response.deal_comparison.max_savings.toLocaleString()} compared to highest seller.
              </p>
            </div>
          </div>
          <div>
            <span style={{
              fontSize: '13px',
              padding: '8px 16px',
              borderRadius: '999px',
              background: '#FBE4D8',
              color: '#190019',
              fontWeight: 800,
              display: 'inline-block'
            }}>
              Save Rs. {response.deal_comparison.max_savings.toLocaleString()}
            </span>
          </div>
        </div>
      )}

      {/* Extracted Parameters Bar */}
      {response && response.parsed_query && (
        <section style={{
          background: '#2B124C',
          border: '1px solid #522B5B',
          borderRadius: '12px',
          padding: '14px 18px',
          marginBottom: '24px'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '10px', flexWrap: 'wrap', gap: '8px' }}>
            <span style={{ fontSize: '12px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.06em', color: '#DFB6B2' }}>
              Extracted Parameters
            </span>
            <div style={{ display: 'flex', gap: '14px', fontSize: '12px', color: '#DFB6B2' }}>
              <span>Language: <strong style={{ color: '#FBE4D8' }}>{response.parsed_query.detected_language.toUpperCase()}</strong></span>
              <span>Clean phrase: <strong style={{ color: '#FBE4D8' }}>"{response.parsed_query.clean_search_phrase}"</strong></span>
            </div>
          </div>

          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
            {response.parsed_query.attributes.brand && (
              <span style={badgeStyle}>
                Brand: <strong style={{ marginLeft: '4px', color: '#FBE4D8' }}>{response.parsed_query.attributes.brand}</strong>
              </span>
            )}
            {response.parsed_query.attributes.model_name && (
              <span style={badgeStyle}>
                Model: <strong style={{ marginLeft: '4px', color: '#FBE4D8' }}>{response.parsed_query.attributes.model_name}</strong>
              </span>
            )}
            {response.parsed_query.attributes.category && (
              <span style={badgeStyle}>
                Category: <strong style={{ marginLeft: '4px', color: '#FBE4D8' }}>{response.parsed_query.attributes.category}</strong>
              </span>
            )}
            {response.parsed_query.attributes.specs && Object.entries(response.parsed_query.attributes.specs).map(([k, v]) => (
              <span key={k} style={badgeStyle}>
                {k}: <strong style={{ marginLeft: '4px', color: '#FBE4D8' }}>{String(v)}</strong>
              </span>
            ))}
            {response.parsed_query.budget_max && (
              <span style={badgeStyle}>
                Max Budget: <strong style={{ marginLeft: '4px', color: '#FBE4D8' }}>Rs. {response.parsed_query.budget_max.toLocaleString()}</strong>
              </span>
            )}
            {response.parsed_query.pincode && (
              <span style={badgeStyle}>
                Pincode: <strong style={{ marginLeft: '4px', color: '#FBE4D8' }}>{response.parsed_query.pincode}</strong>
              </span>
            )}
          </div>
        </section>
      )}

      {/* Results Header */}
      {response && (
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '18px' }}>
          <h2 style={{ fontSize: '19px', fontWeight: 800, color: '#FBE4D8' }}>
            Platforms Selling This Item ({response.total_found})
          </h2>
          <span style={{ fontSize: '13px', color: '#DFB6B2' }}>
            Ranked by lowest price & maximum discount
          </span>
        </div>
      )}

      {/* Results Grid */}
      {response && response.results.length > 0 ? (
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(340px, 1fr))',
          gap: '22px'
        }}>
          {response.results.map((product) => (
            <div
              key={`${product.platform}-${product.id}`}
              style={{
                background: '#2B124C',
                border: product.is_best_deal ? '2px solid #DFB6B2' : '1px solid #522B5B',
                borderRadius: '16px',
                overflow: 'hidden',
                display: 'flex',
                flexDirection: 'column',
                position: 'relative',
                boxShadow: product.is_best_deal ? '0 8px 30px rgba(133, 79, 108, 0.35)' : 'none'
              }}
            >
              {/* Best Deal Flag Header */}
              {product.is_best_deal && (
                <div style={{
                  background: '#DFB6B2',
                  color: '#190019',
                  fontSize: '11px',
                  fontWeight: 900,
                  letterSpacing: '0.06em',
                  padding: '5px 14px',
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
              <div style={{ position: 'relative', height: '230px', background: '#190019' }}>
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
                  background: 'rgba(25, 0, 25, 0.92)',
                  backdropFilter: 'blur(4px)',
                  borderRadius: '6px',
                  fontSize: '12px',
                  fontWeight: 700,
                  color: '#FBE4D8',
                  border: '1px solid #522B5B'
                }}>
                  {product.platform}
                </span>

                {product.discount_percent > 0 && (
                  <span style={{
                    position: 'absolute',
                    top: '12px',
                    right: '12px',
                    padding: '4px 8px',
                    background: '#854F6C',
                    border: '1px solid #DFB6B2',
                    borderRadius: '6px',
                    fontSize: '11px',
                    fontWeight: 800,
                    color: '#FBE4D8'
                  }}>
                    {Math.round(product.discount_percent)}% OFF
                  </span>
                )}
              </div>

              {/* Details */}
              <div style={{ padding: '18px', display: 'flex', flexDirection: 'column', flex: 1 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: '8px' }}>
                  <span style={{ fontSize: '12px', color: '#DFB6B2', fontWeight: 600 }}>
                    Seller: {product.seller || product.brand}
                  </span>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <Star size={13} fill="#DFB6B2" color="#DFB6B2" />
                    <span style={{ fontSize: '12px', fontWeight: 700, color: '#FBE4D8' }}>{product.rating}</span>
                    <span style={{ fontSize: '11px', color: '#DFB6B2' }}>({product.rating_count})</span>
                  </div>
                </div>

                <h3 style={{
                  fontSize: '15px',
                  fontWeight: 600,
                  marginBottom: '10px',
                  lineHeight: '1.4',
                  color: '#FBE4D8',
                  display: '-webkit-box',
                  WebkitLineClamp: 2,
                  WebkitBoxOrient: 'vertical',
                  overflow: 'hidden'
                }}>
                  {product.title}
                </h3>

                {/* Price Display */}
                <div style={{ display: 'flex', alignItems: 'baseline', gap: '8px', marginBottom: '12px' }}>
                  <span style={{ fontSize: '20px', fontWeight: 800, color: '#FBE4D8' }}>
                    Rs. {product.price.toLocaleString()}
                  </span>
                  {product.mrp && product.mrp > product.price && (
                    <span style={{ fontSize: '13px', color: '#DFB6B2', textDecoration: 'line-through' }}>
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
                          padding: '3px 8px',
                          background: '#522B5B',
                          borderRadius: '6px',
                          color: '#FBE4D8',
                          border: '1px solid #854F6C'
                        }}
                      >
                        {key}: <strong>{String(val)}</strong>
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
                  background: 'rgba(25, 0, 25, 0.4)',
                  border: '1px solid #522B5B',
                  borderRadius: '8px',
                  fontSize: '12px',
                  marginBottom: '12px',
                  color: '#DFB6B2'
                }}>
                  <Truck size={14} color="#DFB6B2" />
                  <span>
                    Delivery: <strong style={{ color: '#FBE4D8' }}>{product.estimated_delivery_days} days</strong> ({product.delivery_status})
                  </span>
                </div>

                {/* Why This Matched Box */}
                <div style={{
                  background: product.is_best_deal ? 'rgba(223, 182, 178, 0.12)' : 'rgba(82, 43, 91, 0.35)',
                  border: product.is_best_deal ? '1px solid #DFB6B2' : '1px solid #522B5B',
                  borderRadius: '10px',
                  padding: '10px 12px',
                  fontSize: '12px',
                  color: '#FBE4D8',
                  marginBottom: '16px',
                  flex: 1
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '4px', marginBottom: '4px', fontWeight: 700, color: '#DFB6B2' }}>
                    <Sparkles size={12} />
                    <span>Price & Match Breakdown</span>
                  </div>
                  <p style={{ lineHeight: '1.4', color: '#FBE4D8' }}>{product.why_matched}</p>
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
                    padding: '11px',
                    borderRadius: '10px',
                    background: product.is_best_deal ? '#DFB6B2' : '#522B5B',
                    border: '1px solid #854F6C',
                    color: product.is_best_deal ? '#190019' : '#FBE4D8',
                    fontSize: '13px',
                    fontWeight: 800,
                    textAlign: 'center',
                    transition: 'opacity 0.15s'
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
          background: '#2B124C',
          borderRadius: '16px',
          border: '1px solid #522B5B'
        }}>
          <p style={{ color: '#DFB6B2', fontSize: '15px' }}>
            No platforms found for this item with the current filters.
          </p>
        </div>
      ) : null}
    </div>
  );
}

const badgeStyle: React.CSSProperties = {
  fontSize: '12px',
  padding: '4px 10px',
  borderRadius: '999px',
  background: '#522B5B',
  border: '1px solid #854F6C',
  color: '#DFB6B2'
};
