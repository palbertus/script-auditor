# Ordered list of (substring, vendor_name) tuples.
# First match wins — keep more specific patterns before general ones.
VENDOR_PATTERNS = [
    # --- Google Tag Manager ---
    ("googletagmanager.com/gtm.js",             "Google Tag Manager"),
    ("googletagmanager.com/gtag/js",            "Google Tag Manager"),

    # --- Google Analytics ---
    ("google-analytics.com/analytics.js",       "Google Analytics (UA)"),
    ("google-analytics.com/ga.js",              "Google Analytics (Legacy)"),
    ("googletagmanager.com/gtag",               "Google Analytics 4 (gtag)"),

    # --- Google Ads ---
    ("googleadservices.com/pagead",             "Google Ads"),
    ("doubleclick.net",                         "Google Ads (DoubleClick)"),
    ("google.com/pagead",                       "Google Ads"),

    # --- Google Optimize ---
    ("google-analytics.com/cx/api.js",          "Google Optimize"),

    # --- Facebook / Meta ---
    ("connect.facebook.net/en_us/fbevents",     "Facebook Pixel"),
    ("connect.facebook.net",                    "Facebook / Meta SDK"),

    # --- Hotjar ---
    ("static.hotjar.com",                       "Hotjar"),
    ("script.hotjar.com",                       "Hotjar"),

    # --- Segment ---
    ("cdn.segment.com",                         "Segment"),
    ("segment.io",                              "Segment"),

    # --- HubSpot ---
    ("js.hs-scripts.com",                       "HubSpot"),
    ("js.hubspot.com",                          "HubSpot"),
    ("hubspot.com",                             "HubSpot"),

    # --- Intercom ---
    ("widget.intercom.io",                      "Intercom"),
    ("js.intercomcdn.com",                      "Intercom"),
    ("intercom.io",                             "Intercom"),

    # --- LinkedIn ---
    ("snap.licdn.com",                          "LinkedIn Insight Tag"),
    ("platform.linkedin.com",                   "LinkedIn"),

    # --- Twitter / X ---
    ("static.ads-twitter.com",                  "Twitter/X Ads Pixel"),
    ("platform.twitter.com",                    "Twitter/X Platform"),

    # --- Microsoft Clarity ---
    ("clarity.ms",                              "Microsoft Clarity"),

    # --- Heap ---
    ("cdn.heapanalytics.com",                   "Heap"),
    ("heapanalytics.com",                       "Heap"),

    # --- Mixpanel ---
    ("cdn.mxpnl.com",                           "Mixpanel"),
    ("cdn4.mxpnl.com",                          "Mixpanel"),
    ("mixpanel.com",                            "Mixpanel"),

    # --- Amplitude ---
    ("cdn.amplitude.com",                       "Amplitude"),
    ("amplitude.com",                           "Amplitude"),

    # --- FullStory ---
    ("fullstory.com/s/fs.js",                   "FullStory"),
    ("rs.fullstory.com",                        "FullStory"),
    ("edge.fullstory.com",                      "FullStory"),

    # --- Pendo ---
    ("cdn.pendo.io",                            "Pendo"),
    ("app.pendo.io",                            "Pendo"),

    # --- Drift ---
    ("js.driftt.com",                           "Drift"),
    ("cdn.drift.com",                           "Drift"),

    # --- Zendesk ---
    ("static.zdassets.com",                     "Zendesk"),
    ("ekr.zdassets.com",                        "Zendesk"),

    # --- Stripe ---
    ("js.stripe.com",                           "Stripe"),

    # --- Sentry ---
    ("browser.sentry-cdn.com",                  "Sentry"),
    ("js.sentry-cdn.com",                       "Sentry"),
    ("sentry.io",                               "Sentry"),

    # --- Datadog ---
    ("browser-intake-datadoghq.com",            "Datadog"),
    ("rum.browser-intake-datadoghq.com",        "Datadog"),
    ("datadoghq.com",                           "Datadog"),

    # --- New Relic ---
    ("js-agent.newrelic.com",                   "New Relic"),
    ("bam.nr-data.net",                         "New Relic"),

    # --- Crisp ---
    ("client.crisp.chat",                       "Crisp"),

    # --- TikTok ---
    ("analytics.tiktok.com",                    "TikTok Pixel"),

    # --- Pinterest ---
    ("s.pinimg.com",                            "Pinterest Tag"),
    ("ct.pinterest.com",                        "Pinterest Tag"),

    # --- Crazy Egg ---
    ("script.crazyegg.com",                     "Crazy Egg"),

    # --- Lucky Orange ---
    ("luckyorange.com",                         "Lucky Orange"),

    # --- Consent Management ---
    ("cdn.cookielaw.org",                       "OneTrust (CMP)"),
    ("optanon.blob.core.windows.net",           "OneTrust (CMP)"),
    ("cookie-cdn.cookiepro.com",                "OneTrust (CMP)"),
    ("consent.cookiebot.com",                   "Cookiebot (CMP)"),
    ("sdk.privacy-center.org",                  "Didomi (CMP)"),

    # --- CDN / Generic Libraries ---
    ("code.jquery.com",                         "jQuery (CDN)"),
    ("ajax.googleapis.com/ajax/libs",           "Google Hosted Libraries"),
    ("cdnjs.cloudflare.com",                    "Cloudflare CDNJS"),
    ("unpkg.com",                               "unpkg CDN"),
    ("jsdelivr.net",                            "jsDelivr CDN"),
]

# Inline script fingerprints: (content_substring, vendor_name)
_INLINE_FINGERPRINTS = [
    ("gtag(",                   "Google Analytics 4 (gtag)"),
    ("GoogleAnalyticsObject",   "Google Analytics (UA)"),
    ("fbq(",                    "Facebook Pixel"),
    ("_fbq",                    "Facebook Pixel"),
    ("hj(",                     "Hotjar"),
    ("_hsq",                    "HubSpot"),
    ("intercomSettings",        "Intercom"),
    ("Intercom(",               "Intercom"),
    ("analytics.load(",         "Segment"),
    ("amplitude.getInstance",   "Amplitude"),
    ("mixpanel.init",           "Mixpanel"),
    ("heap.load(",              "Heap"),
    ("pendo.initialize",        "Pendo"),
    ("drift.load(",             "Drift"),
    ("FS.identify",             "FullStory"),
    ("clarity(",                "Microsoft Clarity"),
    ("lintrk(",                 "LinkedIn Insight Tag"),
    ("twq(",                    "Twitter/X Ads Pixel"),
    ("ttq.load(",               "TikTok Pixel"),
    ("pintrk(",                 "Pinterest Tag"),
    ("dataLayer",               "Google Tag Manager"),
]


def lookup_vendor(url: str) -> str:
    """Return the vendor name for a script URL, or 'Unknown'."""
    lowered = url.lower()
    for pattern, vendor in VENDOR_PATTERNS:
        if pattern.lower() in lowered:
            return vendor
    return "Unknown"


def infer_vendor_from_inline(content: str) -> str:
    """Best-effort vendor detection from inline script content."""
    for fingerprint, vendor in _INLINE_FINGERPRINTS:
        if fingerprint in content:
            return vendor
    return "Unknown"
