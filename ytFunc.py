from pytube import YouTube
import google.generativeai as genai
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
CREDS_FILE = r'C:\Users\domin\python-projects\credentials.json'
creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1Gte1GiYPhLlvJVtfkj48JkMDUreEBw7yj96JrFSKqCg/edit?gid=0#gid=0").sheet1

load_dotenv()

genai.configure(api_key="AIzaSyAcu3YCl0UpFGtfGupXtmTtsae2uFI9w2A")

model = genai.GenerativeModel('gemini-1.5-flash')



user_link = input("YouTube Link: ")
directory = r"C:\Users\domin\OneDrive\Desktop"


print("Getting video...")
video = YouTube(
    user_link,  
    use_oauth=True,
    allow_oauth_cache=True
)
print("Downloading...")
video.streams.filter(progressive=True).get_highest_resolution().download(directory)

caption = None
if "a.en" in video.captions and "en" not in video.captions:
    caption = video.captions["a.en"]
elif "en" in video.captions and "a.en" not in video.captions:
    caption = video.captions["en"]
else:
    print("No captions available for the specified language code.")
    exit()

response = model.generate_content(f'Summarize and bullet the main points of this: {caption.xml_captions}')
print(response.text)


def add_data_to_next_row(data):
    try:
        row_data = [data['Video Title'], data['Video Summary']]
        sheet.append_row(row_data)
        print("Data added successfully.")
    except Exception as e:
        print(f"Error adding data: {e}")

data_to_send = {'Video Title': video.title, 'Video Summary': response.text}
add_data_to_next_row(data_to_send)

