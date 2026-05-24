"""
cite process to convert sources and metasources into full citations
"""

import re
import traceback
import yaml
from importlib import import_module
from pathlib import Path
from dotenv import load_dotenv
from util import *


# load environment variables
load_dotenv()


# load member names and aliases for author normalization
name_mappings = {}
for member_file in Path("_members").glob("*.md"):
    try:
        content = member_file.read_text(encoding="utf-8")
        fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
        if fm_match:
            fm_data = yaml.safe_load(fm_match.group(1))
            name = fm_data.get("name")
            aliases = fm_data.get("aliases", [])
            if name:
                name_mappings[name.lower()] = name
                for alias in aliases:
                    name_mappings[alias.lower()] = name
                    # Also map stripped versions without dots or spaces
                    normalized_alias = re.sub(r"[^a-z]", "", alias.lower())
                    name_mappings[normalized_alias] = name
    except Exception as e:
        log(f"Error parsing member file {member_file.name}: {e}", level="WARNING")


# save errors/warnings for reporting at end
errors = []
warnings = []

# output citations file
output_file = "_data/citations.yaml"


def normalize_title(title):
    """
    normalize title for comparison (lowercase, alphanumeric only, collapse spaces)
    """
    if not title:
        return ""
    # remove non-alphanumeric characters, convert to lowercase, and collapse whitespace
    title = re.sub(r"[^a-zA-Z0-9]", " ", title.lower())
    return " ".join(title.split())


def merge_citations(base, secondary):
    """
    merge two citation dicts, non-empty values from secondary override base
    """
    for key, value in secondary.items():
        if key == "id":
            # prioritize standard IDs (doi, pmcode, arxiv, etc.) over Google Scholar IDs
            base_id = str(base.get("id", ""))
            sec_id = str(value)
            
            base_is_standard = base_id.startswith("doi:") or base_id.startswith("pmid:") or base_id.startswith("arxiv:")
            sec_is_standard = sec_id.startswith("doi:") or sec_id.startswith("pmid:") or sec_id.startswith("arxiv:")
            
            if sec_is_standard and not base_is_standard:
                base["id"] = sec_id
            elif not sec_is_standard and base_is_standard:
                # keep base_id
                pass
            elif len(sec_id) > len(base_id):
                # fallback to length-based merge
                base["id"] = sec_id
            continue

        # if secondary has a value and base doesn't, or secondary value is longer/better
        if value and (not base.get(key) or len(str(value)) > len(str(base.get(key)))):
            base[key] = value
    return base


log()

log("Compiling sources")

# compiled list of sources
sources = []

# in-order list of plugins to run
plugins = ["google-scholar", "pubmed", "orcid", "sources"]

# loop through plugins
for plugin in plugins:
    # convert into path object
    plugin = Path(f"plugins/{plugin}.py")

    log(f"Running {plugin.stem} plugin")

    # get all data files to process with current plugin
    files = Path.cwd().glob(f"_data/{plugin.stem}*.*")
    files = list(filter(lambda p: p.suffix in [".yaml", ".yml", ".json"], files))

    log(f"Found {len(files)} {plugin.stem}* data file(s)", indent=1)

    # loop through data files
    for file in files:
        log(f"Processing data file {file.name}", indent=1)

        # load data from file
        try:
            data = load_data(file)
            # check if file in correct format
            if not list_of_dicts(data):
                raise Exception(f"{file.name} data file not a list of dicts")
        except Exception as e:
            log(e, indent=2, level="ERROR")
            errors.append(e)
            continue

        # loop through data entries
        for index, entry in enumerate(data):
            log(f"Processing entry {index + 1} of {len(data)}, {label(entry)}", level=2)

            # run plugin on data entry to expand into multiple sources
            try:
                expanded = import_module(f"plugins.{plugin.stem}").main(entry)
                # check that plugin returned correct format
                if not list_of_dicts(expanded):
                    raise Exception(f"{plugin.stem} plugin didn't return list of dicts")
            # catch any plugin error
            except Exception as e:
                # log detailed pre-formatted/colored trace
                print(traceback.format_exc())
                # log high-level error
                log(e, indent=3, level="ERROR")
                errors.append(e)
                continue

            # loop through sources
            for source in expanded:
                if plugin.stem != "sources":
                    log(label(source), level=3)

                # include meta info about source
                source["plugin"] = plugin.name
                source["file"] = file.name

                # add source to compiled list
                sources.append(source)

            if plugin.stem != "sources":
                log(f"{len(expanded)} source(s)", indent=3)


