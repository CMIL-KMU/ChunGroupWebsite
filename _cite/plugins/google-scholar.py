import os
from serpapi import GoogleSearch
from util import *


def main(entry):
    """
    receives single list entry from google-scholar data file
    returns list of sources to cite
    """

    # get id from entry
    _id = get_safe(entry, "gsid", "")
    if not _id:
        raise Exception('No "gsid" key')

    # query api
    @log_cache
    @cache.memoize(name=__file__, expire=1 * (60 * 60 * 24))
    def query(_id):
        api_key = os.environ.get("GOOGLE_SCHOLAR_API_KEY", "")
        if not api_key:
            raise Exception('No "GOOGLE_SCHOLAR_API_KEY" env var')
            
        params = {
            "engine": "google_scholar_author",
            "api_key": api_key,
            "num": 100,  # max allowed
            "author_id": _id,
        }
        return get_safe(GoogleSearch(params).get_dict(), "articles", [])

    try:
        response = query(_id)
    except Exception as e:
        log(f"Google Scholar fetch failed: {e}. Attempting fallback to existing citations.", level="WARNING")
        
        fallback_citations = []
        try:
            import yaml
            with open("_data/citations.yaml", "r", encoding="utf-8") as f:
                existing_data = yaml.safe_load(f)
                if isinstance(existing_data, list):
                    for cit in existing_data:
                        if cit.get("plugin") == "google-scholar.py" and cit.get("gsid") == _id:
                            # Strip out plugin/file properties that cite.py will re-append
                            cit_clean = cit.copy()
                            cit_clean.pop("plugin", None)
                            cit_clean.pop("file", None)
                            fallback_citations.append(cit_clean)
        except Exception as fallback_err:
            log(f"Failed to load fallback citations: {fallback_err}", level="WARNING")
            
        if fallback_citations:
            log(f"Successfully loaded {len(fallback_citations)} Google Scholar citation(s) from local fallback.", level="SUCCESS")
            return fallback_citations
        else:
            raise e

    # list of sources to return
    sources = []

    # go through response and format sources
    for work in response:
        # create source
        year = get_safe(work, "year", "")
        source = {
            "id": get_safe(work, "citation_id", ""),
            # api does not provide Manubot-citeable id, so keep citation details
            "title": get_safe(work, "title", ""),
            "authors": list(map(str.strip, get_safe(work, "authors", "").split(","))),
            "publisher": get_safe(work, "publication", ""),
            "date": (year + "-01-01") if year else "",
            "link": get_safe(work, "link", ""),
        }

        # copy fields from entry to source
        source.update(entry)

        # add source to list
        sources.append(source)

    return sources
