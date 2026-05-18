import {
  Home, MapPin, Building2, Bed, Maximize2, Banknote, Calendar, User,
  Info, ShieldCheck, AlertTriangle, ChevronRight, CheckCircle2, Phone,
  Briefcase, FileText, Layers, BarChart3, Wallet, Compass, Star,
  TreePine, Sparkles, Sofa, Car, Building, ArrowRight, Box,
} from "lucide-react";

const ACCENT = "#34D399";

const fmtINR = (n) => {
  if (n == null) return "—";
  if (n >= 10000000) return `₹${(n / 10000000).toFixed(2)} Cr`;
  if (n >= 100000)   return `₹${(n / 100000).toFixed(2)} L`;
  if (n >= 1000)     return `₹${(n / 1000).toFixed(0)}k`;
  return `₹${n}`;
};

const fmtINRFull = (n) => "₹" + Number(n).toLocaleString("en-IN", { maximumFractionDigits: 0 });

const LISTING_TYPE_META = {
  sale: { label: "For sale",  color: "#34D399" },
  rent: { label: "For rent",  color: "#60A5FA" },
};

/* ─── TextBlock ────────────────────────────────────────── */
export function TextBlock({ content }) {
  const parts = content.split(/(\*\*[^*]+\*\*)/g);
  return (
    <div
      className="text-sm leading-relaxed px-4 py-2.5 rounded-2xl rounded-tl-md"
      style={{ background: "rgba(255,255,255,0.03)", color: "rgba(255,255,255,0.88)" }}
    >
      {parts.map((p, i) =>
        p.startsWith("**") && p.endsWith("**") ? (
          <strong key={i} className="text-white font-medium">{p.slice(2, -2)}</strong>
        ) : (
          <span key={i}>{p.split("\n").map((line, j, arr) => (
            <span key={j}>{line}{j < arr.length - 1 && <br />}</span>
          ))}</span>
        )
      )}
    </div>
  );
}

/* ─── DisclaimerBlock ──────────────────────────────────── */
export function DisclaimerBlock({ content }) {
  return (
    <div
      className="flex items-start gap-2.5 px-4 py-2.5 rounded-2xl border"
      style={{ background: "rgba(250, 204, 21, 0.04)", borderColor: "rgba(250, 204, 21, 0.18)", color: "rgba(250, 204, 21, 0.85)" }}
    >
      <Info size={14} className="mt-0.5 flex-shrink-0" />
      <div className="text-11 leading-relaxed">{content}</div>
    </div>
  );
}

/* ─── FairHousingAlertBlock (fair-housing / privacy / social-eng) ─── */
export function FairHousingAlertBlock({ headline, message, indicators, offer }) {
  return (
    <div
      className="rounded-2xl border-2 p-4 housing-pulse"
      style={{
        background: "linear-gradient(180deg, rgba(52,211,153,0.10), rgba(52,211,153,0.02))",
        borderColor: "rgba(52,211,153,0.4)",
      }}
    >
      <div className="flex items-center gap-2 mb-2">
        <ShieldCheck size={18} style={{ color: ACCENT }} />
        <div className="text-sm font-semibold" style={{ color: ACCENT }}>{headline}</div>
      </div>
      <div className="text-xs leading-relaxed mb-3" style={{ color: "rgba(255,255,255,0.85)" }}>{message}</div>
      <div className="space-y-1 mb-3">
        {indicators.map((it, i) => (
          <div key={i} className="flex items-start gap-2 text-11" style={{ color: "rgba(255,255,255,0.7)" }}>
            <AlertTriangle size={10} style={{ color: ACCENT, marginTop: 3, flexShrink: 0 }} />
            <span>{it}</span>
          </div>
        ))}
      </div>
      <div
        className="flex items-start gap-2 px-3 py-2 rounded-lg border"
        style={{ background: "rgba(255,255,255,0.04)", borderColor: ACCENT + "33" }}
      >
        <Sparkles size={12} style={{ color: ACCENT, marginTop: 2, flexShrink: 0 }} />
        <div className="text-11 leading-relaxed" style={{ color: "rgba(255,255,255,0.9)" }}>{offer}</div>
      </div>
    </div>
  );
}

