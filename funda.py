from funda_scraper import FundaScraper
import numpy as np
import asyncio
import telegram

telegram_token = "REDACTED"
new_url = ""

async def main():
    bot = telegram.Bot(telegram_token)
    async with bot:
        await bot.send_message(text='New listing! ' + new_url, chat_id=-000000000) # Redacted chat_id too
        # Only necessary during bot setup
        # updates = (await bot.get_updates())[0]
        # print(updates)

if __name__ == '__main__':
    scraper_links = []
    areas = ["utrecht"]

    # Funda scraper
    for desired_area in areas:
        # Set the desired price and an arbitrary high number of pages
        scraper = FundaScraper(area=desired_area, want_to="rent", find_past=False, n_pages=100, max_price=1300)
        df = scraper.run(raw_data=True)
        df.head()

        scraper_links = scraper_links + scraper.links

    # Load previously found URLs
    urls = np.loadtxt('/home/pi/funda/data.npy', dtype='str')

    # Determine whether found URLs are new or not
    for url in scraper_links:
        if url in urls:
            print("Not new: " + url)
        else:
            print("New listing! " + url)
            new_url = url
            asyncio.run(main())

    # Overwrite found URLs
    np.savetxt('/home/pi/funda/data.npy', scraper.links, fmt="%s", newline="\n") 
