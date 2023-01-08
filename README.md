# BearHacks
# BearHacks - Being Careless, Machine Learning style.


### Inspiration

After being utterly confused by the prerequisites and corequisites of our University of Alberta courses, we decided to go down a nihilistic spiral and leave our fate to Machine Learning and Reddit.

**Perfect Plan.**

### What it does

**BearHacks**, like the name suggests, is truly a hacker's Beartracks. It eliminates the tedious task of planning your future and generates a degree plan for you by balancing tough, mandatory courses with easy electives to make sure you can spend your time at university exactly how you wanted to - **PARTYING**.

### How we built it

BearHacks uses a combination of Machine Learning and Web Scraping to gather data for all university of Alberta courses, and runs a sentiment analysis algorithm on all Reddit posts about them. Based on this analysis it creates a degree plan that ensures a stable difficulty across every semester while accounting for prerequisites and corequisites. 

### Challenges we ran into

- Due to the slow Reddit API, building a detailed analysis of every course's sentiment would take more time than we had to spare. So we had to limit the number of comments analyzed, reducing the accuracy of the analysis.

- Having access to the USRI surveys without extensive authentication, or having an API would greatly increase the accuracy of the data but due to the time limit, would not be feasible.

- The function for balancing per-term difficulty is essentially a brute-force method. Thus it needs to be limited to an extremely small fraction of the total dataset for the code to work at all.

### Accomplishments that we're proud of

- Sorting through the entirely textual prerequisite and corequisite course requirements from the university catalogue to make it consistent and readable in a JSON format was an unforeseen challenge that took a lot of **RegEx** work and hours of frustration. We were helped greatly by a GitHub repo by user _abenezerBelachewthat_ who had partially compiled most of the basic information from the university catalogue.

- The other major challenge was using a sentiment analysis algorithm on comments searched through the sluggish Reddit API while ignoring random references to the target course that did not necessarily contribute to its sentiment rating.

### What we learned

- As our first hackathon, we were admittedly in over our heads, but we also wanted to win. So we learned Flask, Jinja2 and CSS to make a usable front-end.
- We also had to learn web scraping and working with _JSON_ files to make our database. We had to use several libraries unknown to us such as  _pmaw_, _spacy_, _textblob_ . 

### What's next for BearHacks
Even though it started as a joke meant to take slacking to ridiculous proportions, BearHacks truly has potential. Assessing the difficulty of courses using Machine Learning is something that shows promise even in this extremely primitive stage.

We will continue to work on BearHacks to transform it from a party trick to an actual tool that can help students like ourselves.
