import React, { useState, useEffect } from 'react';
import { Search, Mic, MicOff, Truck, Star, ExternalLink, Sparkles, Filter, CheckCircle2, AlertCircle } from 'lucide-react';
import { SearchResponse, ProductOut, ParsedSearchRequest } from './types';

const API_BASE = "http://localhost:8000/api/v1";

const PRESET_QUERIES = [
  "purple saree with golden border under 1500",
  "violet banarasi saree under 1500 deliver in 2 days to 560034",
  "mustard yellow georgette haldi saree under 1200",
  "red banarasi silk saree for wedding"
];

export default function App() {
  const [query, setQuery] = useState("purple saree with golden border under 1500");
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
      setError(err.message || "Failed to execute search. Make sure backend is running.");
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
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '24px 16px' }}>
      {/* Header */}
      <header style={{ marginBottom: '28px', borderBottom: '1px solid var(--border-subtle)', paddingBottom: '20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div>
            <h1 style={{ fontSize: '24px', fontWeight: 700, letterSpacing: '-0.02em', color: '#fff' }}>
              EasyPezy Saree Search
            </h1>
            <p style={{ color: 'var(--text-muted)', fontSize: '14px', marginTop: '4px' }}>
              Multilingual attribute extraction and cross-platform fulfillment ranker
            </p>
          </div>
          <div style={{ display: 'flex', gap: '8px' }}>
            <span style={{
              fontSize: '12px',
              padding: '4px 10px',
              borderRadius: '999px',
              background: '#1e293b',
              border: '1px solid var(--border-subtle)',
              color: '#38bdf8'
            }}>
              Phase 1 Core Slice
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
            background: 'var(--bg-secondary)',
            border: '1px solid var(--border-subtle)',
            borderRadius: '12px',
            padding: '8px 12px',
            boxShadow: '0 4px 20px rgba(0,0,0,0.3)',
            transition: 'border-color 0.2s'
          }}>
            <Search size={20} color="var(--text-muted)" style={{ marginRight: '10px' }} />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Speak or type (e.g. purple saree with golden border under 1500)"
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
              title="Voice Search"
              style={{
                padding: '8px',
                borderRadius: '8px',
                background: isListening ? '#dc2626' : 'rgba(255,255,255,0.05)',
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
                padding: '10px 18px',
                borderRadius: '8px'
              }}
            >
              {loading ? "Searching..." : "Search"}
            </button>
          </div>
        </form>

        {/* Preset query chips */}
        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', marginTop: '12px' }}>
          <span style={{ fontSize: '12px', color: 'var(--text-muted)', alignSelf: 'center' }}>Examples:</span>
          {PRESET_QUERIES.map((q) => (
            <button
              key={q}
              onClick={() => { setQuery(q); executeSearch(q); }}
              style={{
                fontSize: '12px',
                padding: '4px 10px',
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

      {/* Error State */}
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

      {/* Parsed Intent Summary */}
      {response && response.parsed_query && (
        <section style={{
          background: 'var(--bg-secondary)',
          border: '1px solid var(--border-subtle)',
          borderRadius: '10px',
          padding: '16px',
          marginBottom: '24px'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
            <span style={{ fontSize: '13px', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-muted)' }}>
              Extracted Parameters
            </span>
            <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
              Vector phrase: <strong style={{ color: '#fff' }}>"{response.parsed_query.clean_search_phrase}"</strong>
            </span>
          </div>

          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
            {response.parsed_query.attributes.primary_color && (
              <span style={badgeStyle}>
                Color: <strong style={{ marginLeft: '4px', color: '#fff' }}>{response.parsed_query.attributes.primary_color}</strong>
              </span>
            )}
            {response.parsed_query.attributes.zari_type && (
              <span style={badgeStyle}>
                Zari: <strong style={{ marginLeft: '4px', color: '#fff' }}>{response.parsed_query.attributes.zari_type}</strong>
              </span>
            )}
            {response.parsed_query.attributes.border_type && (
              <span style={badgeStyle}>
                Border: <strong style={{ marginLeft: '4px', color: '#fff' }}>{response.parsed_query.attributes.border_type}</strong>
              </span>
            )}
            {response.parsed_query.attributes.fabric && (
              <span style={badgeStyle}>
                Fabric: <strong style={{ marginLeft: '4px', color: '#fff' }}>{response.parsed_query.attributes.fabric}</strong>
              </span>
            )}
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
            {response.parsed_query.deadline_days && (
              <span style={badgeStyle}>
                Max SLA: <strong style={{ marginLeft: '4px', color: '#fff' }}>Within {response.parsed_query.deadline_days} days</strong>
              </span>
            )}
          </div>

          {/* Clarification Chips */}
          {response.parsed_query.clarifications_needed.length > 0 && (
            <div style={{ marginTop: '12px', padding: '10px', background: 'rgba(245, 158, 11, 0.1)', borderRadius: '6px', border: '1px solid rgba(245, 158, 11, 0.3)' }}>
              <span style={{ fontSize: '13px', color: '#fbbf24', fontWeight: 500 }}>
                Clarification needed: {response.parsed_query.clarifications_needed.join(", ")}
              </span>
            </div>
          )}
        </section>
      )}

      {/* Results Header */}
      {response && (
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <h2 style={{ fontSize: '18px', fontWeight: 600 }}>
            Ranked Results ({response.total_found})
          </h2>
          <span style={{ fontSize: '13px', color: 'var(--text-muted)' }}>
            Sorted by multi-factor score and delivery SLA
          </span>
        </div>
      )}

      {/* Results Grid */}
      {response && response.results.length > 0 ? (
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
          gap: '20px'
        }}>
          {response.results.map((product) => (
            <div
              key={product.id}
              style={{
                background: 'var(--bg-card)',
                border: '1px solid var(--border-subtle)',
                borderRadius: '12px',
                overflow: 'hidden',
                display: 'flex',
                flexDirection: 'column',
                transition: 'transform 0.15s, border-color 0.15s'
              }}
            >
              {/* Image & Platform Tag */}
              <div style={{ position: 'relative', height: '260px', background: '#0f172a' }}>
                <img
                  src={product.image_urls[0] || 'https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=800&q=80'}
                  alt={product.title}
                  style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                />
                <span style={{
                  position: 'absolute',
                  top: '12px',
                  left: '12px',
                  padding: '4px 10px',
                  background: 'rgba(15, 23, 42, 0.85)',
                  backdropFilter: 'blur(4px)',
                  borderRadius: '6px',
                  fontSize: '11px',
                  fontWeight: 600,
                  letterSpacing: '0.04em',
                  color: '#fff',
                  border: '1px solid rgba(255,255,255,0.1)'
                }}>
                  {product.platform}
                </span>

                <span style={{
                  position: 'absolute',
                  top: '12px',
                  right: '12px',
                  padding: '4px 8px',
                  background: 'rgba(16, 185, 129, 0.9)',
                  borderRadius: '6px',
                  fontSize: '11px',
                  fontWeight: 700,
                  color: '#fff'
                }}>
                  {Math.round(product.match_score * 100)}% Match
                </span>
              </div>

              {/* Content */}
              <div style={{ padding: '16px', display: 'flex', flexDirection: 'column', flex: 1 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: '8px' }}>
                  <span style={{ fontSize: '12px', color: 'var(--text-muted)', fontWeight: 600 }}>
                    {product.brand || product.seller}
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

                {/* Price and MRP */}
                <div style={{ display: 'flex', alignItems: 'baseline', gap: '8px', marginBottom: '12px' }}>
                  <span style={{ fontSize: '18px', fontWeight: 700, color: '#fff' }}>
                    Rs. {product.price.toLocaleString()}
                  </span>
                  {product.mrp && product.mrp > product.price && (
                    <>
                      <span style={{ fontSize: '13px', color: 'var(--text-muted)', textDecoration: 'line-through' }}>
                        Rs. {product.mrp.toLocaleString()}
                      </span>
                      <span style={{ fontSize: '12px', color: 'var(--accent-green)', fontWeight: 600 }}>
                        {Math.round(((product.mrp - product.price) / product.mrp) * 100)}% off
                      </span>
                    </>
                  )}
                </div>

                {/* Delivery Badge */}
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  padding: '6px 10px',
                  background: 'rgba(255,255,255,0.03)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: '6px',
                  fontSize: '12px',
                  marginBottom: '14px'
                }}>
                  <Truck size={14} color="#38bdf8" />
                  <span>
                    Estimated: <strong style={{ color: '#fff' }}>{product.estimated_delivery_days} days</strong> ({product.delivery_status})
                  </span>
                </div>

                {/* Why This Matched Box */}
                <div style={{
                  background: 'rgba(59, 130, 246, 0.08)',
                  border: '1px solid rgba(59, 130, 246, 0.25)',
                  borderRadius: '8px',
                  padding: '10px 12px',
                  fontSize: '12px',
                  color: '#bfdbfe',
                  marginBottom: '16px',
                  flex: 1
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '4px', marginBottom: '4px', fontWeight: 600, color: '#60a5fa' }}>
                    <Sparkles size={12} />
                    <span>Why this matched</span>
                  </div>
                  <p style={{ lineHeight: '1.4' }}>{product.why_matched}</p>
                </div>

                {/* CTA Button */}
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
                    background: '#1e293b',
                    border: '1px solid var(--border-subtle)',
                    color: '#fff',
                    fontSize: '13px',
                    fontWeight: 600,
                    textAlign: 'center',
                    transition: 'background 0.15s'
                  }}
                >
                  <span>View on {product.platform}</span>
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
            No sarees survived the filters for this criteria. Try relaxing budget or delivery constraints.
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
