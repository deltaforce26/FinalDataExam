import json
from groq import Groq
from app.settings.config import GROQ_API_KEY

def init_groq():
    client = Groq(
        api_key=GROQ_API_KEY
    )
    return client

def get_event_details(news: str, client) -> dict:
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "assistant",
                "content": '{ category": "", '
                           '"country": "", '
                           '"city": "", '
                           '"latitude": "", '
                           '"longitude": "" }'
            },
            {
                "role": "system",
                "content": "I will give you a description of news, and you tell me which category it belongs to:  general news, current terrorist event, or historical terrorist event. Additionally, only if it is a historical or current terrorist event, provide a location in the format of city and country and longitude of the city and latitude of the city, and return the result in JSON format in the JSON will be 3 keys: category, country and city and latitude and longitude of the city."
            },
            {
                "role": "user",
                "content" : news
            }
        ],
        temperature=0.5,
        max_tokens=4900,
        top_p=1,
        stream=False,
        response_format={"type": "json_object"},
        stop=None,
    )

    res = completion.choices[0].message.content

    return json.loads(res)


if __name__ == "__main__":
    groq_client = init_groq()
    content = "Mumbai, Nov 26 (ANI): November 26, 2024 marked the 16th anniversary of the 26/11 Mumbai terror attack that shook the nation. On the occasion, Maharashtra Guv Radhakrishnan paid floral tributes to Bravehearts at Martyrs' Memorial on premises of Police Commissioner's Office. Maharashtra CM Eknath Shinde also paid tribute to the Bravehearts at the Memorial on the 16th anniversary. Further, Maharashtra Deputy CMs Devendra Fadnavis, Ajit Pawar paid homage to the Bravehearts."
    result = get_event_details(content, groq_client)
    print(result)