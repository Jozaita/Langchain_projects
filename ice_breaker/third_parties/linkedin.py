import json
import os 
import requests


def scrape_linkedin_profile(linkedin_profile_url,mock=True):
    """Scrape information form a linkedin profile,
    Manually scrape information from a linkedin profile
    """
    if mock:
        response = requests.get("https://gist.githubusercontent.com/Jozaita/47a9d036278a3b7615e084e68c8cbe58/raw/c1e56a3142a15bdd80fd158df9c442ad63dc54df/test_json.json")
    else:
        headers = {'Authorization': 'Bearer ' + os.environ.get('PROXICURL_API_KEY')}
        api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
        params = {
            'linkedin_profile_url':linkedin_profile_url,
            'extra': 'include',
            'github_profile_id': 'include',
            'facebook_profile_id': 'include',
            'twitter_profile_id': 'include',
            'personal_contact_number': 'include',
            'personal_email': 'include',
            'inferred_salary': 'include',
            'skills': 'include',
            'use_cache': 'if-present',
            'fallback_to_cache': 'on-error',
        }
        response = requests.get(api_endpoint,
                                params=params,
                                headers=headers)
        

    json_response = response.json()

    json_response = {k:v for k,v in json_response.items() 
                        if (v not in ([],"","[]",None,"null")) 
                        and( k not in ("people_also_viewed","certifications"))}

    if json_response.get("groups"):
        for group in json_response.get("groups"):
            group.pop("profile_pic_url") 
    return json_response




if __name__ == "__main__":
    print(scrape_linkedin_profile("test",True))
    # response = requests.get("https://drive.google.com/uc?export=download&id=1I1eng_Sv7zZN5OotEmsqEGuF32eUlMpb",stream=True)
    # with open("test.jpeg", 'wb') as file:
    #     for chunk in response.iter_content(chunk_size=8192):
    #         if chunk:
    #             file.write(chunk)