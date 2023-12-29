import requests
import xml.etree.ElementTree as ET
import json

# Function to fetch scientific papers from Arxiv.org
def fetch_papers(query, max_results=10):
    # Format the query for the Arxiv API by replacing spaces with '+AND+'
    query = '+AND+'.join(query.split())
    # Create the URL for the Arxiv API request
    url = f'http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={max_results}'
    print(f"Request URL: {url}")  # Diagnostic print to show the request URL

    response = requests.get(url)

    # Check if the response status code is not 200 (OK)
    if response.status_code != 200:
        print(f"Failed to retrieve data, Status Code: {response.status_code}")
        return []

    try:
        # Parse the XML response content using ElementTree
        root = ET.fromstring(response.content)
        papers = []

        # Iterate through each 'entry' element in the XML
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            # Extract title, summary, and link information from each entry
            title = entry.find('{http://www.w3.org/2005/Atom}title').text
            summary = entry.find('{http://www.w3.org/2005/Atom}summary').text
            link = entry.find('{http://www.w3.org/2005/Atom}id').text

            # Append the extracted data to the 'papers' list as a dictionary
            papers.append({
                'title': title.strip(),
                'summary': summary.strip(),
                'link': link.strip()
            })

    except ET.ParseError as e:
        print("Error parsing XML:", e)
        return []

    return papers

# Fetch scientific papers related to the query 'llama'
papers = fetch_papers('llama')
if papers:
    for paper in papers:
        # Print the title, summary, and link of each paper
        print(f"Title: {paper['title']}\nSummary: {paper['summary']}\nLink: {paper['link']}\n")
else:
    print("No papers found for the query.")

# Function to process and structure the fetched papers data
def process_papers(papers):
    processed_data = []

    for paper in papers:
    # Append each paper's title, summary, and link to the 'processed_data' list
        processed_data.append({
            'title': paper['title'],
            'summary': paper['summary'],
            'link': paper['link']
        })

    return processed_data

# Function to save the processed papers data to a JSON file
def save_to_json(data, filename='data/papers_data.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        # Write the structured data to the JSON file with proper formatting
        json.dump(data, f, ensure_ascii=False, indent=4)

# Process and structure the fetched papers data
processed_papers = process_papers(papers)

# Save the processed data to a JSON file named 'papers_data.json'
save_to_json(processed_papers)

print("Papers data saved to JSON file.")