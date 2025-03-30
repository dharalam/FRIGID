# 🧊 FRIGID: Fetching Reliable Instances of Genuine ICE Detainments
Team Name: The Three Greeks  
Team Members: Dimitrios Haralampopoulos, Ioannis Skoulidas, Sean Wyckoff

In recent months, increasing ire has been drawn upon immigrants to the United States of all kinds. Many are our neighbors, our friends, family, classmates, or coworkers. In a time when even legal migrants, permanent residents, and military veterans have a chance of being detained and held for days at a time by ICE, it becomes more and more important that people are prepared for what may come their way. With FRIGID, we aim to record incidences of ICE detainments of any kind in the state of New Jersey, and display the number and location of cases on an intuitive heatmap. We obtained this information through scraping social media sites such as Reddit, X, and Bluesky, as well as those of reputable local news sources such as News12-NJ. Aside from mapping cases, we also feel that it is important that migrants and those close to them are aware of the rights bestowed upon them by the laws of this country regardless of their immigration status. We feel that this is a project worth sustaining and investing more time into even beyond this hackathon, and would allow us to make our scope nationwide rather than solely New Jersey. We also hope that with a stronger dataset that FRIGID will become more and more useful.

## Tech Stack
Listed below are all technologies that were used to develop this project:
* ### Python
  * Flask - to create our web app
  * Polars - for data manipulation and storage
  * PRAW - to scrape Reddit data
  * Requests - to scrape everything else
  * Folium - to render our map
  * Geopy - to grab geocoords for named locations to render them on the map
  * smtplib - to create an SMTP server to send anonymous user reports via email
* ### HTML/CSS
  * Combined to structure the web components of our Flask app
* ### Google Colab
  * EDA and scraper creation
* ### Media Sources
  * #### Social Media
    * Reddit (r/newjersey)
    * X (ERO's official account)
    * Bluesky
  * #### News Outlets
    * News12-NJ
* ### Generative AI
  * A *little* help from Claude 3.7 for UI refinement

## Running FRIGID
At present, we don't have a way to host the app in the browser (we tried Vercel but it didn't want to build properly), but it is a goal of ours in the future. For the time being, running the application locally is the only way to access it. The app relies heavily on various APIs with different secret keys that would spell disaster if they were shared, so it's a bit of a pain to run locally if you're not us. Future steps include greater accessibility, however for now if you *really* want to run the app locally, the only things that you'll need are:
1. A GMail account with an App Password for the SMTP server (GMAIL="your@gmail.com")
2. The App Password associated with that account (GMAIL_PSWD="yourAppPassword")
3. (Optionally) Another email address to send the Reports to (PROTONMAIL="your_other@email.com")
These can all rather conveniently be put into a .env file and loaded with their names listed in the parentheses.
Additionally, before running locally, run:
```bash
pip install -r requirements.txt
```
This will ensure you have all the packages to run the application.
After that, you can run it from the CLI with:
```bash
python app.py #or python ./app/app.py depending on what folder you're in
```
From there you're all set to explore the app!

