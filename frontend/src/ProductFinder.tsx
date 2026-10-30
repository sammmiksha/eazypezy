import { FormEvent, useEffect, useMemo, useState } from 'react';
import { ArrowUpRight, BadgeCheck, Check, ChevronRight, CircleDollarSign, Cpu, ExternalLink, MapPin, Search, ShieldCheck, SlidersHorizontal, Sparkles, Star, Wifi } from 'lucide-react';
import { ProductOut, SearchResponse } from './types';
import './product-finder.css';

const API_BASE = 'http://localhost:8000/api/v1';
const EXAMPLES = [
  '5G phone, budget 40000, best screen',
  'Ergonomic office chair under ₹15,000',
  '8 kg front-load washing machine below ₹35,000',
  'Pink cotton shirt under 1000',
];

const humanize = (value: string) => value.replace(/_/g, ' ').replace(/\b\w/g, char => char.toUpperCase());
const money = (value: number) => new Intl.NumberFormat('en-IN', { maximumFractionDigits: 0 }).format(value);

function ProductCard({ product, index }: { product: ProductOut; index: number }) {
  const visibleSpecs = Object.entries(product.specs || {}).filter(([key]) => key !== 'display_score').slice(0, 5);
  const isTopPick = index === 0;
  return (
    <article className={`product-card ${isTopPick ? 'product-card--top' : ''}`}>
      <div className="product-card__image-wrap">
        {product.image_urls[0] ? <img src={product.image_urls[0]} alt="" className="product-card__image" /> : <div className="product-card__image product-card__image--empty"><Cpu size={34} /></div>}
        <div className="product-card__store">{product.platform}</div>
        {isTopPick && <div className="product-card__top-badge"><Sparkles size={13} /> Best match</div>}
        {product.is_best_deal && <div className="product-card__deal-badge">Lowest price</div>}
      </div>
      <div className="product-card__body">
        <div className="product-card__meta">
          <span>{product.brand || product.seller || 'Marketplace listing'}</span>
          <span><Star size={13} fill="currentColor" /> {product.rating || '—'}</span>
        </div>
        <h3>{product.title}</h3>
        <div className="product-card__price-row">
          <strong>₹{money(product.price)}</strong>
          {product.mrp && product.mrp > product.price && <s>₹{money(product.mrp)}</s>}
          {product.discount_percent > 0 && <em>{Math.round(product.discount_percent)}% off</em>}
        </div>
        <div className="product-card__match">
          <span><BadgeCheck size={16} /> {product.requirement_score}% fit</span>
          <span>{product.estimated_delivery_days ? `${product.estimated_delivery_days}-day delivery` : 'Delivery at checkout'}</span>
        </div>
        {visibleSpecs.length > 0 && <div className="spec-list">
          {visibleSpecs.map(([key, value]) => <span key={key}>{humanize(key)}: <b>{String(value)}</b></span>)}
        </div>}
        <p className="product-card__reason">{product.why_matched}</p>
        <a href={product.product_url} target="_blank" rel="noreferrer" className="product-card__link">View at {product.platform} <ExternalLink size={15} /></a>
      </div>
    </article>
  );
}