log("Merging sources by id")

# merge sources with matching (non-blank) ids (case-insensitive)
for a in range(0, len(sources)):
    a_id = str(get_safe(sources, f"{a}.id", "")).strip()
    if not a_id:
        continue
    for b in range(a + 1, len(sources)):
        b_id = str(get_safe(sources, f"{b}.id", "")).strip()
        if b_id.lower() == a_id.lower():
            log(f"Found duplicate {b_id} (matches {a_id})", indent=2)
            sources[a].update(sources[b])
            sources[b] = {}
sources = [entry for entry in sources if entry]


# filter out preprints not explicitly included in sources.yaml
log("Filtering preprints (opt-in only)")
filtered_sources = []
for source in sources:
    citation_id = str(get_safe(source, "id", "")).lower()
    publisher_lower = str(get_safe(source, "publisher", "")).lower()
    # detect various preprint identifiers
    is_preprint = (
        any(p in citation_id for p in ["arxiv", "chemrxiv", "rs.3.rs"]) or
        any(p in publisher_lower for p in ["arxiv", "chemrxiv", "biorxiv", "medrxiv", "research square"])
    )
    is_from_sources = get_safe(source, "plugin", "") == "sources.py"

    if is_preprint and not is_from_sources:
        log(f"Removing preprint {citation_id} (not in sources.yaml)", indent=2)
        continue

    filtered_sources.append(source)
sources = filtered_sources


log(f"{len(sources)} total source(s) to cite")


log()

log("Generating citations")

# list of new citations
citations = []


# loop through compiled sources
for index, source in enumerate(sources):
    log(f"Processing source {index + 1} of {len(sources)}, {label(source)}")

    # if explicitly flagged, remove/ignore entry
    if get_safe(source, "remove", False) == True:
        continue

    # new citation data for source
    citation = {}

    # source id
    _id = get_safe(source, "id", "").strip()

    # manubot doesn't work without an id
    if _id:
        log("Using Manubot to generate citation", indent=1)

        try:
            # run manubot and set citation
            citation = cite_with_manubot(_id)

        # if manubot cannot cite source
        except Exception as e:
            plugin = get_safe(source, "plugin", "")
            file = get_safe(source, "file", "")
            # if regular source (id entered by user), throw error
            if plugin == "sources.py":
                log(e, indent=3, level="ERROR")
                errors.append(f"Manubot could not generate citation for source {_id}")
            # otherwise, if from metasource (id retrieved from some third-party api), just warn
            else:
                log(e, indent=3, level="WARNING")
                warnings.append(
                    f"Manubot could not generate citation for source {_id} (from {file} with {plugin})"
                )
                # fall back to metadata retrieved by the plugin instead of discarding it
                citation = {}

    # preserve fields from input source, overriding existing fields
    citation.update(source)

    # ensure date in proper format for correct date sorting
    if get_safe(citation, "date", ""):
        citation["date"] = format_date(get_safe(citation, "date", ""))

    # normalize author names based on member files
    normalized_authors = []
    for author in get_safe(citation, "authors", []):
        author_cleaned = author.strip()
        author_lower = author_cleaned.lower()
        author_no_dots = author_lower.replace(".", "")
        author_no_spaces = re.sub(r"[^a-z]", "", author_lower)
        
        if author_lower in name_mappings:
            normalized_authors.append(name_mappings[author_lower])
        elif author_no_dots in name_mappings:
            normalized_authors.append(name_mappings[author_no_dots])
        elif author_no_spaces in name_mappings:
            normalized_authors.append(name_mappings[author_no_spaces])
        else:
            normalized_authors.append(author_cleaned)
    if normalized_authors:
        citation["authors"] = normalized_authors

    # determine type of citation
    citation_id = str(get_safe(citation, "id", "")).lower()
    publisher = str(get_safe(citation, "publisher", "")).lower()
    
    is_preprint = (
        any(p in citation_id for p in ["arxiv", "chemrxiv", "rs.3.rs"]) or
        any(p in publisher for p in ["arxiv", "chemrxiv", "biorxiv", "medrxiv", "research square"])
    )
    
    if "patent" in publisher or "patent" in citation_id:
        citation["type"] = "patent"
    elif is_preprint:
        citation["type"] = "preprint"
    else:
        citation["type"] = "paper"

    # add new citation to list
    citations.append(citation)


