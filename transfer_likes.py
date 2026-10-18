import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# რაზეც ვითხოვთ წვდომას (YouTube-ის მართვის უფლება)
SCOPES = ['https://www.googleapis.com/auth/youtube']

def authenticate(token_file, prompt_message):
    """
    ეს ფუნქცია პასუხისმგებელია დალოგინებაზე. 
    თუ უკვე დალოგინებული ვართ (გვაქვს token ფაილი), პირდაპირ შეგვიშვებს.
    თუ არა, გაგვიხსნის ბრაუზერს და გვთხოვს პაროლს.
    """
    print(f"\n{prompt_message}")
    creds = None
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
        creds = flow.run_local_server(port=0)
        # ვინახავთ დალოგინების სესიას, რომ ყოველ ჯერზე პაროლი არ გვთხოვოს
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
    return build('youtube', 'v3', credentials=creds)

def main():
    # 1. ვლოგინდებით ძველ ექაუნთში
    youtube_old = authenticate('token_old.json', "--- გთხოვთ, ბრაუზერში აირჩიოთ ძველი ექაუნთი ---")
    
    # 2. მოგვაქვს მოწონებული ვიდეოები (Pagination-ის გამოყენებით, რომ ყველა წამოვიღოთ)
    print("მოვძებნოთ მოწონებული ვიდეოები...")
    video_ids = []
    next_page_token = None
    
    while True:
        request = youtube_old.videos().list(
            part="snippet", 
            myRating="like", 
            maxResults=50, 
            pageToken=next_page_token
        )
        response = request.execute()
        
        for item in response.get('items', []):
            video_ids.append(item['id'])
            
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
            
    print(f"ნაპოვნია {len(video_ids)} მოწონებული ვიდეო/სიმღერა.")

    # 3. ვლოგინდებით ახალ (Premium) ექაუნთში
    youtube_new = authenticate('token_new.json', "--- ახლა ბრაუზერში აირჩიეთ ახალი (Premium) ექაუნთი ---")

    # 4. ვქმნით ახალ ფლეილისტს Premium ექაუნთზე
    print("ვქმნით ფლეილისტს ახალ ექაუნთზე...")
    playlist_insert_response = youtube_new.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": "My Transferred Likes",
                "description": "პითონით გადმოტანილი მოწონებული ვიდეოები",
            },
            "status": {
                "privacyStatus": "private" # ფლეილისტი იქნება დახურული
            }
        }
    ).execute()
    
    playlist_id = playlist_insert_response["id"]
    print(f"ფლეილისტი შეიქმნა! ვიწყებთ ვიდეოების გადმოტანას...")

    # 5. ძველი ექაუნთიდან წამოღებულ ვიდეოებს სათითაოდ ვამატებთ ახალ ფლეილისტში
    for vid in reversed(video_ids): # reversed ვიყენებთ, რომ ქრონოლოგია არ დაირღვეს
        try:
            youtube_new.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": vid
                        }
                    }
                }
            ).execute()
            print(f"ვიდეო ID: {vid} წარმატებით დაემატა.")
        except Exception as e:
            print(f"შეცდომა ვიდეოზე {vid} (შეიძლება ვიდეო წაშლილია ავტორის მიერ).")
            
    print("\nგილოცავ! ყველა ვიდეო წარმატებით გადავიდა ახალ ექაუნთზე!")

if __name__ == "__main__":
    main()
