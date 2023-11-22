import json
import logging

import wikipediaapi


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('WikipediaFetcher')


visited_pages = set()  # To keep track of visited pages
counter = 0  # To keep track of number of requests


def get_page_content(page_title, depth, max_depth):
    wiki_wiki = wikipediaapi.Wikipedia('MyCheeseRAGApp/1.0 (myemail@example.com)')
    if depth > max_depth or page_title in visited_pages:
        return [], []
    visited_pages.add(page_title)

    if len(visited_pages) % 10 == 0:
        logger.info(f"Visited pages: {len(visited_pages)}")
        logger.info(f"Fetching page '{page_title}' (depth={depth})")

    try:
        page = wiki_wiki.page(page_title)
        if not page.exists():
            return [], []

        texts, metadata = [], []
        if len(texts) % 100:
            logger.info(f"Texts length {len(texts)}")

        # Add page summary
        texts.append(page.summary)
        metadata.append({'title': page_title, 'section': 'Summary', 'url': page.fullurl})

        # Add sections
        for section in page.sections:
            texts.append(section.text)
            metadata.append({'title': page_title, 'section': section.title, 'url': page.fullurl})

        # Recursive fetching for links
        if depth < max_depth:
            for link_title in page.links:
                # time.sleep(1)  # Delay to respect Wikipedia's API rate limit
                link_texts, link_metadata = get_page_content(link_title, depth + 1, max_depth)
                if len(link_texts) > 0:
                    texts.extend(link_texts)
                    metadata.extend(link_metadata)

        return texts, metadata
    except Exception as e:
        logger.error(f"Error fetching page '{page_title}': {e}")
        return [], []


## EXTRACT ##

# Starting with the 'List of cheeses' page
texts_list, metadata_list = get_page_content('List of cheeses', 0, 2)

texts = []
metadata = []
# Remove empty content
for text in texts_list:
    if text != '':
        texts.append(text)
        metadata.append(metadata_list[texts_list.index(text)])

# Save to files
with open('texts.json', 'w') as f:
    f.write(json.dumps(texts))
with open('metadata.json', 'w') as f:
    f.write(json.dumps(metadata))