/* ─── Property card (used by list & by detail) ─────────── */
function PropertyCard({ p, dense = false }) {
  const meta = LISTING_TYPE_META[p.listing_type] || { label: p.listing_type, color: ACCENT };
  return (
    <div className="rounded-xl p-3 border"
      style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
      <div className="flex items-start gap-3">
        <div className="rounded-lg flex items-center justify-center flex-shrink-0"
          style={{ width: 44, height: 44, background: ACCENT + "14" }}>
          {p.type === "Villa" ? <Home size={18} style={{ color: ACCENT }} /> :
           p.type === "Office" || p.type === "Showroom" ? <Briefcase size={18} style={{ color: ACCENT }} /> :
                                                          <Building2 size={18} style={{ color: ACCENT }} />}
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between gap-2 mb-0.5">
            <div className="text-xs font-medium" style={{ color: "white" }}>{p.title}</div>
            <span className="text-9 px-1.5 py-0.5 rounded-full font-medium uppercase tracking-tightest2 flex-shrink-0"
              style={{ background: meta.color + "22", color: meta.color }}>
              {meta.label}
            </span>
          </div>
          <div className="flex items-center gap-1 text-10 mb-1.5" style={{ color: "rgba(255,255,255,0.55)" }}>
            <MapPin size={9} />
            <span>{p.neighborhood}, {p.city}</span>
            <span style={{ color: "rgba(255,255,255,0.3)" }}>·</span>
            <span>{p.type}</span>
            {p.rera_id && (
              <>
                <span style={{ color: "rgba(255,255,255,0.3)" }}>·</span>
                <span style={{ color: "#86efac" }}>RERA ✓</span>
              </>
            )}
          </div>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3 text-10" style={{ color: "rgba(255,255,255,0.7)" }}>
              {p.bhk != null && (
                <span className="flex items-center gap-1"><Bed size={9} /> {p.bhk} BHK</span>
              )}
              <span className="flex items-center gap-1"><Maximize2 size={9} /> {p.carpet_sqft} sqft</span>
              {!dense && p.furnishing && (
                <span className="flex items-center gap-1"><Sofa size={9} /> {p.furnishing.split(" ")[0]}</span>
              )}
            </div>
            <div className="text-right">
              <div className="text-xs font-mono font-medium" style={{ color: ACCENT }}>
                {fmtINR(p.price)}{p.listing_type === "rent" ? <span className="text-9" style={{ color: "rgba(255,255,255,0.5)" }}>/mo</span> : ""}
              </div>
              {p.price_per_sqft && (
                <div className="text-9 font-mono" style={{ color: "rgba(255,255,255,0.45)" }}>
                  ₹{p.price_per_sqft.toLocaleString("en-IN")}/sqft
                </div>
              )}
            </div>
          </div>
          {!dense && p.id && (
            <div className="text-9 font-mono mt-1.5" style={{ color: "rgba(255,255,255,0.35)" }}>{p.id}</div>
          )}
        </div>
      </div>
    </div>
  );
}

/* ─── PropertyListBlock ────────────────────────────────── */
export function PropertyListBlock({ title, items, total }) {
  return (
    <div className="space-y-2">
      {title && (
        <div className="flex items-center justify-between px-1">
          <div className="text-10 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>{title}</div>
          <div className="text-10 font-mono" style={{ color: "rgba(255,255,255,0.55)" }}>{total} found</div>
        </div>
      )}
      {items.map((p) => <PropertyCard key={p.id} p={p} />)}
    </div>
  );
}

