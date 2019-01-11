def create_page_scraper(scraping_function):
    def scrape_pages(search_term, amount):
        results = []
        page = 1
        while len(results) < amount:
            new_quotes = scraping_function(search_term, page)
            if not new_quotes:
                break
            results.extend(new_quotes)
            page += 1

        return results[0:amount]

    return scrape_pages
