from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from datetime import datetime


def get_datetime():
    #return str(datetime.now())
    current_datetime = datetime.now()
    return current_datetime.strftime("%H:%M:%S")
    
#current_datetime = datetime.now()

api_key = ""

model = ChatOpenAI(model='gpt-4.1-nano',
                   api_key=api_key
                  )

smart_description = """
SMART Goal Description
Specific:
A SMART goal should clearly define what needs to be achieved, who is involved, and what actions are required. 
Measurable:
The goal should include metrics or criteria that can be used to track progress and determine if it has been achieved. 
Achievable:
Goals should be realistic and attainable, considering available resources and capabilities. 
Relevant:
The goal should align with overall objectives and contribute to the larger purpose. 
Time-bound:
A SMART goal has a defined deadline or timeframe for completion, creating a sense of urgency and accountability. 
"""

template = smart_description 
template += """ to which item of SMART Goal description this phrase '{topic}' is most relevant to?. 
If the phrase does not match any of the items, please indicate it is off topic.
Provided output in the form of json object with 5 items of SMART goals and for 
each item indicate 1 if phrase is relevant for the item, 0 otherwise. Add off-topic item as well. 
"""

prompt_template = ChatPromptTemplate.from_template(template)


import streamlit as st

#st.text("This is text\n[and more text](that's not a Markdown link).")

#title = st.text_input("Movie title", "Life of Brian")
#st.write("The current movie title is", title)

left1, right1 = st.columns(2)

txt_script = left1.text_area("Input your script",
                             value="what is expected time line?",
                             height=300)
                             
txt_agenda = right1.text_area("Input your agenda",
                              value=smart_description,
                              height=300)
cnt1,cnt2 = st.columns(2)

if cnt1.button("Analyze Script"):
    prompt = prompt_template.invoke({"topic": txt_script})
    result = model.invoke(prompt)
    cnt1.write(get_datetime() +" "+result.content)