log()

log("Merging duplicate citations by title (removing preprint versions)")

# merge citations with matching titles, keeping published version over preprint
# use a dictionary to group by normalized title
title_groups = {}
for citation in citations:
    title = get_safe(citation, "title", "").strip()
    norm_title = normalize_title(title)
    if not norm_title:
        continue
    if norm_title not in title_groups:
        title_groups[norm_title] = []
    title_groups[norm_title].append(citation)

# process each group
merged_citations = []
removed_ids = set()

for norm_title, group in title_groups.items():
    if len(group) == 1:
        # no duplicates, keep as is
        merged_citations.append(group[0])
        continue

    # find published and preprint versions
    published = []
    preprints = []

    for citation in group:
        citation_id = get_safe(citation, "id", "")
        if not citation_id:
            continue
        publisher_lower = str(get_safe(citation, "publisher", "")).lower()
        is_preprint = (
            "chemrxiv" in citation_id.lower() or
            "arxiv" in citation_id.lower() or
            "chemrxiv" in publisher_lower or
            "arxiv" in publisher_lower or
            "biorxiv" in publisher_lower or
            "medrxiv" in publisher_lower or
            "research square" in publisher_lower
        )

        if is_preprint:
            preprints.append(citation)
        else:
            published.append(citation)

    # if there are published versions, merge them and discard preprints
    if published:
        # start with the first published version
        merged = published[0]
        for other in published[1:]:
            merged = merge_citations(merged, other)

        merged_citations.append(merged)

        # log removals
        for prep in preprints:
            prep_id = get_safe(prep, "id", "")
            log(f"Removing preprint {prep_id}, keeping published version(s)", indent=1)
            removed_ids.add(prep_id)
        for pub in published[1:]:
            pub_id = get_safe(pub, "id", "")
            log(f"Merged duplicate published version {pub_id}", indent=1)
            removed_ids.add(pub_id)

    # if only preprints, merge them
    elif preprints:
        log(
            f"Only preprint versions found for title, merging {len(preprints)} versions",
            indent=1,
        )
        merged = preprints[0]
        for other in preprints[1:]:
            merged = merge_citations(merged, other)
            removed_ids.add(get_safe(other, "id", ""))
        merged_citations.append(merged)

# also add citations without titles (shouldn't happen, but just in case)
for citation in citations:
    title = get_safe(citation, "title", "").strip()
    norm_title = normalize_title(title)
    citation_id = get_safe(citation, "id", "")
    if not norm_title and citation_id and citation_id not in removed_ids:
        merged_citations.append(citation)

citations = merged_citations


log()

log("Saving updated citations")


# save new citations
try:
    save_data(output_file, citations)
except Exception as e:
    log(e, level="ERROR")
    errors.append(e)


log()


# exit at end, so user can see all errors/warnings in one run
if len(warnings):
    log(f"{len(warnings)} warning(s) occurred above", level="WARNING")
    for warning in warnings:
        log(warning, indent=1, level="WARNING")

if len(errors):
    log(f"{len(errors)} error(s) occurred above", level="ERROR")
    for error in errors:
        log(error, indent=1, level="ERROR")
    log()
    # non-fatal errors (like plugin failures due to missing keys) shouldn't block the whole process
    # we exit with 0 to allow the rest of the workflow (like git commit) to proceed
    exit(0)

else:
    log("All done!", level="SUCCESS")

log()