/* ─── PropertyDetailBlock ──────────────────────────────── */
export function PropertyDetailBlock({ property: p }) {
  const meta = LISTING_TYPE_META[p.listing_type] || { label: p.listing_type, color: ACCENT };
  const isRent = p.listing_type === "rent";
  return (
    <div className="rounded-xl border overflow-hidden"
      style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
      {/* Header */}
      <div className="px-4 py-3 border-b" style={{ borderColor: "rgba(255,255,255,0.06)", background: ACCENT + "0C" }}>
        <div className="flex items-center justify-between mb-1">
          <div className="text-sm font-medium" style={{ color: "white" }}>{p.title}</div>
          <span className="text-9 px-1.5 py-0.5 rounded-full font-medium uppercase tracking-tightest2"
            style={{ background: meta.color + "22", color: meta.color }}>{meta.label}</span>
        </div>
        <div className="flex items-center gap-1 text-11" style={{ color: "rgba(255,255,255,0.6)" }}>
          <MapPin size={11} /><span>{p.neighborhood}, {p.city}</span>
          <span style={{ color: "rgba(255,255,255,0.3)" }}>·</span>
          <span>{p.type}</span>
          <span style={{ color: "rgba(255,255,255,0.3)" }}>·</span>
          <span className="font-mono">{p.id}</span>
        </div>
      </div>

      {/* Price strip */}
      <div className="px-4 py-3 flex items-end justify-between border-b" style={{ borderColor: "rgba(255,255,255,0.06)" }}>
        <div>
          <div className="text-xs" style={{ color: "rgba(255,255,255,0.5)" }}>{isRent ? "Monthly rent" : "Asking price"}</div>
          <div className="text-xl font-mono font-medium" style={{ color: ACCENT }}>
            {fmtINRFull(p.price)}{isRent && <span className="text-xs" style={{ color: "rgba(255,255,255,0.5)" }}>/mo</span>}
          </div>
          {p.price_per_sqft && (
            <div className="text-10 font-mono" style={{ color: "rgba(255,255,255,0.55)" }}>
              ₹{p.price_per_sqft.toLocaleString("en-IN")}/sqft
            </div>
          )}
        </div>
        <div className="text-right">
          {isRent && p.deposit && (
            <>
              <div className="text-10 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>Deposit</div>
              <div className="text-sm font-mono" style={{ color: "white" }}>{fmtINRFull(p.deposit)}</div>
            </>
          )}
          {!isRent && p.maintenance_per_month && (
            <>
              <div className="text-10 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>Maintenance</div>
              <div className="text-sm font-mono" style={{ color: "white" }}>{fmtINRFull(p.maintenance_per_month)}<span className="text-9" style={{ color: "rgba(255,255,255,0.5)" }}>/mo</span></div>
            </>
          )}
        </div>
      </div>

      {/* Facts grid */}
      <div className="px-4 py-3 grid grid-cols-3 gap-3 border-b" style={{ borderColor: "rgba(255,255,255,0.06)" }}>
        {p.bhk != null && (
          <div>
            <div className="text-9 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>Config</div>
            <div className="text-xs flex items-center gap-1" style={{ color: "white" }}><Bed size={11} /> {p.bhk} BHK</div>
          </div>
        )}
        <div>
          <div className="text-9 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>Carpet</div>
          <div className="text-xs flex items-center gap-1" style={{ color: "white" }}><Maximize2 size={11} /> {p.carpet_sqft} sqft</div>
        </div>
        <div>
          <div className="text-9 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>Built-up</div>
          <div className="text-xs font-mono" style={{ color: "white" }}>{p.built_up_sqft} sqft</div>
        </div>
        <div>
          <div className="text-9 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>Floor</div>
          <div className="text-xs" style={{ color: "white" }}>{p.floor}</div>
        </div>
        <div>
          <div className="text-9 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>Facing</div>
          <div className="text-xs flex items-center gap-1" style={{ color: "white" }}><Compass size={11} /> {p.facing}</div>
        </div>
        <div>
          <div className="text-9 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>Age</div>
          <div className="text-xs" style={{ color: "white" }}>{p.age_years} yr{p.age_years === 1 ? "" : "s"}</div>
        </div>
        <div className="col-span-2">
          <div className="text-9 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>Furnishing</div>
          <div className="text-xs flex items-center gap-1" style={{ color: "white" }}><Sofa size={11} /> {p.furnishing}</div>
        </div>
        <div>
          <div className="text-9 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>Available</div>
          <div className="text-xs" style={{ color: "white" }}>{p.available_from}</div>
        </div>
      </div>

      {/* Highlights */}
      {p.highlights && p.highlights.length > 0 && (
        <div className="px-4 py-3 border-b" style={{ borderColor: "rgba(255,255,255,0.06)" }}>
          <div className="text-10 uppercase tracking-tightest2 mb-1.5" style={{ color: "rgba(255,255,255,0.4)" }}>Highlights</div>
          <div className="flex flex-wrap gap-1">
            {p.highlights.map((h, i) => (
              <span key={i} className="text-10 px-2 py-0.5 rounded-full" style={{ background: ACCENT + "1A", color: ACCENT }}>
                {h}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Amenities */}
      {p.amenities && p.amenities.length > 0 && (
        <div className="px-4 py-3 border-b" style={{ borderColor: "rgba(255,255,255,0.06)" }}>
          <div className="text-10 uppercase tracking-tightest2 mb-1.5" style={{ color: "rgba(255,255,255,0.4)" }}>Amenities</div>
          <div className="grid grid-cols-2 gap-1">
            {p.amenities.map((a, i) => (
              <div key={i} className="flex items-center gap-1.5 text-11" style={{ color: "rgba(255,255,255,0.75)" }}>
                <CheckCircle2 size={9} style={{ color: ACCENT }} /> {a}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* RERA */}
      {p.rera_id && (
        <div className="px-4 py-2.5 flex items-center justify-between"
          style={{ background: "rgba(134,239,172,0.06)" }}>
          <div className="flex items-center gap-2">
            <ShieldCheck size={12} style={{ color: "#86efac" }} />
            <span className="text-10 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.55)" }}>RERA registered</span>
          </div>
          <span className="text-10 font-mono" style={{ color: "rgba(255,255,255,0.7)" }}>{p.rera_id}</span>
        </div>
      )}
    </div>
  );
}

/* ─── NeighborhoodBlock ────────────────────────────────── */
export function NeighborhoodBlock({ title, items }) {
  return (
    <div className="space-y-2">
      {title && (
        <div className="text-10 uppercase tracking-tightest2 px-1" style={{ color: "rgba(255,255,255,0.4)" }}>{title}</div>
      )}
      {items.map((nb) => (
        <div key={nb.id} className="rounded-xl p-3 border"
          style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
          <div className="flex items-start gap-3 mb-2">
            <div className="rounded-lg flex items-center justify-center flex-shrink-0"
              style={{ width: 36, height: 36, background: ACCENT + "14" }}>
              <TreePine size={15} style={{ color: ACCENT }} />
            </div>
            <div className="flex-1">
              <div className="text-sm font-medium" style={{ color: "white" }}>{nb.name}</div>
              <div className="text-10" style={{ color: "rgba(255,255,255,0.5)" }}>{nb.city} · {nb.type}</div>
            </div>
            <span className="text-9 px-1.5 py-0.5 rounded-full font-medium"
              style={{ background: ACCENT + "1A", color: ACCENT }}>
              {nb.connectivity}
            </span>
          </div>
          <div className="text-11 leading-relaxed mb-2" style={{ color: "rgba(255,255,255,0.75)" }}>
            {nb.highlights}
          </div>
          <div className="flex items-center justify-between pt-2 border-t text-10" style={{ borderColor: "rgba(255,255,255,0.06)" }}>
            {nb.avg_price_per_sqft_sale && (
              <div>
                <span style={{ color: "rgba(255,255,255,0.4)" }}>Sale avg:</span>{" "}
                <span className="font-mono" style={{ color: "white" }}>₹{nb.avg_price_per_sqft_sale.toLocaleString("en-IN")}/sqft</span>
              </div>
            )}
            {nb.avg_rent_per_sqft && (
              <div>
                <span style={{ color: "rgba(255,255,255,0.4)" }}>Rent avg:</span>{" "}
                <span className="font-mono" style={{ color: "white" }}>₹{nb.avg_rent_per_sqft}/sqft</span>
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}

/* ─── ProjectBlock ─────────────────────────────────────── */
export function ProjectBlock({ title, items }) {
  return (
    <div className="space-y-2">
      {title && (
        <div className="text-10 uppercase tracking-tightest2 px-1" style={{ color: "rgba(255,255,255,0.4)" }}>{title}</div>
      )}
      {items.map((pr) => {
        const sold_pct = Math.round((pr.units_sold / pr.units_total) * 100);
        const ready = pr.status === "Ready to move";
        return (
          <div key={pr.id} className="rounded-xl p-3 border"
            style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
            <div className="flex items-start justify-between gap-2 mb-2">
              <div className="flex items-center gap-2 min-w-0">
                <div className="rounded-lg flex items-center justify-center flex-shrink-0"
                  style={{ width: 36, height: 36, background: ACCENT + "14" }}>
                  <Building size={15} style={{ color: ACCENT }} />
                </div>
                <div className="min-w-0">
                  <div className="text-xs font-medium truncate" style={{ color: "white" }}>{pr.name}</div>
                  <div className="text-10" style={{ color: "rgba(255,255,255,0.5)" }}>{pr.developer} · {pr.neighborhood}</div>
                </div>
              </div>
              <span className="text-9 px-1.5 py-0.5 rounded-full font-medium uppercase tracking-tightest2 flex-shrink-0"
                style={{ background: ready ? "rgba(134,239,172,0.18)" : "rgba(250,204,21,0.15)", color: ready ? "#86efac" : "#fde047" }}>
                {pr.status}
              </span>
            </div>

            <div className="grid grid-cols-3 gap-2 text-10 mb-2">
              <div>
                <div style={{ color: "rgba(255,255,255,0.4)" }}>Configs</div>
                <div style={{ color: "white" }}>{pr.configurations.join(", ")}</div>
              </div>
              <div>
                <div style={{ color: "rgba(255,255,255,0.4)" }}>From</div>
                <div className="font-mono" style={{ color: ACCENT }}>{fmtINR(pr.starting_price)}</div>
              </div>
              <div>
                <div style={{ color: "rgba(255,255,255,0.4)" }}>Completion</div>
                <div style={{ color: "white" }}>{pr.completion}</div>
              </div>
            </div>

            <div className="mb-2">
              <div className="flex items-center justify-between text-10 mb-0.5" style={{ color: "rgba(255,255,255,0.6)" }}>
                <span>Units sold</span>
                <span className="font-mono">{pr.units_sold}/{pr.units_total} · {sold_pct}%</span>
              </div>
              <div className="h-1 rounded-full overflow-hidden" style={{ background: "rgba(255,255,255,0.06)" }}>
                <div style={{ width: `${sold_pct}%`, height: "100%", background: ACCENT, borderRadius: 999 }} />
              </div>
            </div>

            {pr.highlights && (
              <div className="flex flex-wrap gap-1 mb-2">
                {pr.highlights.slice(0, 4).map((h, i) => (
                  <span key={i} className="text-9 px-1.5 py-0.5 rounded-full"
                    style={{ background: "rgba(255,255,255,0.05)", color: "rgba(255,255,255,0.6)" }}>
                    {h}
                  </span>
                ))}
              </div>
            )}

            <div className="flex items-center justify-between pt-2 border-t text-9" style={{ borderColor: "rgba(255,255,255,0.06)" }}>
              <span style={{ color: "rgba(255,255,255,0.4)" }}>RERA</span>
              <span className="font-mono" style={{ color: "#86efac" }}>{pr.rera_id}</span>
            </div>
          </div>
        );
      })}
    </div>
  );
}

/* ─── EmiBlock ─────────────────────────────────────────── */
export function EmiBlock({ property_price, down_payment, loan_amount, interest_rate, tenure_years, emi, total_interest, total_payable }) {
  return (
    <div className="rounded-xl border overflow-hidden"
      style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
      <div className="px-4 py-3 border-b flex items-center justify-between"
        style={{ borderColor: "rgba(255,255,255,0.06)", background: ACCENT + "0C" }}>
        <div className="flex items-center gap-2">
          <Wallet size={14} style={{ color: ACCENT }} />
          <span className="text-xs font-medium" style={{ color: "white" }}>Home loan EMI estimate</span>
        </div>
        <span className="text-10 font-mono" style={{ color: "rgba(255,255,255,0.55)" }}>
          {interest_rate}% · {tenure_years} yr
        </span>
      </div>

      {/* Hero EMI */}
      <div className="px-4 py-4 text-center border-b" style={{ borderColor: "rgba(255,255,255,0.06)" }}>
        <div className="text-10 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>Monthly EMI</div>
        <div className="text-2xl font-mono font-medium" style={{ color: ACCENT }}>{fmtINRFull(emi)}</div>
      </div>

      {/* Breakdown */}
      <div className="px-4 py-3 space-y-1.5 text-xs">
        <div className="flex justify-between">
          <span style={{ color: "rgba(255,255,255,0.5)" }}>Property price</span>
          <span className="font-mono" style={{ color: "rgba(255,255,255,0.9)" }}>{fmtINRFull(property_price)}</span>
        </div>
        <div className="flex justify-between">
          <span style={{ color: "rgba(255,255,255,0.5)" }}>Down payment (20%)</span>
          <span className="font-mono" style={{ color: "rgba(255,255,255,0.9)" }}>{fmtINRFull(down_payment)}</span>
        </div>
        <div className="flex justify-between">
          <span style={{ color: "rgba(255,255,255,0.5)" }}>Loan amount</span>
          <span className="font-mono" style={{ color: "rgba(255,255,255,0.9)" }}>{fmtINRFull(loan_amount)}</span>
        </div>
        <div className="flex justify-between pt-1.5 border-t" style={{ borderColor: "rgba(255,255,255,0.08)" }}>
          <span style={{ color: "rgba(255,255,255,0.5)" }}>Total interest</span>
          <span className="font-mono" style={{ color: "#fde047" }}>{fmtINRFull(total_interest)}</span>
        </div>
        <div className="flex justify-between">
          <span style={{ color: "rgba(255,255,255,0.5)" }}>Total payable</span>
          <span className="font-mono font-medium" style={{ color: "white" }}>{fmtINRFull(total_payable)}</span>
        </div>
      </div>
    </div>
  );
}

/* ─── AffordabilityBlock ───────────────────────────────── */
export function AffordabilityBlock({ monthly_income, obligations, estimated_loan, estimated_property_budget, assumptions }) {
  return (
    <div className="rounded-xl border overflow-hidden"
      style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
      <div className="px-4 py-3 border-b flex items-center gap-2"
        style={{ borderColor: "rgba(255,255,255,0.06)", background: ACCENT + "0C" }}>
        <Banknote size={14} style={{ color: ACCENT }} />
        <span className="text-xs font-medium" style={{ color: "white" }}>Affordability estimate</span>
      </div>

      <div className="px-4 py-4 text-center border-b" style={{ borderColor: "rgba(255,255,255,0.06)" }}>
        <div className="text-10 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>You can target up to</div>
        <div className="text-2xl font-mono font-medium" style={{ color: ACCENT }}>{fmtINR(estimated_property_budget)}</div>
        <div className="text-10 mt-1" style={{ color: "rgba(255,255,255,0.5)" }}>
          Loan ~{fmtINR(estimated_loan)} · Income ₹{monthly_income.toLocaleString("en-IN")}/mo
        </div>
      </div>

      <div className="px-4 py-3">
        <div className="text-10 uppercase tracking-tightest2 mb-1.5" style={{ color: "rgba(255,255,255,0.4)" }}>Assumptions</div>
        <div className="space-y-1">
          {assumptions.map((a, i) => (
            <div key={i} className="flex items-start gap-2 text-11" style={{ color: "rgba(255,255,255,0.75)" }}>
              <CheckCircle2 size={9} style={{ color: ACCENT, marginTop: 3, flexShrink: 0 }} /> {a}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

/* ─── ViewingBlock (single confirmation) ──────────────── */
export function ViewingBlock({ confirmation: c }) {
  return (
    <div className="rounded-xl p-4 border-2"
      style={{
        background: "linear-gradient(180deg, rgba(52,211,153,0.10), rgba(52,211,153,0.02))",
        borderColor: ACCENT + "44",
      }}>
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <Calendar size={15} style={{ color: ACCENT }} />
          <div className="text-sm font-medium" style={{ color: "white" }}>Viewing requested</div>
        </div>
        <span className="text-10 font-mono px-2 py-0.5 rounded-full" style={{ background: "rgba(250,204,21,0.15)", color: "#fde047" }}>
          {c.status}
        </span>
      </div>
      <div className="space-y-1.5 text-xs">
        <div className="flex justify-between gap-3">
          <span style={{ color: "rgba(255,255,255,0.5)" }}>Viewing ID</span>
          <span className="font-mono" style={{ color: ACCENT }}>{c.viewing_id}</span>
        </div>
        <div className="flex justify-between gap-3">
          <span style={{ color: "rgba(255,255,255,0.5)" }}>Property</span>
          <span className="text-right" style={{ color: "white", maxWidth: "70%" }}>{c.property_title}</span>
        </div>
        <div className="flex justify-between gap-3">
          <span style={{ color: "rgba(255,255,255,0.5)" }}>Area</span>
          <span style={{ color: "white" }}>{c.neighborhood}</span>
        </div>
        <div className="flex justify-between gap-3 pt-1.5 border-t" style={{ borderColor: "rgba(255,255,255,0.08)" }}>
          <span style={{ color: "rgba(255,255,255,0.5)" }}>Next step</span>
          <span className="text-right" style={{ color: "rgba(255,255,255,0.85)", maxWidth: "70%" }}>{c.next_step}</span>
        </div>
      </div>
    </div>
  );
}

/* ─── ViewingListBlock ─────────────────────────────────── */
export function ViewingListBlock({ items }) {
  return (
    <div className="rounded-xl p-4 border" style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
      <div className="flex items-center gap-2 mb-3">
        <Calendar size={14} style={{ color: ACCENT }} />
        <div className="text-10 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>Scheduled viewings</div>
      </div>
      <div className="space-y-2">
        {items.map((v) => {
          const confirmed = v.status.toLowerCase().includes("confirmed");
          return (
            <div key={v.id} className="px-3 py-2.5 rounded-lg" style={{ background: "rgba(255,255,255,0.02)" }}>
              <div className="flex items-center justify-between gap-2 mb-1">
                <div className="text-xs font-medium" style={{ color: "white" }}>{v.property_title}</div>
                <span className="text-9 px-1.5 py-0.5 rounded-full font-medium uppercase tracking-tightest2"
                  style={{ background: confirmed ? "rgba(134,239,172,0.18)" : "rgba(250,204,21,0.15)",
                           color: confirmed ? "#86efac" : "#fde047" }}>
                  {v.status}
                </span>
              </div>
              <div className="text-10 flex items-center gap-2" style={{ color: "rgba(255,255,255,0.6)" }}>
                <Calendar size={9} /><span>{v.scheduled}</span>
                <span style={{ color: "rgba(255,255,255,0.3)" }}>·</span>
                <User size={9} /><span>{v.agent}</span>
              </div>
              <div className="text-10 mt-1 italic" style={{ color: ACCENT }}>{v.notes}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

/* ─── SavedSearchBlock ─────────────────────────────────── */
export function SavedSearchBlock({ items }) {
  return (
    <div className="rounded-xl p-4 border" style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
      <div className="flex items-center gap-2 mb-3">
        <Star size={14} style={{ color: ACCENT }} />
        <div className="text-10 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>Saved searches</div>
      </div>
      <div className="space-y-2">
        {items.map((s) => (
          <div key={s.id} className="px-3 py-2.5 rounded-lg" style={{ background: "rgba(255,255,255,0.02)" }}>
            <div className="flex items-center justify-between gap-2 mb-1">
              <div className="text-xs" style={{ color: "white" }}>{s.label}</div>
              {s.new_matches > 0 && (
                <span className="text-9 px-1.5 py-0.5 rounded-full font-medium"
                  style={{ background: ACCENT + "22", color: ACCENT }}>
                  {s.new_matches} new
                </span>
              )}
            </div>
            <div className="flex items-center gap-2 text-10" style={{ color: "rgba(255,255,255,0.5)" }}>
              <span className="font-mono">{s.id}</span>
              <span style={{ color: "rgba(255,255,255,0.3)" }}>·</span>
              <span>{s.alerts_enabled ? "Alerts on" : "Alerts off"}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

/* ─── MarketTrendBlock ─────────────────────────────────── */
export function MarketTrendBlock({ title, neighborhoods, period }) {
  return (
    <div className="rounded-xl p-4 border" style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <BarChart3 size={14} style={{ color: ACCENT }} />
          <div className="text-10 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>{title || "Market trends"}</div>
        </div>
        <span className="text-9 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>{period}</span>
      </div>
      <div className="space-y-1">
        <div className="grid grid-cols-12 text-9 uppercase tracking-tightest2 pb-1.5 border-b"
          style={{ color: "rgba(255,255,255,0.4)", borderColor: "rgba(255,255,255,0.06)" }}>
          <div className="col-span-5">Neighborhood</div>
          <div className="col-span-4 text-right">Sale ₹/sqft</div>
          <div className="col-span-3 text-right">Rent ₹/sqft</div>
        </div>
        {neighborhoods.map((n) => (
          <div key={n.id} className="grid grid-cols-12 py-1.5 text-11 border-b"
            style={{ borderColor: "rgba(255,255,255,0.04)" }}>
            <div className="col-span-5" style={{ color: "white" }}>
              {n.name}
              <span className="text-9 ml-1" style={{ color: "rgba(255,255,255,0.4)" }}>· {n.type}</span>
            </div>
            <div className="col-span-4 text-right font-mono" style={{ color: ACCENT }}>
              {n.avg_price_per_sqft_sale ? `₹${n.avg_price_per_sqft_sale.toLocaleString("en-IN")}` : "—"}
            </div>
            <div className="col-span-3 text-right font-mono" style={{ color: "#60A5FA" }}>
              {n.avg_rent_per_sqft ? `₹${n.avg_rent_per_sqft}` : "—"}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

/* ─── CompareBlock ─────────────────────────────────────── */
export function CompareBlock({ properties, attributes }) {
  const labels = {
    price:       "Price",
    bhk:         "BHK",
    carpet_sqft: "Carpet (sqft)",
    neighborhood: "Area",
    type:        "Type",
    age_years:   "Age",
    furnishing:  "Furnishing",
    rera_id:     "RERA",
  };
  const fmtVal = (attr, p) => {
    if (attr === "price") return fmtINR(p.price);
    if (attr === "rera_id") return p.rera_id ? "✓" : "—";
    if (attr === "age_years") return p.age_years + " yr";
    return p[attr] ?? "—";
  };
  return (
    <div className="rounded-xl p-4 border" style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
      <div className="flex items-center gap-2 mb-3">
        <Layers size={14} style={{ color: ACCENT }} />
        <div className="text-10 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>Side-by-side</div>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-xs">
          <thead>
            <tr>
              <th className="text-left py-1.5 pr-3 font-medium"
                style={{ color: "rgba(255,255,255,0.4)", textTransform: "uppercase", letterSpacing: "0.1em", fontSize: 9 }}>
                Attribute
              </th>
              {properties.map((p) => (
                <th key={p.id} className="text-left py-1.5 pr-3 font-medium" style={{ color: "white" }}>
                  <div className="text-11 font-medium" style={{ color: "white" }}>{p.id}</div>
                  <div className="text-9 font-normal" style={{ color: "rgba(255,255,255,0.5)" }}>{p.neighborhood}</div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {attributes.map((attr) => (
              <tr key={attr} className="border-t" style={{ borderColor: "rgba(255,255,255,0.06)" }}>
                <td className="py-1.5 pr-3 text-11" style={{ color: "rgba(255,255,255,0.6)" }}>{labels[attr] || attr}</td>
                {properties.map((p) => (
                  <td key={p.id + attr} className="py-1.5 pr-3 font-mono text-11" style={{ color: "rgba(255,255,255,0.9)" }}>
                    {fmtVal(attr, p)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

/* ─── DocumentChecklistBlock ───────────────────────────── */
export function DocumentChecklistBlock({ purpose, items }) {
  // Group by category
  const groups = items.reduce((acc, it) => {
    (acc[it.category] = acc[it.category] || []).push(it);
    return acc;
  }, {});
  return (
    <div className="rounded-xl p-4 border" style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
      <div className="flex items-center gap-2 mb-3">
        <FileText size={14} style={{ color: ACCENT }} />
        <div className="text-10 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>
          Documents to {purpose}
        </div>
      </div>
      <div className="space-y-3">
        {Object.entries(groups).map(([cat, group]) => (
          <div key={cat}>
            <div className="text-10 mb-1.5 font-medium" style={{ color: ACCENT }}>{cat}</div>
            <div className="space-y-1.5">
              {group.map((it, i) => (
                <div key={i} className="flex items-start gap-2 text-11">
                  <div className="rounded-sm flex-shrink-0 flex items-center justify-center mt-0.5"
                    style={{ width: 12, height: 12, border: `1px solid ${it.required ? ACCENT : "rgba(255,255,255,0.2)"}`, background: it.required ? ACCENT + "22" : "transparent" }}>
                    {it.required && <CheckCircle2 size={8} style={{ color: ACCENT }} />}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div style={{ color: "rgba(255,255,255,0.9)" }}>
                      {it.name}
                      {!it.required && (
                        <span className="text-9 ml-1.5 italic" style={{ color: "rgba(255,255,255,0.4)" }}>(if applicable)</span>
                      )}
                    </div>
                    <div className="text-10 mt-0.5" style={{ color: "rgba(255,255,255,0.55)" }}>{it.note}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

/* ─── Dispatcher ───────────────────────────────────────── */
export default function Block({ block }) {
  switch (block.type) {
    case "text":               return <TextBlock {...block} />;
    case "disclaimer":         return <DisclaimerBlock {...block} />;
    case "fair_housing_alert": return <FairHousingAlertBlock {...block} />;
    case "property_list":      return <PropertyListBlock {...block} />;
    case "property_detail":    return <PropertyDetailBlock {...block} />;
    case "neighborhood":       return <NeighborhoodBlock {...block} />;
    case "project":            return <ProjectBlock {...block} />;
    case "emi":                return <EmiBlock {...block} />;
    case "affordability":      return <AffordabilityBlock {...block} />;
    case "viewing":            return <ViewingBlock {...block} />;
    case "viewing_list":       return <ViewingListBlock {...block} />;
    case "saved_search":       return <SavedSearchBlock {...block} />;
    case "market_trend":       return <MarketTrendBlock {...block} />;
    case "compare":            return <CompareBlock {...block} />;
    case "document_checklist": return <DocumentChecklistBlock {...block} />;
    default:
      return (
        <div className="text-xs px-3 py-2 rounded-md" style={{ background: "rgba(255,255,255,0.04)", color: "rgba(255,255,255,0.5)" }}>
          [Unknown block type: {block.type}]
        </div>
      );
  }
}