export default function ProductFinder() {
  const [query, setQuery] = useState(EXAMPLES[0]);
  const [pincode, setPincode] = useState('');
  const [response, setResponse] = useState<SearchResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const saved = localStorage.getItem('easypezy_pincode');
    if (saved) setPincode(saved);
  }, []);

  const requirementPills = useMemo(() => {
    if (!response) return [];
    return [
      ...Object.entries(response.parsed_query.attributes.required_specs || {}).map(([key, value]) => ({ label: `${humanize(key)}: ${value}`, type: 'required' })),
      ...Object.entries(response.parsed_query.attributes.preferred_specs || {}).map(([key]) => ({ label: humanize(key).replace(' Priority', ''), type: 'preferred' })),
      response.parsed_query.budget_max ? { label: `Up to ₹${money(response.parsed_query.budget_max)}`, type: 'required' } : null,
    ].filter(Boolean) as { label: string; type: string }[];
  }, [response]);

  async function search(event?: FormEvent, value = query) {
    event?.preventDefault();
    if (!value.trim()) return;
    setLoading(true);
    setError('');
    try {
      const request = await fetch(`${API_BASE}/search`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: value, pincode: pincode.trim() || undefined }),
      });
      if (!request.ok) throw new Error('The search service did not respond. Start the backend on port 8000 and try again.');
      const data = await request.json() as SearchResponse;
      setResponse(data);
      if (pincode.trim()) localStorage.setItem('easypezy_pincode', pincode.trim());
    } catch (cause) {
      setResponse(null);
      setError(cause instanceof Error ? cause.message : 'Unable to search right now.');
    } finally {
      setLoading(false);
    }
  }

  function useExample(example: string) {
    setQuery(example);
    void search(undefined, example);
  }

  return (
    <main className="finder-shell">
      <header className="finder-nav">
        <a className="brand" href="#top"><span className="brand__mark">e</span><span>easypezy</span></a>
        <div className="nav-trust"><ShieldCheck size={16} /> Compare before you buy</div>
      </header>

      <section id="top" className="finder-hero">
        <div className="eyebrow"><Sparkles size={14} /> Requirement-aware product search</div>
        <h1>Tell us what matters.<br /><span>We’ll find the fit.</span></h1>
        <p>Search any product category in ordinary language. We turn your budget, must-haves and preferences into a transparent product shortlist.</p>
        <form className="search-panel" onSubmit={search}>
          <div className="search-panel__query"><Search size={21} /><input aria-label="Product search" value={query} onChange={event => setQuery(event.target.value)} placeholder="e.g. a quiet 8 kg washing machine under ₹35,000" /></div>
          <div className="search-panel__location"><MapPin size={18} /><input aria-label="Delivery pincode" value={pincode} maxLength={6} inputMode="numeric" onChange={event => setPincode(event.target.value.replace(/\D/g, ''))} placeholder="PIN code" /></div>
          <button type="submit" disabled={loading}>{loading ? 'Finding matches…' : <>Find products <ArrowUpRight size={18} /></>}</button>
        </form>
        <div className="example-row"><span>Try:</span>{EXAMPLES.map(example => <button key={example} onClick={() => useExample(example)}>{example}</button>)}</div>
      </section>

      {error && <div className="message message--error">{error}</div>}

      {!response && !loading && !error && <section className="how-it-works">
        <div><span className="step-icon"><SlidersHorizontal /></span><h2>Read the real request</h2><p>“5G”, “8 kg” or “ergonomic” can be must-haves. “Best screen” is a preference.</p></div>
        <ChevronRight className="how-it-works__arrow" />
        <div><span className="step-icon"><CircleDollarSign /></span><h2>Compare the right offers</h2><p>Price, seller, rating and delivery are considered only after essential requirements match.</p></div>
        <ChevronRight className="how-it-works__arrow" />
        <div><span className="step-icon"><Check /></span><h2>Show why it won</h2><p>Every recommendation explains what it matched, so the final choice stays yours.</p></div>
      </section>}

      {loading && <div className="loading-state"><span></span> Reading requirements and comparing offers…</div>}

      {response && <section className="results-section">
        <div className="results-intro">
          <div>
            <div className="result-source"><span className={response.data_source === 'live_shopping_api' ? 'live-dot' : 'demo-dot'}></span>{response.data_source === 'live_shopping_api' ? 'Live shopping API results' : 'Demo catalog results'}</div>
            <h2>{response.total_found} offers meet your requirements</h2>
            <p>Ranked by your stated preferences, value and seller signal.</p>
          </div>
          {response.deal_comparison && <div className="savings-card"><span>Lowest matching offer</span><strong>₹{money(response.deal_comparison.lowest_price)}</strong><p>Save up to ₹{money(response.deal_comparison.max_savings)} across {response.deal_comparison.total_sellers_found} offers</p></div>}
        </div>

        <div className="requirements-bar">
          <div><Wifi size={16} /><span>Understood from your search</span></div>
          <div className="pill-group">{requirementPills.length ? requirementPills.map(pill => <span key={pill.label} className={`pill pill--${pill.type}`}>{pill.type === 'required' && <Check size={12} />}{pill.label}</span>) : <span className="pill">No specific requirements detected</span>}</div>
        </div>

        {response.parsed_query.clarifications_needed.length > 0 && <div className="message message--tip">{response.parsed_query.clarifications_needed[0]}</div>}
        {response.results.length > 0 ? <div className="product-grid">{response.results.map((product, index) => <ProductCard key={`${product.platform}-${product.id}`} product={product} index={index} />)}</div> : <div className="empty-state"><Search size={28} /><h2>No matching offers yet</h2><p>Try widening the budget or removing one must-have requirement.</p></div>}
      </section>}
    </main>
  );
}
