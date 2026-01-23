# Session Log: SEO Optimization in Page Specifications

**Date:** 2026-01-20  
**Topic:** SEO Requirements for Page Specifications  
**Status:** Planned for Future Implementation  
**Target Project:** Car Mechanics Website (SEO-critical project)

---

## Context

During Dog Week specification audit work, identified that WDS methodology lacks SEO optimization requirements in page specifications. This is a critical gap for projects where organic search traffic is important.

**Decision:** Defer SEO implementation to next project (car mechanics website) where SEO is business-critical, allowing real-world validation of requirements.

---

## Proposed SEO Section for Page Specification Template

### SEO Optimization

#### Page Metadata
- **Page Title:** `{55-60 character title with primary keyword}`
- **Meta Description:** `{150-160 character description with call-to-action}`
- **Canonical URL:** `{canonical URL to prevent duplicate content}`
- **Language/Region:** `{hreflang tags for multi-language sites}`

#### Open Graph (Social Sharing)
- **og:title:** `{Social media title}`
- **og:description:** `{Social media description}`
- **og:image:** `{1200x630px image URL}`
- **og:type:** `{website/article/product}`
- **og:url:** `{Canonical URL}`

#### Twitter Card
- **twitter:card:** `{summary_large_image/summary}`
- **twitter:title:** `{Twitter-specific title}`
- **twitter:description:** `{Twitter-specific description}`
- **twitter:image:** `{Image URL}`

#### Structured Data (Schema.org)
- **Schema Type:** `{Organization/LocalBusiness/Product/Article/etc.}`
- **JSON-LD:** `{Structured data markup}`
- **Key Properties:** `{name, address, phone, hours, ratings, etc.}`

#### Content SEO
- **Primary Keyword:** `{Main target keyword}`
- **Secondary Keywords:** `{2-3 related keywords}`
- **Heading Structure:** `{H1 contains primary keyword, H2s contain variations}`
- **Keyword Density:** `{Natural placement, avoid keyword stuffing}`
- **Internal Links:** `{Links to related pages with descriptive anchor text}`
- **External Links:** `{Authoritative sources where relevant}`

#### Technical SEO
- **URL Structure:** `{Clean, descriptive URLs with keywords}`
- **Mobile-Friendly:** `{Responsive design, mobile-first indexing}`
- **Page Speed:** `{Target load time < 3 seconds}`
- **Image Optimization:** `{Compressed images with descriptive filenames}`
- **Robots Meta:** `{index,follow / noindex,nofollow}`
- **Sitemap:** `{Include in XML sitemap}`

#### Local SEO (if applicable)
- **NAP Consistency:** `{Name, Address, Phone consistent across web}`
- **Google Business Profile:** `{Integration requirements}`
- **Local Schema:** `{LocalBusiness structured data}`
- **Location Keywords:** `{City/region in content}`

---

## Implementation Checklist

When adding SEO to WDS:

- [ ] Add SEO section to `page-specification.template.md`
- [ ] Create SEO micro-guide for Freya (`data/agent-guides/freya/seo-optimization.md`)
- [ ] Add SEO validation to specification audit workflow
- [ ] Update specification quality checklist with SEO items
- [ ] Create SEO component specifications (meta tags, structured data)
- [ ] Document SEO testing procedures
- [ ] Add SEO to development checklist

---

## SEO Audit Criteria (Level 6)

**Page-Level SEO Checks:**
- [ ] Page title unique and optimized (55-60 chars)
- [ ] Meta description compelling and optimized (150-160 chars)
- [ ] Canonical URL defined
- [ ] Open Graph tags complete
- [ ] Twitter Card tags complete
- [ ] Structured data/Schema.org markup present
- [ ] Primary keyword identified and placed in H1
- [ ] Heading hierarchy logical (H1 → H2 → H3)
- [ ] Image alt text descriptive and keyword-rich
- [ ] URL structure clean and keyword-optimized
- [ ] Internal linking strategy documented
- [ ] Mobile-responsive design specified
- [ ] Page speed requirements defined

**Site-Level SEO Checks:**
- [ ] XML sitemap inclusion
- [ ] Robots.txt configuration
- [ ] 404 page design
- [ ] Redirect strategy (301/302)
- [ ] HTTPS/SSL requirements
- [ ] Breadcrumb navigation
- [ ] Pagination handling (rel=prev/next)

---

## Example: Car Mechanics Page SEO Specification

### Landing Page: "Bilverkstad i Stockholm"

**Page Title:** "Bilverkstad Stockholm | Professionell Bilservice & Reparation"  
**Meta Description:** "Erfaren bilverkstad i Stockholm. Snabb service, konkurrenskraftiga priser. Boka tid online idag! ⭐⭐⭐⭐⭐"

**Primary Keyword:** "bilverkstad stockholm"  
**Secondary Keywords:** "bilservice stockholm", "bilreparation stockholm", "bilmekaniker stockholm"

**Schema.org Type:** LocalBusiness + AutomotiveBusiness

```json
{
  "@context": "https://schema.org",
  "@type": "AutomotiveBusiness",
  "name": "Stockholm Bilverkstad AB",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Verkstadsgatan 15",
    "addressLocality": "Stockholm",
    "postalCode": "123 45",
    "addressCountry": "SE"
  },
  "telephone": "+46-8-123-4567",
  "openingHours": "Mo-Fr 08:00-17:00",
  "priceRange": "$$",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "reviewCount": "127"
  }
}
```

---

## Resources for Future Implementation

**SEO Best Practices:**
- Google Search Central Documentation
- Schema.org Vocabulary
- Open Graph Protocol
- Twitter Card Validator
- Google Rich Results Test
- Lighthouse SEO Audit

**Tools for Testing:**
- Google Search Console
- Screaming Frog SEO Spider
- Ahrefs/SEMrush
- PageSpeed Insights
- Mobile-Friendly Test

---

## Next Steps (When Implementing)

1. **Research Phase**
   - Study car mechanics industry SEO best practices
   - Analyze competitor SEO strategies
   - Identify high-value keywords
   - Map keyword intent to page types

2. **Template Phase**
   - Add SEO section to page specification template
   - Create SEO micro-guide for Freya
   - Define SEO validation criteria

3. **Implementation Phase**
   - Apply SEO specs to car mechanics pages
   - Test with real content and keywords
   - Validate with SEO tools
   - Measure results and iterate

4. **Integration Phase**
   - Add SEO to specification audit workflow
   - Update quality checklists
   - Document lessons learned
   - Refine for general WDS use

---

## Notes

- SEO requirements vary significantly by industry and project goals
- Local SEO critical for service businesses (car mechanics, restaurants, etc.)
- E-commerce requires product schema and different optimization
- Blog/content sites need article schema and content SEO focus
- B2B sites may prioritize different keywords and conversion paths

**Recommendation:** Build SEO framework with car mechanics project, then generalize for WDS methodology.

---

**Status:** Documented for future implementation  
**Next Review:** When starting car mechanics website project  
**Owner:** Freya WDS Designer Agent (with SEO micro-guide)
