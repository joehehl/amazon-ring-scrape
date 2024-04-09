from requests_html import HTMLSession
import pandas as pd

def get_reviews(url, pages=5):  # Updated to fetch from the first 5 pages
    session = HTMLSession()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    reviews = []

    for page in range(1, pages + 1):
        paginated_url = f"{url}/ref=cm_cr_arp_d_paging_btm_{page}?ie=UTF8&pageNumber={page}&reviewerType=all_reviews"
        r = session.get(paginated_url, headers=headers)
        r.html.render(sleep=1)  # May increase sleep if necessary for page content to load

        review_items = r.html.find('div[data-hook="review"]')
        for item in review_items:
            try:
                rating = item.find('i[data-hook="review-star-rating"]', first=True).text.strip()
                review_text = item.find('span[data-hook="review-body"]', first=True).text.strip()
                reviews.append({'rating': rating, 'review_text': review_text})
            except AttributeError as e:
                print(f"An attribute error occurred: {e}")
                continue

    return reviews

def main():
    start_url = 'https://www.amazon.com/Ring-Video-Doorbell-Satin-Nickel-2020-Release/product-reviews/B08N5NQ869'
    reviews = get_reviews(start_url)  # No need to specify pages here as it defaults to 5

    if reviews:
        # Convert to DataFrame
        df = pd.DataFrame(reviews)
        print(f"Extracted {len(reviews)} reviews.")

        # Writing DataFrame to an Excel file
        df.to_excel('amazon_reviews.xlsx', index=False)
        print("Data written to amazon_reviews.xlsx successfully.")
    else:
        print("No reviews were extracted, thus no Excel file was created.")

if __name__ == '__main__':
    main()

