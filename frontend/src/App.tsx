import React, { useState, useEffect } from 'react';
import { Search, Mic, MicOff, Truck, Star, ExternalLink, Sparkles, TrendingDown, MapPin, User, ArrowRight, Edit2 } from 'lucide-react';
import { SearchResponse, ProductOut } from './types';

const API_BASE = "http://localhost:8000/api/v1";

export default function App() {
  // Step 1: User Profile & Location first
  const [userName, setUserName] = useState<string>("");
  const [pincode, setPincode] = useState<string>("");
  const [isConfigured, setIsConfigured] = useState<boolean>(false);
  const [profileError, setProfileError] = useState<string | null>(null);

  // Step 2: Main Search State
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [searchError, setSearchError] = useState<string | null>(null);
  const [response, setResponse] = useState<SearchResponse | null>(null);
  const [isListening, setIsListening] = useState(false);

  // Load saved user info from localStorage if available
  useEffect(() => {
    const savedName = localStorage.getItem("easypezy_user_name");
    const savedPin = localStorage.getItem("easypezy_pincode");
    if (savedName && savedPin) {
      setUserName(savedName);
      setPincode(savedPin);
      setIsConfigured(true);
    }
  }, []);

  const handleProfileSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!userName.trim()) {
      setProfileError("Please enter your name");
      return;
    }
    if (!pincode.trim() || pincode.trim().length !== 6 || !/^\d+$/.test(pincode.trim())) {
      setProfileError("Please enter a valid 6-digit delivery pincode");
      return;
    }

    setProfileError(null);
    localStorage.setItem("easypezy_user_name", userName.trim());
    localStorage.setItem("easypezy_pincode", pincode.trim());
    setIsConfigured(true);
  };

  const handleEditProfile = () => {
    setIsConfigured(false);
  };

  const executeSearch = async (searchQuery: string) => {
    if (!searchQuery.trim()) return;
    setLoading(true);
    setSearchError(null);

    try {
      const res = await fetch(`${API_BASE}/search`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query: searchQuery,
          pincode: pincode.trim() || undefined
        }),
      });

      if (!res.ok) {
        throw new Error(`Search request failed with status ${res.status}`);
      }

      const data: SearchResponse = await res.json();
      setResponse(data);
    } catch (err: any) {
      setSearchError(err.message || "Failed to execute search. Make sure backend is running on port 8000.");
    } finally {
      setLoading(false);
    }
  };

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

  // View 1: Name and Location / Pincode Section First
  if (!isConfigured) {
    return (
      <div style={{ maxWidth: '480px', margin: '80px auto 40px auto', padding: '0 16px' }}>
        <div style={{
          background: '#2B124C',
          border: '1px solid #522B5B',
          borderRadius: '16px',
          padding: '32px 24px',
          boxShadow: 'none'
        }}>
          <div style={{ marginBottom: '24px', textAlign: 'center' }}>
            <h1 style={{ fontSize: '26px', fontWeight: 800, color: '#FBE4D8', letterSpacing: '-0.02em' }}>
              EasyPezy
            </h1>
            <p style={{ color: '#DFB6B2', fontSize: '14px', marginTop: '6px' }}>
              Enter your details to calculate delivery timelines and compare prices across platforms.
            </p>
          </div>

          {profileError && (
            <div style={{
              background: '#522B5B',
              border: '1px solid #854F6C',
              color: '#FBE4D8',
              padding: '10px 14px',
              borderRadius: '8px',
              fontSize: '13px',
              marginBottom: '18px'
            }}>
              {profileError}
            </div>
          )}

          <form onSubmit={handleProfileSubmit}>
            <div style={{ marginBottom: '18px' }}>
              <label style={{ display: 'block', fontSize: '13px', fontWeight: 600, color: '#DFB6B2', marginBottom: '8px' }}>
                Your Name
              </label>
              <div style={{
                display: 'flex',
                alignItems: 'center',
                background: '#190019',
                border: '1px solid #522B5B',
                borderRadius: '10px',
                padding: '10px 14px'
              }}>
                <User size={18} color="#DFB6B2" style={{ marginRight: '10px' }} />
                <input
                  type="text"
                  value={userName}
                  onChange={(e) => setUserName(e.target.value)}
                  placeholder="Enter full name"
                  style={{
                    background: 'transparent',
                    border: 'none',
                    outline: 'none',
                    color: '#FBE4D8',
                    fontSize: '15px',
                    width: '100%'
                  }}
                />
              </div>
            </div>

            <div style={{ marginBottom: '24px' }}>
              <label style={{ display: 'block', fontSize: '13px', fontWeight: 600, color: '#DFB6B2', marginBottom: '8px' }}>
                Delivery Pincode / Location
              </label>
              <div style={{
                display: 'flex',
                alignItems: 'center',
                background: '#190019',
                border: '1px solid #522B5B',
                borderRadius: '10px',
                padding: '10px 14px'
              }}>
                <MapPin size={18} color="#DFB6B2" style={{ marginRight: '10px' }} />
                <input
                  type="text"
                  maxLength={6}
                  value={pincode}
                  onChange={(e) => setPincode(e.target.value)}
                  placeholder="Enter 6-digit Indian PIN code (e.g. 560034)"
                  style={{
                    background: 'transparent',
                    border: 'none',
                    outline: 'none',
                    color: '#FBE4D8',
                    fontSize: '15px',
                    width: '100%'
                  }}
                />
              </div>
            </div>

            <button
              type="submit"
              style={{
                width: '100%',
                background: '#854F6C',
                color: '#FBE4D8',
                border: '1px solid #DFB6B2',
                borderRadius: '10px',
                padding: '12px 18px',
                fontSize: '15px',
                fontWeight: 700,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px'
              }}
            >
              <span>Continue to Search</span>
              <ArrowRight size={18} />
            </button>
          </form>
        </div>
      </div>
    );
  }

  // View 2: Main Search Page
  return (
    <div style={{ maxWidth: '1240px', margin: '0 auto', padding: '24px 16px' }}>
      {/* Top Header & User Info Bar */}
      <header style={{ marginBottom: '24px', borderBottom: '1px solid #522B5B', paddingBottom: '18px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '14px' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <h1 style={{ fontSize: '26px', fontWeight: 800, letterSpacing: '-0.02em', color: '#FBE4D8' }}>
                EasyPezy
              </h1>
              <span style={{
                fontSize: '11px',
                fontWeight: 700,
                padding: '3px 8px',
                borderRadius: '6px',
                background: '#522B5B',
                color: '#FBE4D8',
                letterSpacing: '0.05em',
                textTransform: 'uppercase',
                border: '1px solid #854F6C'
              }}>
                Universal Deal Finder
              </span>
            </div>
          </div>

          {/* Active User and Delivery Location display with Edit Button */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            background: '#2B124C',
            border: '1px solid #522B5B',
            borderRadius: '10px',
            padding: '8px 14px'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <User size={15} color="#DFB6B2" />
              <span style={{ fontSize: '13px', fontWeight: 700, color: '#FBE4D8' }}>
                {userName}
              </span>
            </div>
            <span style={{ color: '#522B5B' }}>|</span>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <MapPin size={15} color="#DFB6B2" />
              <span style={{ fontSize: '13px', color: '#DFB6B2' }}>
                PIN: <strong style={{ color: '#FBE4D8' }}>{pincode}</strong>
              </span>
            </div>
            <button
              onClick={handleEditProfile}
              title="Change user or delivery location"
              style={{
                marginLeft: '6px',
                padding: '4px 8px',
                background: '#522B5B',
                border: '1px solid #854F6C',
                borderRadius: '6px',
                color: '#FBE4D8',
                fontSize: '11px',
                display: 'flex',
                alignItems: 'center',
                gap: '4px'
              }}
            >
              <Edit2 size={12} />
              <span>Change</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Search Input */}
      <section style={{ marginBottom: '24px' }}>
        <form onSubmit={(e) => { e.preventDefault(); executeSearch(query); }}>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            background: '#2B124C',
            border: '1px solid #522B5B',
            borderRadius: '12px',
            padding: '8px 12px'
          }}>
            <Search size={20} color="#DFB6B2" style={{ marginRight: '10px' }} />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search gadgets, clothing, or appliances (e.g. iPhone 18 1TB, Sony WH-1000XM5)"
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
              title="Voice Search"
              style={{
                padding: '8px',
                borderRadius: '8px',
                background: isListening ? '#854F6C' : '#190019',
                color: '#FBE4D8',
                marginRight: '8px',
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
                padding: '10px 20px',
                borderRadius: '8px',
                border: '1px solid #DFB6B2'
              }}
            >
              {loading ? "Searching..." : "Search Deals"}
            </button>
          </div>
        </form>
      </section>

      {/* Error Banner */}
      {searchError && (
        <div style={{
          padding: '12px 16px',
          background: '#522B5B',
          border: '1px solid #854F6C',
          borderRadius: '8px',
          marginBottom: '20px',
          color: '#FBE4D8',
          fontSize: '14px'
        }}>
          {searchError}
        </div>
      )}

      {/* Static Best Deal Comparison Banner */}
      {response && response.deal_comparison && (
        <div style={{
          background: '#2B124C',
          border: '1px solid #854F6C',
          borderRadius: '12px',
          padding: '16px 20px',
          marginBottom: '22px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: '12px'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
            <div style={{
              width: '40px',
              height: '40px',
              borderRadius: '8px',
              background: '#522B5B',
              border: '1px solid #854F6C',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#FBE4D8'
            }}>
              <TrendingDown size={22} />
            </div>
            <div>
              <span style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.05em', color: '#DFB6B2', fontWeight: 700 }}>
                Cross-Platform Price Summary
              </span>
              <h3 style={{ fontSize: '17px', fontWeight: 800, color: '#FBE4D8' }}>
                Lowest price on {response.deal_comparison.lowest_platform} at Rs. {response.deal_comparison.lowest_price.toLocaleString()}
              </h3>
              <p style={{ fontSize: '13px', color: '#DFB6B2' }}>
                Found across {response.deal_comparison.total_sellers_found} platforms for pincode {pincode}.
              </p>
            </div>
          </div>
          <div>
            <span style={{
              fontSize: '13px',
              padding: '6px 14px',
              borderRadius: '6px',
              background: '#DFB6B2',
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
          borderRadius: '10px',
          padding: '12px 16px',
          marginBottom: '22px'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px', flexWrap: 'wrap', gap: '8px' }}>
            <span style={{ fontSize: '12px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em', color: '#DFB6B2' }}>
              Detected Attributes
            </span>
            <div style={{ display: 'flex', gap: '12px', fontSize: '12px', color: '#DFB6B2' }}>
              <span>Language: <strong style={{ color: '#FBE4D8' }}>{response.parsed_query.detected_language.toUpperCase()}</strong></span>
              <span>Search phrase: <strong style={{ color: '#FBE4D8' }}>"{response.parsed_query.clean_search_phrase}"</strong></span>
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
            <span style={badgeStyle}>
              Delivering to: <strong style={{ marginLeft: '4px', color: '#FBE4D8' }}>{pincode}</strong>
            </span>
          </div>
        </section>
      )}

      {/* Results Header */}
      {response && (
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <h2 style={{ fontSize: '18px', fontWeight: 800, color: '#FBE4D8' }}>
            Available Platforms ({response.total_found})
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
          gap: '20px'
        }}>
          {response.results.map((product) => (
            <div
              key={`${product.platform}-${product.id}`}
              style={{
                background: '#2B124C',
                border: product.is_best_deal ? '1px solid #DFB6B2' : '1px solid #522B5B',
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
                  background: '#DFB6B2',
                  color: '#190019',
                  fontSize: '11px',
                  fontWeight: 900,
                  letterSpacing: '0.05em',
                  padding: '5px 12px',
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
              <div style={{ position: 'relative', height: '220px', background: '#190019' }}>
                <img
                  src={product.image_urls[0] || 'https://images.unsplash.com/photo-1695048133142-1a20484d2569?auto=format&fit=crop&w=800&q=80'}
                  alt={product.title}
                  style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                />
                {/* Platform Tag */}
                <span style={{
                  position: 'absolute',
                  top: '10px',
                  left: '10px',
                  padding: '4px 8px',
                  background: '#190019',
                  borderRadius: '4px',
                  fontSize: '11px',
                  fontWeight: 700,
                  color: '#FBE4D8',
                  border: '1px solid #522B5B'
                }}>
                  {product.platform}
                </span>

                {product.discount_percent > 0 && (
                  <span style={{
                    position: 'absolute',
                    top: '10px',
                    right: '10px',
                    padding: '3px 6px',
                    background: '#854F6C',
                    border: '1px solid #DFB6B2',
                    borderRadius: '4px',
                    fontSize: '11px',
                    fontWeight: 800,
                    color: '#FBE4D8'
                  }}>
                    {Math.round(product.discount_percent)}% OFF
                  </span>
                )}
              </div>

              {/* Details */}
              <div style={{ padding: '16px', display: 'flex', flexDirection: 'column', flex: 1 }}>
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
                  <span style={{ fontSize: '19px', fontWeight: 800, color: '#FBE4D8' }}>
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
                          padding: '2px 6px',
                          background: '#190019',
                          borderRadius: '4px',
                          color: '#FBE4D8',
                          border: '1px solid #522B5B'
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
                  background: '#190019',
                  border: '1px solid #522B5B',
                  borderRadius: '6px',
                  fontSize: '12px',
                  marginBottom: '12px',
                  color: '#DFB6B2'
                }}>
                  <Truck size={14} color="#DFB6B2" />
                  <span>
                    Delivery to {pincode}: <strong style={{ color: '#FBE4D8' }}>{product.estimated_delivery_days} days</strong> ({product.delivery_status})
                  </span>
                </div>

                {/* Why This Matched Box */}
                <div style={{
                  background: '#190019',
                  border: '1px solid #522B5B',
                  borderRadius: '8px',
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
                    padding: '10px',
                    borderRadius: '8px',
                    background: product.is_best_deal ? '#DFB6B2' : '#522B5B',
                    border: '1px solid #854F6C',
                    color: product.is_best_deal ? '#190019' : '#FBE4D8',
                    fontSize: '13px',
                    fontWeight: 800,
                    textAlign: 'center'
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
          borderRadius: '12px',
          border: '1px solid #522B5B'
        }}>
          <p style={{ color: '#DFB6B2', fontSize: '15px' }}>
            No platforms found for this item with the current delivery location and filters.
          </p>
        </div>
      ) : null}
    </div>
  );
}

const badgeStyle: React.CSSProperties = {
  fontSize: '12px',
  padding: '4px 10px',
  borderRadius: '6px',
  background: '#190019',
  border: '1px solid #522B5B',
  color: '#DFB6B2'
};
