"""Source Authority Module.

Determines the credibility and authority score of a given URL.
Official docs get 1.0, community sites get 0.65-0.75, unknown gets 0.50 default.
"""
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

AUTHORITY_SCORES = {
    # Official / High Authority (1.0)
    "docs.": 1.0,
    "developer.": 1.0,
    "reference.": 1.0,
    "api.": 1.0,
    ".edu": 1.0,
    ".gov": 1.0,
    "manual.": 1.0,
    
    # High-quality community / Code hosting (0.75)
    "github.com": 0.75,
    "gitlab.com": 0.75,
    "bitbucket.org": 0.75,
    
    # Q&A forums / General community (0.65)
    "stackoverflow.com": 0.65,
    "stackexchange.com": 0.65,
    "dev.to": 0.65,
    
    # Blogs / Social forums (0.60)
    "medium.com": 0.60,
    "reddit.com": 0.60,
}

def get_authority(url: str) -> float:
    """Return the authority score for a given URL (0.0 to 1.0)."""
    if not url:
        return 0.50

    try:
        domain = urlparse(url).netloc.lower()
        if not domain:
            # If netloc is empty, maybe the URL is missing the scheme (e.g. 'stackoverflow.com/questions')
            domain = url.split('/')[0].lower()
    except Exception as e:
        logger.debug(f"Failed to parse URL '{url}' for authority check: {e}")
        return 0.50

    # Prefix/Suffix matching for subdomains like docs.python.org
    for key, score in AUTHORITY_SCORES.items():
        if key in domain:
            return score

    return 0.50
