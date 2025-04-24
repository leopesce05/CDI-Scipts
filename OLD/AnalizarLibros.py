import pandas as pd
import re

# Time Magazine Top 100 Novels list
time_magazine_top_100_novels = [
    "To Kill a Mockingbird",
    "1984",
    "The Lord of the Rings",
    "The Catcher in the Rye",
    "The Great Gatsby",
    "The Lion, the Witch and the Wardrobe",
    "Lord of the Flies",
    "Animal Farm",
    "Catch-22",
    "The Grapes of Wrath",
    "Go Tell It on the Mountain",
    "The Heart of the Matter",
    "A Dance to the Music of Time",
    "Invisible Man",
    "The Golden Notebook",
    "Lord of the Rings",
    "The Catcher in the Rye",
    "Beloved",
    "The Sun Also Rises",
    "Wide Sargasso Sea",
    "Under the Net",
    "The French Lieutenant's Woman",
    "Atonement",
    "The Prime of Miss Jean Brodie",
    "On the Road",
    "The Golden Notebook",
    "The Big Sleep",
    "A House for Mr Biswas",
    "The Spy Who Came in from the Cold",
    "The Catcher in the Rye",
    "A Clockwork Orange",
    "White Teeth",
    "The Painted Bird",
    "American Pastoral",
    "The Sound and the Fury",
    "The Blind Assassin",
    "Portnoy's Complaint",
    "The Crying of Lot 49",
    "The Corrections",
    "The Recognitions",
    "The Heart Is a Lonely Hunter",
    "Herzog",
    "Housekeeping",
    "A Passage to India",
    "The Death of the Heart",
    "The Moviegoer",
    "A Bend in the River",
    "Blood Meridian",
    "Possession",
    "Loving",
    "Midnight's Children",
    "The Man Who Loved Children",
    "The Sot-Weed Factor",
    "The Sheltering Sky",
    "An American Tragedy",
    "The Assistant",
    "Call It Sleep",
    "The Berlin Stories",
    "The Bridge of San Luis Rey",
    "The Confessions of Nat Turner",
    "The Day of the Locust",
    "Death Comes for the Archbishop",
    "Deliverance",
    "Dog Soldiers",
    "Falconer",
    "A Farewell to Arms",
    "The First Circle",
    "Franny and Zooey",
    "Gravity's Rainbow",
    "The Handmaid's Tale",
    "A High Wind in Jamaica",
    "If on a Winter's Night a Traveler",
    "Light in August",
    "Lucky Jim",
    "The Maltese Falcon",
    "Money",
    "Mrs. Dalloway",
    "Native Son",
    "Neuromancer",
    "Never Let Me Go",
    "1984",
    "One Flew Over the Cuckoo's Nest",
    "Pale Fire",
    "Play It As It Lays",
    "Rabbit, Run",
    "Ragtime",
    "Red Harvest",
    "Revolutionary Road",
    "Slaughterhouse-Five",
    "Snow Crash",
    "The Sot-Weed Factor",
    "The Sound and the Fury",
    "The Sportswriter",
    "The Spy Who Came in from the Cold",
    "The Sun Also Rises",
    "Their Eyes Were Watching God",
    "Things Fall Apart",
    "To the Lighthouse",
    "Tropic of Cancer",
    "Ubik",
    "Under the Volcano",
    "Watchmen",
    "White Noise"
]

def normalize_title(title):
    # Convert to lowercase and remove special characters
    return re.sub(r'[^\w\s]', '', title.lower())

# Read the CSV file
df = pd.read_csv('integrated_books.csv')

# Get total number of books in database
total_books = len(df)

# Normalize titles in both lists
time_magazine_normalized = [normalize_title(title) for title in time_magazine_top_100_novels]
database_titles_normalized = [normalize_title(title) for title in df['title'].astype(str)]

# Find matches
matches = []
for time_title in time_magazine_normalized:
    for db_title in database_titles_normalized:
        if time_title in db_title or db_title in time_title:
            matches.append(time_title)
            break

# Calculate percentages
percentage_of_time_list = (len(matches) / len(time_magazine_top_100_novels)) * 100
percentage_of_database = (len(matches) / total_books) * 100

print(f"Total number of books in database: {total_books}")
print(f"Number of Time Magazine Top 100 Novels found in database: {len(matches)}")
print(f"Percentage of Time Magazine Top 100 Novels in database: {percentage_of_time_list:.2f}%")
print(f"Percentage of total database that are Time Magazine Top 100 Novels: {percentage_of_database:.2f}%")

if percentage_of_database < 20:
    print("\n⚠️ Warning: The Time Magazine Top 100 Novels represent less than 20% of your database.")
    print(f"You need to add approximately {int((0.20 * total_books) - len(matches))} more books from the list to reach 20%.")
else:
    print("\n✅ Your database meets the requirement of having at least 20% Time Magazine Top 100 Novels.")

print("\nMatching books:")
for match in matches:
    original_title = time_magazine_top_100_novels[time_magazine_normalized.index(match)]
    print(f"- {original_title}") 